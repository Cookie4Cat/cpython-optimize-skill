---
name: cpython-runtime-test-run
description: Use when CPython/CinderX 需要运行 RuntimeTests 功能测试、test_cinderx/lib test 集成测试、相关子集、失败重跑或近千条全量验证。
---

# CPython Runtime Test Run

负责 RuntimeTests 功能测试和 test_cinderx/lib test 集成测试，不负责 pyperformance 性能测试。

## 三类测试用语

- RuntimeTests = 功能测试。
- test_cinderx/lib test = 集成测试。
- pyperformance = 性能测试，交给 `pyperformance-worker-run` 或 `pyperformance-suite-run`。

## 验证等级

- L1 smoke：`import cinderx`、最小 JIT、目标单元测试、目标功能测试。
- L3 相关子集：受影响 RuntimeTests 功能测试、test_cinderx/lib test 集成测试、失败用例集合。
- L4 全量：近千条 CPython Runtime / CinderX 聚合测试，提交或报告前使用。

## 命令形态

- RuntimeTests 功能测试：`$CINDERX_TEST_PYTHON ci_pipeline/run_gate.py --suite runtime [--coverage]`。
- test_cinderx/lib test 集成测试：`CINDERX_LOCAL_RUN_LIBTEST=1 $CINDERX_TEST_PYTHON ci_pipeline/run_gate.py --suite cinderx_local`。
- 只跑受影响集合时，保留同一解释器、同一容器线、同一 JIT flags，并记录裁剪理由。

## 规则

- L1 未过，不讨论性能收益。
- 失败重跑必须复用原命令、环境变量、日志路径和 exit status。
- `SIGSEGV` / `exit 139` 转 `cinderx-gdb-core-triage`。
- 测试前后记录 Python、CinderX commit、容器线和 JIT flags。
- 功能测试或集成测试未通过时，不把 pyperformance 性能测试结果写成可提交结论。

输出测试范围、真实命令、失败列表、晋级理由和下一步。
