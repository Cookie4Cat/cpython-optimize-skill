---
name: workflow-remote-cinderx-lab-setup
description: 需要从零准备远程 CPython/CinderX 优化实验环境时使用；串联 SSH/tmux、独立宿主机目录、Docker 双线、源码同步、构建和最小 smoke 验证
---

# Remote CinderX Lab Setup Workflow

## 目标

建立一个可重复使用、互不污染的远程优化实验环境，为后续 crash triage、benchmark 和 JIT 分析提供基础。

## 调用技能

| 阶段 | 技能 | 产出 |
|------|------|------|
| 远程接入 | `remote-environment` | SSH 别名、独立宿主机目录、tmux 会话 |
| 容器准备 | `docker-runtime` | `cinderx-test` 和可选 `cpython-baseline` |
| 构建安装 | `cpython-build` | CinderX editable install 或 CPython baseline |
| smoke 验证 | `pyperformance-test` | 最小 benchmark 或导入验证命令 |
| 环境记录 | `experiment-documentation` | 环境记录或 setup note |

## 推荐 Agent

- `agents/pyperformance-env-auditor.md`：检查 Python、pyperformance、LD_LIBRARY_PATH、PYTHONPATH 和 JIT 环境变量。

## Workflow Gates

### Gate 1: 宿主机目录隔离

每个 Agent 必须使用独立宿主机目录，不能直接复用其他任务的工作目录。

### Gate 2: 容器隔离

默认进入 Docker 容器工作。只有在 Docker 与真实环境差异需要复核时，才回到宿主机。

### Gate 3: 安装验证

开始 benchmark 或分析前必须确认：

- 当前 Python 路径
- `cinderx.__file__`
- `cinderx.is_initialized()`
- `cinderx.get_import_error()`
- pyperformance 路径和版本

## 完成条件

记录远程 host、宿主机目录、tmux 会话名、容器线、源码路径、解释器路径和最小 smoke 命令。
