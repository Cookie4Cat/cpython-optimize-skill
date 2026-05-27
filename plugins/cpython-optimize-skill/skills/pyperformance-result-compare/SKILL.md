---
name: pyperformance-result-compare
description: Use when 已有 pyperformance run.json 或 speedup.json，需要比较 baseline/candidate、方差、噪声、提交 baseline、收益范围或回归可信度。
---

# pyperformance Result Compare

负责解释结果，不负责跑 benchmark。

## 输入

- baseline `run.json`
- candidate `run.json`
- `speedup.json`
- 提交 baseline / candidate commit
- 口径 baseline：CPython JIT、CinderX JIT、解释执行等

## 判断

- 命令口径是否一致
- baseline/candidate 是否只在目标变量上不同
- 方差、噪声和异常值
- 收益范围、无收益范围、未验证范围
- 需要回到 `pyperformance-worker-run` 的异常用例

输出可信收益、可信回归、噪声项、补测建议和不能外推的范围。
