---
name: cinderx-gdb-core-triage
description: Use when CPython/CinderX 或 pyperformance worker 出现 SIGSEGV、exit 139、core dump、SIGABRT、native assertion，需要 gdb bt full 和 core 证据。
---

# CinderX GDB/Core Triage

日志不能替代 native crash 证据。必须优先保留同一真实命令、`gdb bt full`、core dump 和寄存器信息。

## 触发

- `SIGSEGV`
- `exit 139`
- `core dump`
- `SIGABRT`
- native assertion failure

## 最小证据

- 同一真实命令和关键环境变量
- stdout/stderr、exit status、日志路径
- `gdb --args ...` 下的 `bt full`
- `info registers`
- 已有 core 时：`gdb <python> <core>`
- JIT 相关时补 `cinderx-hir-dump`

## 输出

crash 签名、栈、关键 frame、寄存器、core 摘要、最强根因假设和下一步验证命令。
