---
name: remote-environment
description: 在需要连接远程服务器、配置 SSH、创建独立宿主机目录、同步代码时使用
---

# 环境获取：SSH 与 tmux

## 目标

稳定接入远程优化环境，并尽量复用连接，不重复开新会话。

注意：
- SSH 只是进入远程宿主机
- 对 CPython/CinderX 主工作流来说，默认下一步应进入 Docker 容器隔离
- 不要把"SSH 上去后直接在裸机做编译/测试"当作默认路径

## 基本流程

1. 配置 SSH 别名，固定主机名、用户和密钥
2. 先确认 SSH 能稳定登录
3. 登录后先确认当前 Agent 的宿主机目录是否独立
4. 再用 `rsync` 同步代码仓到远端独立宿主机目录
5. 优先创建或复用 `tmux` 会话
6. 进入目标 Docker 容器或先启动对应容器
7. 长任务统一在 `tmux` 和容器内执行
8. 断线后优先 `tmux attach`，不要重建上下文

## 推荐习惯

- 每个 Agent 使用独立宿主机目录，例如按项目名、分支名或 Agent 名隔离
- 每个项目固定一个 `tmux` 会话名
- 构建、日志、benchmark、调试分开 pane 或 window
- 重要远端路径写进文档，不靠记忆
- bind mount 前先确认宿主机目录不会覆盖已有工作目录
- 代码同步默认优先 `rsync`，不要手工逐文件拷贝
- 如果远端还没安装 `rsync`，先提醒用户安装，再开始同步

## 远程命令输出契约

每条非交互式远程命令第一次执行时，就要能回答：

- stdout/stderr 在哪里看
- exit status 是多少
- 长任务日志文件在哪里
- 如果进了 `tmux`，pane/window 名称是什么

推荐模式：

```bash
ssh <host> 'bash -lc '"'"'set -o pipefail; <command> 2>&1; status=$?; printf "\n[exit status=%s]\n" "$status"; exit "$status"'"'"''
```

长任务默认进 `tmux`，并用 `tee` 固化输出：

```bash
<long-command> 2>&1 | tee logs/<task>.log
tail -n 80 logs/<task>.log
```

如果出现“无输出”，先查 exit status、日志文件、`tmux capture-pane`、进程状态和磁盘/网络状态。不要为了补输出盲目重复执行同一条可能有副作用的构建、安装或 benchmark 命令。

## 异常耗时处理

区分正常长编译和异常网络卡顿：

- 编译类任务：只要 CPU/日志持续变化，可以继续观察并定期汇报
- 网络类任务：`pip`、`git clone/fetch`、源码下载、包安装长时间无新增输出时，优先怀疑 DNS、代理、镜像源或连接问题
- 远程网络命令尽量带 `timeout`、进度输出、镜像源或缓存策略
- 超过预期仍无进度时，先诊断代理、DNS、镜像连通性和当前进程，再向用户报告并询问用户是继续等待、换镜像、跳过，还是由用户处理环境

不要在网络卡顿时无限等待，也不要在没有诊断结果时擅自改代理或全局网络配置。

## 最小命令

```bash
ssh <host>
mkdir -p ~/work/<project>-<agent>
exit
rsync -a --delete ./ <host>:~/work/<project>-<agent>/
ssh <host>
tmux new -s cinderx
tmux attach -t cinderx
```

## 进入远程后的默认动作

优先顺序：
1. 确认宿主机目录独立
2. 先确认 SSH 登录和远端权限正常
3. 再确认代码已通过 `rsync` 同步到当前 Agent 目录
4. 确认 Docker 可用
5. 进入或启动目标容器
6. 再开始编译、测试、调试

## 代码同步约定

- 远端主工作流默认使用 `rsync` 同步代码仓
- `rsync` 比手工复制更适合大仓库和频繁迭代
- 同步目标必须是当前 Agent 自己的宿主机目录
- 只有在 `rsync` 不可用且用户明确同意时，才退回其他同步方式
