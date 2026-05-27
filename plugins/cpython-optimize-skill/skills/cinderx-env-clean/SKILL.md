---
name: cinderx-env-clean
description: Use when CPython/CinderX lab 已存在但被污染、版本漂移、CinderX 导入异常、错误 editable install、错版本头文件、坏容器或 pyperformance env 残留。
---

# CinderX Env Clean

只清理被破坏的 CPython/CinderX 实验环境。先由 `cinderx-env-validate` 证明不可复用，再执行清理。

## 清理对象

- 错误 `editable install`、残留 wheel、旧 `cinderx.__file__` 指向。
- 旧 `build 目录`、CMake/Ninja 产物、错版本 generated headers。
- 污染 `venv`、错误 `PYTHONPATH`、坏 `LD_LIBRARY_PATH`。
- 错误 Docker 容器、挂错源码的 bind mount、残留 `pyperformance env`。
- `patchlevel.h`、`SOABI`、解释器微版本不一致造成的错版本头文件。

## 保留对象

默认保留 cache：pip cache、Docker layer、可复用源码 checkout、历史 `run.json` / `speedup.json` / 日志。要删除 cache 必须说明原因。

## 反问 Gate

- 清理会删除非 cache 产物、历史日志、`run.json`、core dump、HIR/jit.log 或用户工作目录时，必须询问。
- 同一 host/workspace 下有多个可疑环境且无法确认目标环境时，询问要清理哪一个。
- 无法判断应清理重建还是保留现场继续取证时，询问用户优先级。

## 输出

- 清理前环境指纹
- 清理了什么
- 保留了什么 cache
- 清理后需要调用的 bootstrap 步骤

不要用重新安装掩盖环境漂移；漂移原因要写清楚。
