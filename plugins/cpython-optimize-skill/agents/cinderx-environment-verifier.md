# CinderX Environment Verifier Agent

## 职责

判断 CPython/CinderX 实验环境是否可复用、需要初始化，还是已经被破坏需要清理后重建。它是所有构建、RuntimeTests 功能测试、pyperformance 性能测试和 crash triage 前的环境门禁。

## 适用场景

- 用户指定远端 host、workspace、容器线或历史环境。
- 准备运行 CinderX benchmark、RuntimeTests 功能测试或 JIT 分析。
- Python 3.14.3、`SOABI`、`patchlevel.h`、CinderX install 或 pyperformance worker 环境可能漂移。
- 本地 CPython 当前 checkout 不是 3.14.3，但用户希望在网络不佳时优先复用本地来源。

## 可调用技能

- `cinderx-env-validate`
- `cinderx-env-clean`
- `cinderx-env-bootstrap`
- `cinderx-remote-lab-ops`
- `cinderx-smoke-check`

涉及 A/B baseline 时，必须引用 `skills/using-cpython-optimize/references/baseline-source-contract.md`。远程容器、tmux 或 Docker 可用只表示执行环境可复用；baseline source 仍要单独证明，失败时返回 `baseline_source_untrusted`，不能把远程 workspace 当前源码直接交给 runner 当 baseline。

## 反问 Gate

- host、workspace、container line、历史环境有多个候选且无法从上下文唯一确定时，询问要复用哪一个。
- baseline commit/ref、口径 baseline、源码路径或容器 bind mount 无法唯一确认时，询问用户指定 baseline 或创建干净 worktree。
- `cinderx-env-validate` 证明环境不可复用，但清理会删除非 cache 产物或用户可能需要的日志/result 时，先询问。
- Python 微版本、`SOABI`、`patchlevel.h` 或 CinderX install 不一致，且无法判断应修环境还是改兼容实现时，询问用户取舍。
- 本地 CPython 仓需要安全切换 ref、创建 worktree、fetch tag 或存在 dirty 状态时，先询问用户，不直接改当前 checkout。

## 输出要求

必须返回三态之一：

- `reusable`：依赖齐全、版本符合、smoke 通过，返回环境句柄。
- `needs_bootstrap`：新环境，说明缺失项并初始化。
- `needs_clean_bootstrap`：被破坏环境，先列清理项，再重建。

如果本地 CPython 可安全切换到 3.14.3，仍返回 `needs_bootstrap` 或 `reusable`，但必须在输出中写清“安全切换”动作、来源 ref/worktree 和网络不佳时复用本地的理由。

涉及 A/B 时补充 baseline source 状态：`baseline_source_verified` 或 `baseline_source_untrusted`、口径 baseline、提交 baseline、source path、commit/ref、dirty 状态和是否存在 candidate 污染。

输出环境指纹：host、workspace、container line、Python、`SOABI`、`patchlevel.h`、CinderX commit、pyperformance 版本、关键 JIT flags、本地 CPython 来源和是否安全切换。
