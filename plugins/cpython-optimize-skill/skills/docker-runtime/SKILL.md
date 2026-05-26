---
name: docker-runtime
description: 在需要创建/管理 Docker 容器、挂载目录、镜像复用、双线结构选择时使用
---

# 运行时环境隔离：Docker

## 目标

在远程服务器上复用可控、可重建的运行时环境，同时保留源码挂载能力。

前提：
- 宿主机目录必须先隔离好
- 容器隔离建立在宿主机目录隔离之上

## 镜像构建规则

**禁止从外部拉取预构建镜像。** 必须使用本技能内置的 Dockerfile 从源码构建：

```bash
# 正确：用内置 Dockerfile 构建
docker compose up -d --build

# 错误：不要拉取外部镜像
docker pull xxx
```

内置模板：
- `templates/cpython-baseline/Dockerfile` — 基于openEuler 24.03 + GCC 14 + Python 3.14.3
- `templates/cpython-baseline/docker-compose.yml` — 基线线编排
- `templates/cinderx-test/docker-compose.yml` — 调试线编排（共享基线线 Dockerfile）

`cinderx-test` 的 `docker-compose.yml` 通过 `DOCKERFILE_CONTEXT` 环境变量指定 Dockerfile 所在目录，两条线共用同一个镜像。首次构建后镜像会被本地缓存，后续启动直接复用。

如果镜像已存在且不需要重建，直接 `docker compose up -d` 即可。

## 环境变量

启动容器前必须设置以下环境变量（必填项缺失时 docker compose 会报错）：

| 变量 | 必填 | 说明 |
|------|------|------|
| `CINDERX_ROOT` | 是 | CinderX 源码根目录 |
| `CPYTHON_ROOT` | baseline 必填 | stock CPython 源码目录 |
| `PYPERFORMANCE_ROOT` | 是 | pyperformance 源码目录 |
| `DOCKERFILE_CONTEXT` | 否 | Dockerfile 所在目录，默认 `../cpython-baseline` |
| `CINDERX_DIST` | 否 | CinderX wheel 目录，默认 `${CINDERX_ROOT}/dist` |
| `PYPERF_HOOK_ROOT` | 否 | pyperf env hook 目录，默认 `${CINDERX_ROOT}/scripts/arm/pyperf_env_hook` |
| `SCRIPTS_DIR` | 否 | 容器内脚本目录，默认 `./scripts` |
| `CONFIGS_DIR` | 否 | benchmark 配置目录，默认 `./configs` |
| `RESULTS_DIR` | 否 | 结果输出目录，默认 `./results` |

使用示例：

```bash
export CINDERX_ROOT=/home/user/cinderx
export CPYTHON_ROOT=/home/user/Repo/cpython
export PYPERFORMANCE_ROOT=/home/user/Repo/pyperformance
docker compose up -d --build
```

## 双线结构

| 线路 | 模板 | 用途 | 优先级 |
|------|------|------|--------|
| `cinderx-test` | `templates/cinderx-test/` | 功能验证、HIR dump、crash 复现 | 先走 |
| `cpython-baseline` | `templates/cpython-baseline/` | stock CPython vs CinderX 正式对照 | 后走 |

先走 `cinderx-test` 完成功能确认，再走 `cpython-baseline` 做正式对照。

## 推荐做法

- 宿主机提供：Docker、`docker compose`、`rsync`
- 每个 Agent 先准备独立宿主机目录
- 源码通过 `rsync` 同步到远端
- 容器通过 bind mount 直接使用源码目录
- 容器内构建和验证，宿主机主要负责同步和编排

调试约束：
- Docker 调试时优先保留一个长连接交互终端
- 不要把反复 `docker exec ...` 当成主要调试方式
- 更推荐先进入固定 shell，再在容器内持续执行命令

目录隔离约束：
- 不复用已有宿主机工作目录
- bind mount 前先确认挂载源目录是当前 Agent 自己的目录
- 结果目录、源码目录、pyperformance 目录都应避免与他人共享写入

## 脚本入口

- `scripts/setup.sh` — 容器内安装 CinderX 和 pyperformance
- `scripts/smoke.sh` — JIT 功能冒烟测试

## 优先级

1. Kunpeng Docker：兼容性主验证环境
2. Kunpeng 宿主机：最终少量关键复核
3. 本地 Docker：开发期快速回归

## 实战注意事项

- 代理不可默认写死，容器内要能自动摘除坏代理
- 容器内 `pip` 默认应切到国内镜像源，优先阿里云或华为云
- 不能只在宿主机配 `pip` 源，容器内构建和安装链路也要显式生效
- openEuler / Python 源码下载最好走国内镜像
- 初始化脚本要避免吞错误
- 首次构建要警惕过宽的包通配符把 `debuginfo` / `debugsource` 一起拉进来
- 容器和宿主机路径要尽量统一，便于挂载源码和复用命令
- `pyperformance` 源码目录必须挂到真正可安装的仓库根
- 只有自动化脚本、一次性检查或批量命令才优先 `docker exec`

推荐默认值：

```bash
export PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/
# 或
export PIP_INDEX_URL=https://repo.huaweicloud.com/repository/pypi/simple
```

在容器脚本里应确保：
- `python -m pip install ...` 能继承 `PIP_INDEX_URL`
- 隔离构建环境也能继承 `PIP_INDEX_URL`

## 网络诊断

当构建或安装过程中出现网络缓慢时，执行以下检查，**但不要自行修复**，必须将诊断结果反馈给用户并等待确认后再操作。

### 检查步骤

1. **测试代理连通性**
   ```bash
   curl -x http://host.docker.internal:7890 -o /dev/null -w "%{http_code} %{time_total}s" https://pypi.org/
   ```

2. **测试直连（绕过代理）**
   ```bash
   curl --noproxy '*' -o /dev/null -w "%{http_code} %{time_total}s" https://pypi.org/
   ```

3. **测试国内镜像**
   ```bash
   curl --noproxy '*' -o /dev/null -w "%{http_code} %{time_total}s" https://mirrors.aliyun.com/pypi/simple/
   ```

4. **检查 DNS 解析**
   ```bash
   time nslookup pypi.org
   time nslookup mirrors.aliyun.com
   ```

### 诊断结果模板

向用户报告时包含：

- 代理是否可达（是/否/超时）
- 直连速率
- 国内镜像速率
- DNS 解析耗时
- 建议方案（如：切换镜像源、关闭代理、修改 DNS 等）

**必须等用户确认后才执行任何修改操作。**
