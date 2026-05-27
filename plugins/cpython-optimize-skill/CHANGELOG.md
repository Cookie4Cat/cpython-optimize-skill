# Changelog

本文件记录 `cpython-optimize-skill` 的版本演进。

## v0.8.1

- 新增统一 `反问 Gate`：当目标路线、实验轴、高成本动作、运行中异常或证据链缺口无法唯一确定时，要求先反问用户
- 为 orchestrator、environment verifier、runner、benchmark analyst、crash triager、JIT analyst、platform analyst 补充各自必须反问的缺口
- 为环境清理、bootstrap、远端操作、A/B slot、pyperformance suite/result、gdb/core、ISA/微架构和验证策略补充反问门禁
- 新增 pressure scenario 32，覆盖必要信息缺失时 `request_user_input` / `AskUserQuestion` 的平台映射和文本降级路径
- 新增 `clarifying-question-templates.md`，统一结构化反问字段、平台映射、文本降级和 CPython/CinderX 高频模板

## v0.8.0

- 新增 `validation-strategy` 子技能，定义 L0-L4 验证阶梯、晋级规则、成本预算和缓存复用原则
- 新增 `workflow-cross-platform-delta-triage`，用于双平台性能差距根因定位和收益扩散验证
- 新增 `workflow-feature-driven-optimization`，用于已知特性驱动的代码优化、功能用例和性能验证
- 新增 `workflow-platform-differential-discovery`，用于系统分析 ISA / 微架构差异并发现优化点
- 将 `using-cpython-optimize` 压薄为 Orchestrator router，明确 Workflow → Agent → Skill 三层分发
- 将 workflow 分为主 Workflow 和 Supporting Workflow，避免旧流程被误用为端到端优化入口
- 新增 Agent 层：`cinderx-orchestrator`、`cinderx-environment-verifier`、baseline/candidate runner、benchmark analyst、crash triager、JIT analyst、platform analyst
- 大幅重切专业 skill：拆出 `cinderx-env-validate`、`cinderx-env-clean`、`cinderx-env-bootstrap`、`cinderx-remote-lab-ops`、`cinderx-ab-run-slot`、`pyperformance-worker-run`、`pyperformance-suite-run`、`cinderx-gdb-core-triage`、`cinderx-hir-dump`、`cinderx-isa-microarch-compare` 等 CPython/CinderX 专业动作
- 移除 `SessionStart` 全量注入 hook，避免启动、恢复和压缩后重复消耗 token
- 新增 `PostToolUse` 运行中信号 hook，在 Bash 输出出现 CinderX crash、timeout、网络卡顿或远程无输出时注入短提醒
- 新增 pressure scenarios 19-31 覆盖准确、高效、workflow 分层、Agent 层、运行中 hook 路由和专业 skill 边界

## v0.7.1

- 增加 CPython/CinderX 编译前 API/ABI 版本门禁，防止目标容器为 Python 3.14.3 时误用 Python 3.14.5 API
- 强化 `SIGSEGV` / `exit 139` crash triage：优先 `gdb bt full`、core dump、HIR/JIT 证据，禁止用反复加日志替代 native 取证
- 增加远程命令输出契约：首次执行必须保留 stdout/stderr、exit status、日志路径或 tmux pane
- 增加远程异常耗时处理：网络卡顿需使用 timeout、镜像/代理/DNS 诊断，并在需要决策时询问用户
- 将 `agents/` 角色文档统一重写为中文，并增加中文模板验证
- 新增 pressure scenarios 15-18 覆盖上述失败模式

## v0.7.0

- 仓库改为 marketplace 结构：插件内容移至 `plugins/cpython-optimize-skill/`，根目录仅保留 marketplace 元数据
- marketplace.json 的 source 路径改为 `./plugins/cpython-optimize-skill`
- README 中 Codex 安装命令修正为 `codex plugin add <plugin>@<marketplace>` 格式

## v0.6.1

- docker-compose 模板所有路径改为环境变量，消除相对路径依赖
- 区分用户侧必填变量（CINDERX_ROOT、CPYTHON_ROOT、PYPERFORMANCE_ROOT）和 skill 侧可选变量

## v0.6.0

- docker-runtime 技能增加镜像构建规则和网络诊断指引
- 模板目录统一为单一 README（消除冗余的 project-readme.md）
- 基础镜像升级为 openEuler 24.03 LTS SP3
- 新增 Codex CLI 插件市场支持（`.agents/plugins/marketplace.json`）
- README 安装说明区分 Claude Code 和 Codex CLI
- 结构验证测试覆盖 `.agents/plugins/` 目录

## v0.5.2

- 性能测试基线版本统一为 Python 3.14.3
- 更新 `cpython-baseline` Dockerfile 中 `PYTHON_VERSION`
- 同步详细设计模板（用户修订）

## v0.5.1

- 新增 `.claude-plugin/marketplace.json` 支持插件市场安装
- 精简 README：移除性能口径、Docker 双线等子技能内容，改为入口技能承载
- 修正 Claude Code 技能调用说明（无 `/skill` 斜杠命令）
- README 添加 emoji 分节

## v0.5.0

新增设计文档编写技能：
- 新增 `skills/design-documentation/` 子技能
  - 架构设计、系统设计、功能设计、详细设计四类标准模板
  - 自顶向下设计流程（架构 → 系统可选 → 功能 → 详细）
  - 文档类型选择决策流程图
  - 编写原则与格式约定
  - 设计文档统一输出到 `docs/design/`
- 更新引导技能 `using-cpython-optimize` 新增 `design-documentation` 条目

## v0.4.0

重构为复合技能仓库：
- 新增 `.claude-plugin/plugin.json`、`.codex-plugin/plugin.json`、`package.json` 插件注册
- 新增 `hooks/` SessionStart 自动注入引导技能
- 新增 `skills/using-cpython-optimize/` 引导技能（含决策流程图和 FAQ）
- 将 6 个工作流迁移为自包含子技能：
  - `skills/remote-environment/` — SSH、tmux、rsync
  - `skills/cpython-build/` — 编译与安装
  - `skills/docker-runtime/` — Docker 容器隔离（含模板和脚本）
  - `skills/pyperformance-test/` — 基准测试（含命令模板、脚本、crash triage）
  - `skills/cinderx-analysis/` — JIT/非JIT 用例分析（含性能口径定义）
  - `skills/experiment-documentation/` — 文档规范（含产物 schema）
- 每个 子技能自包含 SKILL.md + 专属 references/scripts/templates
- playbook 内容按主题吸收到对应子技能
- 移除旧目录：`docs/workflows/`、`docs/playbooks/`、`references/`、`scripts/`
- `docs/` 重新定位为仓库级文档（plans、开发文档）

## v0.3.0

- 明确远程环境工作流：
  - 先确认 SSH 可登录
  - 再使用 `rsync` 同步代码仓
  - 再进入 Docker 容器隔离
- 强化远程宿主机目录隔离约束，避免 bind mount 覆盖已有目录
- 明确容器内 `pip` 默认应切到国内镜像源，优先阿里云或华为云
- 明确 dump HIR 时应优先复用真实测试命令，只增减 debug 环境变量
- 新增性能口径定义：
  - `CPython 解释执行`
  - `CPython JIT`
  - `CinderX 解释执行`
  - `CinderX JIT`
- 明确 `baseline` 的两种含义：
  - 口径基线
  - 提交基线
- 明确 Arm vs x86 属于跨平台对比，必须参数和口径一致
- 修正 HIR 分析顺序：
  - 先确认进入 CinderX JIT
  - 再做热点归因
  - 最终输出必须包含具体 HIR 片段、问题说明和修改方案

## v0.2.0

- 重构为“核心层 + 四平台薄包装”
- 补齐主工作流：
  - SSH / tmux
  - 构建与强制覆盖安装
  - `pyperformance` 测试
  - Docker 运行时隔离
  - 文档规范
  - 用例分析
- 固化 Docker 双线：
  - `cpython-baseline`
  - `cinderx-test`
- 收录真实环境命令模板
- 迁入已验证的 `cinderx-test` 脚本
- 补齐 FAQ、入口决策表、静态/动态 pressure test

## v0.1.0

- 初始化技能仓库脚手架
- 建立 CPython/CinderX 联合优化技能的基础目录结构
- 确立以 CinderX 优先的个人工作流定位
