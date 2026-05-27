# 🔧 CPython/CinderX 性能优化技能仓库

面向个人工作流的 CPython/CinderX 性能优化与设计文档技能集合，以 Claude Code / Codex 插件形式交付。

---

## 📦 技能一览

| 技能 | 用途 | 自带资源 |
|------|------|---------|
| 🎯 `using-cpython-optimize` | Orchestrator 路由入口 | — |
| 🧪 `cinderx-env-validate` | Python/SOABI/CinderX/pyperformance 环境三态校验 | — |
| 🧹 `cinderx-env-clean` | 清理被污染的 CinderX lab | — |
| 🐳 `cinderx-env-bootstrap` | 初始化 Docker 双线、CinderX editable、pyperformance | templates/、scripts/ |
| 🔌 `cinderx-remote-lab-ops` | 远端 SSH/tmux/rsync/docker compose 和输出契约 | — |
| 🧷 `cinderx-ab-run-slot` | baseline/candidate slot、CPU affinity、结果目录隔离 | — |
| 🧪 `cpython-runtime-test-run` | CPython Runtime / CinderX correctness 测试 | — |
| 🔎 `cinderx-smoke-check` | import cinderx、_cinderx、最小 JIT、HIR smoke | — |
| 📊 `pyperformance-worker-run` | 单 benchmark worker、bench_command、sitecustomize | references/、scripts/ |
| 📈 `pyperformance-suite-run` | 正式 `python -m pyperformance run` | — |
| 📉 `pyperformance-result-compare` | run.json、speedup.json、收益/回归/噪声判断 | — |
| 🧯 `cinderx-gdb-core-triage` | SIGSEGV、exit 139、core、gdb 证据链 | references/ |
| 🧾 `cinderx-hir-dump` | 真实 worker 命令叠加 HIR / jit.log | — |
| 🔬 `cinderx-jit-entry-check` | 确认 benchmark 本体进入 CinderX JIT | — |
| 🔬 `cinderx-hir-lir-analyze` | HIR/LIR/uop/机器码和修改方案 | references/ |
| 🧭 `cinderx-isa-microarch-compare` | Kunpeng/x86 ISA、微架构、perf 差异矩阵 | — |
| 📝 `cinderx-optimization-report` | CinderX 优化报告和证据链沉淀 | references/ |
| ✅ `validation-strategy` | 验证阶梯、成本预算、缓存复用 | — |
| 📐 `design-documentation` | 架构/系统/功能/详细设计文档 | references/ |

## 👥 Agent 一览

| Agent | 职责 |
|-------|------|
| `cinderx-orchestrator` | 运行时主 Agent，选择 workflow 并分派阶段 Agent |
| `cinderx-environment-verifier` | 环境三态：可复用、新环境、被破坏环境 |
| `pyperformance-baseline-runner` | 接管 baseline slot |
| `pyperformance-candidate-runner` | 接管 candidate slot |
| `pyperformance-benchmark-analyst` | 解读 run.json / speedup.json |
| `cinderx-crash-triager` | 接管 native crash 取证 |
| `cinderx-jit-analyst` | 接管 JIT/HIR/LIR 优化分析 |
| `cinderx-platform-analyst` | 接管 ISA / 微架构差异分析 |

## 🔁 Workflow 一览

主 Workflow 是用户目标入口；Supporting Workflow 是主流程内部按需调用的阶段或异常分支。

### 主 Workflow

| Workflow | 用途 |
|----------|------|
| `workflow-cross-platform-delta-triage` | 双平台性能差距根因定位和收益验证 |
| `workflow-feature-driven-optimization` | 已知特性驱动的代码优化、功能用例和性能验证 |
| `workflow-platform-differential-discovery` | 系统分析 ISA / 微架构差异并发现优化点 |

### Supporting Workflow

| Workflow | 用途 |
|----------|------|
| `workflow-remote-cinderx-lab-setup` | 从零准备远程 CPython/CinderX 优化实验环境 |
| `workflow-cinderx-crash-triage` | 复现、定位并记录 CinderX/pyperformance crash |
| `workflow-pyperformance-regression` | L3/L4 正式 pyperformance 对比、性能回归和报告沉淀 |
| `workflow-jit-optimization-analysis` | 单 benchmark JIT 热点、HIR/LIR 和优化点分析 |

Workflow 是多个技能和专门 Agent 的编排入口；原子技能继续负责具体领域知识、命令约束和产物格式。

---

## 🚀 安装

### Claude Code（插件市场）

```
/plugin marketplace add https://github.com/sisibeloved/cpython-optimize-skill
/plugin install cpython-optimize-skill
```

安装后，Agent 通过 skill 描述按需加载 `using-cpython-optimize`。插件还带有轻量运行中 hook：当 Bash 输出出现 `SIGSEGV`、`exit 139`、core dump、timeout 或远程无输出等信号时，只注入短提醒，提示 Agent 加载 `cinderx-gdb-core-triage` 或 `cinderx-remote-lab-ops`。

首次启用或更新 hook 后，按宿主 Agent 的要求在 `/hooks` 中 review / trust 新的 hook 定义。

### Codex CLI

```bash
codex plugin marketplace add https://github.com/sisibeloved/cpython-optimize-skill
codex plugin add cpython-optimize-skill@cpython-optimize-skill
```

---

## 💬 使用示例

```
> 帮我在 Kunpeng 上编译 CinderX 并跑一次 pyperformance
> regex_compile 在容器里 SIGSEGV 了，帮我复现和定位
> 对比 stock CPython JIT 和 CinderX JIT 的 pyperformance 数据
> Kunpeng 和 x86 上同一个 benchmark 差距很大，帮我找根因
> 帮我写一份 CinderX JIT 优化点的架构设计说明书
```

Agent 会根据任务自动选择对应技能，无需手动加载。

---

## 📁 仓库结构

```
.
├── .agents/plugins/                         # Codex 插件市场元数据
│   └── marketplace.json
├── .claude-plugin/                          # Claude Code 插件市场元数据
│   └── marketplace.json
├── plugins/cpython-optimize-skill/          # 实际插件包
│   ├── .claude-plugin/
│   │   └── plugin.json
│   ├── .codex-plugin/
│   │   └── plugin.json
│   ├── hooks/
│   │   ├── hooks.json
│   │   └── runtime-skill-router
│   ├── skills/                              # 原子技能 + workflow 技能
│   │   ├── using-cpython-optimize/
│   │   ├── cinderx-env-validate/
│   │   ├── cinderx-env-clean/
│   │   ├── cinderx-env-bootstrap/
│   │   ├── cinderx-remote-lab-ops/
│   │   ├── cinderx-ab-run-slot/
│   │   ├── cpython-runtime-test-run/
│   │   ├── cinderx-smoke-check/
│   │   ├── pyperformance-worker-run/
│   │   ├── pyperformance-suite-run/
│   │   ├── pyperformance-result-compare/
│   │   ├── cinderx-gdb-core-triage/
│   │   ├── cinderx-hir-dump/
│   │   ├── cinderx-jit-entry-check/
│   │   ├── cinderx-hir-lir-analyze/
│   │   ├── cinderx-isa-microarch-compare/
│   │   ├── cinderx-optimization-report/
│   │   ├── validation-strategy/
│   │   ├── design-documentation/
│   │   ├── workflow-remote-cinderx-lab-setup/
│   │   ├── workflow-cinderx-crash-triage/
│   │   ├── workflow-pyperformance-regression/
│   │   ├── workflow-jit-optimization-analysis/
│   │   ├── workflow-cross-platform-delta-triage/
│   │   ├── workflow-feature-driven-optimization/
│   │   └── workflow-platform-differential-discovery/
│   ├── agents/                              # workflow 可引用的专门 Agent 角色文档
│   ├── tests/
│   ├── docs/
│   ├── package.json
│   └── CHANGELOG.md
├── README.md
└── .gitignore
```

每个技能自包含 `SKILL.md` + 专属 `references/`、`scripts/`、`templates/`，技能间通过 Skill 工具互相调用。

---

## ✅ 验证

```bash
cd plugins/cpython-optimize-skill
python3 tests/validate_skill_layout.py
python3 tests/validate_pressure_scenarios.py
```

## 📜 版本历史

见 `plugins/cpython-optimize-skill/CHANGELOG.md`。

## 📄 许可

MIT
