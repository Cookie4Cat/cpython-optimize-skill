# pyperformance Crash Triage

## 目标

快速判断问题属于：
- 依赖缺失
- 环境变量没传到 worker
- `_cinderx` / `cinderjit` 导入失败
- JIT 启动期 compile storm
- 真正的 native crash

## 最小检查顺序

1. 看退出码
   - `139` 通常是 `SIGSEGV`
2. 看是否进入 JIT
3. 看 worker 进程环境
4. 看 `jit.log` 最后一个函数
5. 必要时直接 `gdb` / core dump

## Native crash 取证门禁

看到 `SIGSEGV`、`exit 139`、`Segmentation fault` 或 `core dumped` 时，先冻结“猜测式修复”和反复加日志，保留真实复现命令。

最低证据：

- 完整命令和关键环境变量
- 退出信号 / exit status
- `gdb` 下的 `bt full`
- 可用时保存 core dump 摘要
- JIT 相关 crash 额外保留 `jit.log`、HIR dump 或说明为何无法采集

示例：

```bash
gdb --args python <run_benchmark.py> <真实参数>
(gdb) run
(gdb) bt full
(gdb) info registers
```

已有 core 时：

```bash
gdb <python> <core>
(gdb) bt full
```

日志不能替代 native crash 证据。只有在 `gdb` / core dump 不可用且原因已记录时，才退而使用更细日志缩小范围。

## 常见误判

- `JIT log` 里没有 `__main__:*`，不代表没有进入 JIT
- `venv python` 手工导入成功，不代表 `pyperformance` worker 里也成功
- `python -m pyperformance run` 正常，不代表 `bench_command()` 子进程链也正常

## 高频根因

- `LD_LIBRARY_PATH` 没有传到 worker，导致 `_cinderx` 因 `libstdc++` 版本不匹配而导入失败
- `PYTHONPATH` 只让 hook 可见，但没有让 editable 安装对应的源码路径真正生效
- 坏代理导致容器或 worker 里的 `pip` / 初始化链路失败
- 低阈值 AutoJIT 把启动期、第三方包或 synthetic code 也卷进 compile storm
