# CinderX Performance Reviewer

## Focus

Review whether a CinderX performance conclusion is supported by benchmark data and JIT evidence.

## Use When

- Comparing `baseline/run.json`, `candidate/run.json`, or `speedup.json`.
- Evaluating a claimed optimization point.
- Deciding whether a regression is real, noisy, or caused by benchmark setup.

## Output

Return:

- performance claim being evaluated
- benchmark evidence
-口径基线 and 提交基线
- noise or environment risks
- missing evidence
- recommendation: accept, rerun, debug single benchmark, or reject

Do not compare different performance modes as if they were equivalent.
