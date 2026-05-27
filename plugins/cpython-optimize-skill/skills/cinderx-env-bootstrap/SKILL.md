---
name: cinderx-env-bootstrap
description: Use when 需要初始化 CPython/CinderX 实验环境、Docker 双线、CinderX editable install、CPython baseline、pyperformance、pip mirror 或容器模板。
---

# CinderX Env Bootstrap

负责从零或清理后建立 CPython/CinderX lab。远端 SSH/tmux/rsync 由 `cinderx-remote-lab-ops` 提供。

## 目标形态

- `cinderx-test`：CinderX 功能验证、HIR dump、crash 复现、调试。
- `cpython-baseline`：stock CPython / CPython JIT 与 CinderX 正式对照。
- CinderX editable install：`python -m pip install -e . --no-build-isolation --no-deps --force-reinstall`。
- pyperformance：固定源码、依赖和 worker 环境。
- pip mirror/cache：优先镜像源和已有缓存，不无限等待在线安装。

## 反问 Gate

- host、workspace、源码路径、Docker 双线或 Python 微版本缺失且无法唯一推断时，询问用户。
- 在线依赖下载异常慢时，询问继续等待、切镜像、复用 cache 或中止。
- `cinderx-test` 与 `cpython-baseline` 的目标线不明确时，询问是调试线还是正式对照线。

## 内置资源

- `templates/cpython-baseline/Dockerfile`
- `templates/cpython-baseline/docker-compose.yml`
- `templates/cinderx-test/docker-compose.yml`
- `scripts/setup.sh`
- `scripts/smoke.sh`

## 完成条件

bootstrap 后必须调用 `cinderx-env-validate` 和 `cinderx-smoke-check`，返回可复用环境句柄：host、workspace、container line、Python、CinderX commit、pyperformance 路径。
