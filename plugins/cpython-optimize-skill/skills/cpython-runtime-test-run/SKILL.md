---
name: cpython-runtime-test-run
description: Use when CPython/CinderX correctness 需要运行 CPython Runtime、CinderX 单元测试、功能测试、相关子集、失败重跑或近千条全量验证。
---

# CPython Runtime Test Run

负责 correctness，不负责 pyperformance 性能。

## 验证等级

- L1 smoke：`import cinderx`、最小 JIT、目标单元测试、功能测试。
- L3 相关子集：受影响 Runtime 目录、CinderX correctness 子集、失败用例集合。
- L4 全量：近千条 CPython Runtime / CinderX 聚合测试，提交或报告前使用。

## 规则

- L1 未过，不讨论性能收益。
- 失败重跑必须复用原命令、环境变量、日志路径和 exit status。
- `SIGSEGV` / `exit 139` 转 `cinderx-gdb-core-triage`。
- 测试前后记录 Python、CinderX commit、容器线和 JIT flags。

输出测试范围、真实命令、失败列表、晋级理由和下一步。
