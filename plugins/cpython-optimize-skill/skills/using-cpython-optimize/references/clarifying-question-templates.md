# 结构化反问模板

用于 Orchestrator 在 `反问 Gate` 触发时生成平台无关的问题。先查证仓库、环境、日志和历史产物；只有无法唯一确定时才问。

## 公共格式

使用 Codex 和 Claude Code 都能表达的最小公共子集：

| 字段 | 约束 |
|------|------|
| `question_id` | snake_case，写入后续决策记录 |
| `header` | 不超过 12 个字符 |
| `question` | 只问当前阻塞决策，不夹带说明长文 |
| `options` | 2-3 项；推荐项放第一项；每项有 `label` 和 `description` |

Codex：映射到 `request_user_input`，`question_id` -> `id`，推荐项 label 加 `(Recommended)`；不要手写 `Other`，客户端会提供自由输入。

Claude Code：映射到 `AskUserQuestion`，保留相同 `header/question/options`；`question_id` 只用于本地决策记录。

文本降级：工具不可用时输出同样的 `header/question/options`，请用户回复选项 label 或补充自定义答案。

## 通用规则

- 不问能用命令、文件、日志、`run.json` 或 core 直接查到的信息。
- 一次只问阻塞下一步的 1-2 个问题；多个独立缺口优先问最高风险缺口。
- 选项必须互斥，避免“都可以”。
- 用户回答后记录：`question_id`、选择 label、影响的 workflow/agent/skill、时间戳或当前阶段。

## 模板

### `workflow_route`

header: `路线`

question: `这次 CPython/CinderX 任务优先走哪条路线？`

| label | description |
|-------|-------------|
| `差距定位` | 根据已测双平台或 A/B 性能差距定位根因和优化点。 |
| `特性优化` | 基于已知特性改代码、补功能/集成测试并验证收益。 |
| `平台扫描` | 系统分析 ISA/微架构差异，寻找候选优化点。 |

### `validation_level`

header: `验证`

question: `当前阶段需要做到哪个验证等级？`

| label | description |
|-------|-------------|
| `L2 单用例` | 先复现目标 benchmark、crash 或热点，成本最低。 |
| `L3 小集合` | 跑相关 Runtime/pyperformance 子集，验证收益扩散。 |
| `L4 全量` | 跑全量 Runtime 或 pyperformance，用于提交/报告前确认。 |

### `environment_target`

header: `环境`

question: `要使用哪类 CPython/CinderX 实验环境？`

| label | description |
|-------|-------------|
| `复用现有` | 先校验依赖、版本、SOABI、CinderX install 和 smoke。 |
| `新建环境` | 新建 workspace/container，耗时更长但隔离更干净。 |
| `清理重建` | 仅在环境已被证明污染或破坏时使用。 |

### `destructive_clean`

header: `清理`

question: `清理会影响已有产物，下一步怎么处理？`

| label | description |
|-------|-------------|
| `保留产物` | 只清理可证明污染项，保留 cache、日志、run.json、core、HIR。 |
| `清理重建` | 删除指定污染环境并重新 bootstrap。 |
| `只做审计` | 暂不清理，继续收集环境指纹和污染证据。 |

### `remote_stall`

header: `远端`

question: `远端任务异常无输出或网络变慢，下一步怎么处理？`

| label | description |
|-------|-------------|
| `先诊断` | 查进程、tmux、日志、exit status、DNS、代理、镜像源和 cache。 |
| `继续等待` | 保持任务运行，但加进度检查或超时。 |
| `中止换源` | 停止当前路径，切镜像/缓存/离线依赖后重试。 |

### `ab_slot`

header: `A/B`

question: `baseline 和 candidate 的运行资源如何安排？`

| label | description |
|-------|-------------|
| `先审计` | 先确认 CPU set、容器线、tmux pane 和结果目录不冲突。 |
| `并行执行` | 资源已隔离时同时运行 baseline/candidate。 |
| `串行执行` | 隔离不确定或机器资源不足时降低干扰。 |

### `crash_evidence`

header: `Crash`

question: `crash 证据链缺口怎么补？`

| label | description |
|-------|-------------|
| `授权重跑` | 复用真实命令重跑，采集 exit status、core 和 gdb bt full。 |
| `提供 core` | 用户提供已有 core、Python binary、日志和环境指纹。 |
| `保留现场` | 暂停清理，先 attach 或备份现场。 |

### `result_artifacts`

header: `结果`

question: `性能结果缺少配对产物，下一步怎么处理？`

| label | description |
|-------|-------------|
| `提供路径` | 用户给 baseline/candidate run.json 或 speedup.json 路径。 |
| `补跑缺失` | 只补跑缺失一侧或异常 benchmark。 |
| `降级结论` | 只输出当前证据支持的范围，不外推。 |

### `scope_budget`

header: `预算`

question: `当前任务的时间/资源预算怎么控制？`

| label | description |
|-------|-------------|
| `低成本` | L0-L2 为主，优先复用缓存和已有产物。 |
| `平衡` | 允许相关小集合和必要增量构建。 |
| `充分验证` | 可运行高成本 L3/L4，用于提交或报告结论。 |
