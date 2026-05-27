---
name: cinderx-isa-microarch-compare
description: Use when 需要比较 Kunpeng/x86、Arm/x86 的 ISA、微架构、perf、cache、分支预测、SIMD、barrier、hugepages 或 codegen lowering 差异。
---

# CinderX ISA/Microarch Compare

平台差异分析先建立矩阵，再进入 HIR/LIR 细节。

## 矩阵

- 平台：Kunpeng、x86、内核、容器、CPU governor。
- ISA：指令选择、SIMD、原子、barrier、寄存器和调用约定。
- 微架构：cache、分支预测、流水线、内存带宽、TLB、hugepages。
- 观测：perf top/stat、机器码、speedup、benchmark 覆盖。
- lowering：CinderX codegen 是否生成不同形态。

## 输出

平台差异点、受影响 benchmark、候选优化点、最小验证命令和需要排除的环境漂移。

不要一开始就陷入某个 HIR pass；先证明平台差异存在。
