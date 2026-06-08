---
name: cinderx-gdb-core-triage
description: Use when CPython/CinderX 或 pyperformance worker 出现 SIGSEGV、exit 139、core dump、SIGABRT、native assertion，需要 gdb bt full 和 core 证据。
---

# CinderX GDB/Core Triage

日志不能替代 native crash 证据。必须优先保留同一真实命令、`gdb bt full`、core dump 和寄存器信息。

如果容器内缺少 `gdb` 或相关取证工具，先读取 `../using-cpython-optimize/references/container-tooling-guidance.md`。允许补装 `gdb`、`ripgrep` / `rg`、`strace`、`perf`、`binutils`；补装前探测包管理器、DNS、代理、镜像源和 cache，网络慢时及时反馈。不要因为缺 `gdb` 就改用反复加日志替代 native 取证。

## 触发

- `SIGSEGV`
- `exit 139`
- `core dump`
- `SIGABRT`
- native assertion failure

## 最小证据

- 同一真实命令和关键环境变量
- stdout/stderr、exit status、日志路径
- `command -v gdb`；缺失时记录工具补装探测、安装命令、耗时和 exit status
- `gdb --args ...` 下的 `bt full`
- `info registers`
- 已有 core 时：`gdb <python> <core>`
- JIT 相关时补 `cinderx-hir-dump`

## 反问 Gate

- 缺真实复现命令、core 路径或 Python binary，且无法从日志恢复时，询问用户提供或授权重跑。
- 多个 core、多个容器线或多个解释器可能匹配同一 crash 时，询问要绑定哪一组证据。
- 补装 `gdb` / `strace` / `perf` 等工具时网络慢、metadata 长时间无输出或需要切镜像/离线包时，询问继续等待、切镜像、复用 cache、上传离线包或中止。
- 需要 attach live process、保留现场或执行可能改变现场的清理/重跑时，先询问。

## 输出

crash 签名、栈、关键 frame、寄存器、core 摘要、最强根因假设和下一步验证命令。
