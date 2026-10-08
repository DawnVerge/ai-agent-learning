# GitHub 发布与维护

项目仓库：[DawnVerge/ai-agent-learning](https://github.com/DawnVerge/ai-agent-learning)。维护者显示名称为 `DawnVerge`，许可证为 MIT。日常维护在已有 checkout 中提交并推送；下面的首次初始化步骤供从零创建独立项目时参考，请勿在已有仓库中重复初始化。

## 发布前检查

从本项目根目录执行：

```bash
python -m ai_learning check
python -m unittest discover -s tests -v
python -m pip check
```

阅读 README、环境变量模板与许可证，确认样本文档可以公开。不要加入 `.env`、密钥、密码、会话日志、私人 PDF、虚拟环境或生成的向量库。

本目录作为独立新项目首次初始化，只提交整理后的文件。不要复制其他仓库的 `.git`，也不要在已存在历史的目录中直接运行下面的初始化流程。

## 确认 GitHub 账号

需要安装 Git 与 GitHub CLI。

```bash
gh auth status
gh api user --jq .login
```

输出应为 `DawnVerge`。若已登录多个账号，可以使用：

```bash
gh auth switch --hostname github.com --user DawnVerge
```

尚未登录时使用 `gh auth login --hostname github.com`，完成后重新确认账号。不要把 token 粘贴到文档、聊天记录或提交内容中。

## 建立全新的本地历史

确认当前路径是 `ai-agent-learning`，且目录中没有 `.git` 后再运行：

```bash
git init -b main
git config --local user.name "DawnVerge"
```

为避免提交私人邮箱，可从当前 GitHub 账号信息生成 GitHub noreply 邮箱。

PowerShell：

```powershell
$githubUser = gh api user | ConvertFrom-Json
git config --local user.email "$($githubUser.id)+$($githubUser.login)@users.noreply.github.com"
```

Bash：

```bash
git config --local user.email "$(gh api user --jq '"\(.id)+\(.login)@users.noreply.github.com"')"
```

如 GitHub 的邮箱设置展示了其他 noreply 地址，以该账号设置页中的实际地址为准。上述 `--local` 配置只影响本项目。

## 检查首次提交

```bash
git status --short --untracked-files=all
git add .
git diff --cached --stat
git diff --cached --check
git diff --cached
```

逐项检查暂存内容后提交：

```bash
git commit -m "feat: introduce AI agent learning curriculum"
git log -1 --format=fuller
```

确认 Author 与 Committer 对应当前账号使用的名称和邮箱。若尚未推送且发现身份不正确，先修正本地 `git config`，再用 `git commit --amend --reset-author --no-edit` 更新首次提交。

## 创建公开仓库并推送

下面的命令会创建外部公开仓库并上传文件；只在准备完成、决定公开时执行：

```bash
gh repo create DawnVerge/ai-agent-learning --public --source . --remote origin --description "Learn AI applications with Python, LangChain, RAG, agents and MCP" --push
```

如果目标仓库已经存在，先检查其内容与本地远程配置，不要重复创建或强制覆盖。确认远程为空且属于当前账号后，可采用：

```bash
git remote add origin https://github.com/DawnVerge/ai-agent-learning.git
git push -u origin main
```

推送完成后打开仓库：

```bash
gh repo view DawnVerge/ai-agent-learning --web
```

检查首页、相对文档链接、许可证和 Actions 结果。日常维护使用 `git add`、`git commit` 与 `git push`；不要重复创建远程仓库。
