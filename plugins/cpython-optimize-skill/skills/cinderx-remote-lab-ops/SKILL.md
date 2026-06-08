---
name: cinderx-remote-lab-ops
description: Use when CPython/CinderX lab 在远端机器上，需要 SSH、tmux、rsync、docker compose、日志路径、stdout/stderr、exit status、timeout 或长任务输出契约。
---

# CinderX Remote Lab Ops

远端操作必须服务于 CPython/CinderX lab，不是通用 SSH 技巧。

## 标准对象

- workspace：当前 Agent 独立宿主机目录。
- tmux：按任务固定 session/window/pane。
- docker compose：只操作 `cinderx-test` / `cpython-baseline`。
- logs：每个构建、安装、测试、benchmark 都有日志路径。

## 输出契约

每条远程命令第一次运行就记录真实命令、stdout/stderr、exit status、日志路径和 tmux pane。长任务必须有 `timeout` 或进度检查策略。

```bash
set -o pipefail
<command> 2>&1 | tee logs/<task>.log
status=${PIPESTATUS[0]}
printf '\n[exit status=%s]\n' "$status"
exit "$status"
```

## 异常处理

- 无输出：查进程、tmux capture-pane、日志、CPU/IO/磁盘。
- 网络慢：查 DNS、代理、pip mirror、git 连接和 cache。
- 容器内缺少 `gdb`、`rg` / `ripgrep`、`strace`、`perf`、`binutils` 等排障工具时，先读取 `../using-cpython-optimize/references/container-tooling-guidance.md`，探测网络、包管理器、镜像源和 cache，再决定补装；不要直接绕开关键取证路径。
- 不确定是否继续等待时，询问用户。

不要为了补输出盲目重复构建、安装或 benchmark。

## 反问 Gate

- 远端命令长时间无新增输出，且进程/日志无法证明正常推进时，询问继续等待、查看交互终端、中止还是换策略。
- pip/git/网络下载异常慢时，询问继续等待、切镜像、复用 cache 或让用户处理网络。
- 补装工具的 metadata refresh 或安装长时间无输出时，及时反馈并询问继续等待、切镜像、复用 cache、上传离线包或中止。
- 要 kill 进程、清理目录、重跑有副作用命令或覆盖日志时，先询问。
