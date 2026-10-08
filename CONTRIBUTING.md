# 贡献指南

欢迎修复示例、完善中文解释、补充离线练习和改进实战项目。提交内容应帮助学习者理解具体概念，并能按文档复现。

## 本地开发

推荐 Python 3.12，在项目根目录执行：

```bash
python -m venv .venv
```

激活环境后：

```bash
python -m pip install -e '.[all,dev]'
python -m ai_learning list --offline
python -m ai_learning check
python -m unittest discover -s tests -v
```

PowerShell 可使用 `python -m pip install -e ".[all,dev]"`。密钥写入本机 `.env`，以 [.env.example](.env.example) 为模板。

## 修改约定

- 独立教学示例放入对应 `lessons/` 主题，综合应用放入 `projects/`。
- 保持编号与课程 ID 稳定；增加或移动入口时同步课程目录与文档。
- 注释解释目的、输入输出和必要的前提，优先保持示例短小、易读。
- 使用环境变量和项目相对路径，不硬编码 API 密钥、数据库密码或本机绝对路径。
- 明确示例是否需要网络、模型密钥、MySQL 或额外依赖；模拟数据应在说明中标注。
- 为行为修复增加有意义的离线验证；自动化测试不要依赖收费模型、个人密钥或外部数据库。
- 不提交 `.env`、私人材料、会话记录、向量库、缓存、虚拟环境与编辑器配置。

课件的 `test.py` 和项目内部 `test/` 可能是需要在线服务的演示，不属于根目录自动化测试套件。请用 `python -m unittest discover -s tests -v` 执行统一离线测试。

## 提交 Issue 与 Pull Request

Bug 报告请提供 Python 与操作系统版本、课程或项目 ID、安装和运行命令、预期行为、实际行为，以及脱敏后的最小错误信息。

Pull Request 请说明修改解决的问题、具体行为变化和验证命令。涉及依赖升级时，说明对应官方来源及兼容性；涉及收费或真实服务验证时，说明覆盖范围，不要提交服务凭据。

提交前运行：

```bash
python -m ai_learning check
python -m unittest discover -s tests -v
git diff --check
```

安全问题按 [SECURITY.md](SECURITY.md) 报告。贡献代码使用本项目 [MIT License](LICENSE)；新增资料需确认来源和公开使用权限。
