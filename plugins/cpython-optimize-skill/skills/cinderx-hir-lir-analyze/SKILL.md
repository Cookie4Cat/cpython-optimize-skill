---
name: cinderx-hir-lir-analyze
description: Use when 需要分析 CinderX HIR、LIR、uop、机器码、deopt、frame layout、调用约定、codegen 形态并输出修改方案。
---

# CinderX HIR/LIR Analyze

先由 `cinderx-jit-entry-check` 确认进入 JIT，再做热点和 IR 解释。

## 顺序

1. 热点归因。
2. HIR 片段。
3. LIR 片段。
4. uop / 机器码。
5. deopt、frame layout、调用约定、trampoline。
6. 修改方案和最小验证命令。

## 输出格式

- 热点归因
- 具体 HIR/LIR/uop/机器码片段
- 问题说明
- 修改方案
- 风险和回归用例

没有具体片段时，不把它算作完整优化点。
