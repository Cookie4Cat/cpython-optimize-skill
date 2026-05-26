# 🔧 CPython/CinderX 性能优化技能仓库

面向个人工作流的 CPython/CinderX 性能优化与设计文档技能集合，以 Claude Code / Codex 插件形式交付。

---

## 📦 技能一览

| 技能 | 用途 | 自带资源 |
|------|------|---------|
| 🎯 `using-cpython-optimize` | 引导入口，自动注入 | — |
| 🔌 `remote-environment` | SSH、tmux、rsync | — |
| 🔨 `cpython-build` | CPython/CinderX 编译与安装 | — |
| 🐳 `docker-runtime` | Docker 双线隔离 | templates/、scripts/ |
| 📊 `pyperformance-test` | 基准测试、性能口径、crash triage | references/、scripts/ |
| 🔬 `cinderx-analysis` | JIT/非 JIT 分析、HIR/LIR 定位 | references/ |
| 📝 `experiment-documentation` | 实验记录、报告模板 | references/ |
| 📐 `design-documentation` | 架构/系统/功能/详细设计文档 | references/ |

## 🔁 Workflow 一览

| Workflow | 用途 |
|----------|------|
| `workflow-remote-cinderx-lab-setup` | 从零准备远程 CPython/CinderX 优化实验环境 |
| `workflow-cinderx-crash-triage` | 端到端复现、定位并记录 CinderX/pyperformance crash |
| `workflow-pyperformance-regression` | 正式 pyperformance 对比、性能回归和报告沉淀 |
| `workflow-jit-optimization-analysis` | 单 benchmark JIT 热点、HIR/LIR 和优化点分析 |

Workflow 是多个技能和专门 Agent 的编排入口；原子技能继续负责具体领域知识、命令约束和产物格式。

---

## 🚀 安装

### Claude Code（插件市场）

```
/plugin marketplace add https://github.com/sisibeloved/cpython-optimize-skill
/plugin install cpython-optimize-skill
```

安装后，新会话启动时 `using-cpython-optimize` 引导技能会通过 SessionStart hook 自动注入上下文。

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
│   │   └── session-start
│   ├── skills/                              # 原子技能 + workflow 技能
│   │   ├── using-cpython-optimize/
│   │   ├── remote-environment/
│   │   ├── cpython-build/
│   │   ├── docker-runtime/
│   │   ├── pyperformance-test/
│   │   ├── cinderx-analysis/
│   │   ├── experiment-documentation/
│   │   ├── design-documentation/
│   │   ├── workflow-remote-cinderx-lab-setup/
│   │   ├── workflow-cinderx-crash-triage/
│   │   ├── workflow-pyperformance-regression/
│   │   └── workflow-jit-optimization-analysis/
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
