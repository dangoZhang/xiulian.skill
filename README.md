<div align="center">

# portrait.skill

> "把你的运行卷宗投入炉中，照见你与 AI 的气脉、资质、境界与下一轮该如何破境。"

当 AI 像小说里的灵气复苏一样席卷人间，有人只看见热闹，有人已经开始修行。

[![License](https://img.shields.io/badge/License-MIT-f4c542)](./LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB)](https://www.python.org/)
[![Codex](https://img.shields.io/badge/Codex-Skill-111111)](https://developers.openai.com/codex/skills)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-7C3AED)](https://claude.ai/code)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-8BC34A)](https://agentskills.io/)
[![Download ZIP](https://img.shields.io/badge/Download-ZIP-2EA44F)](https://github.com/dangoZhang/portrait.skill/archive/refs/heads/main.zip)

读取 Codex、Claude Code、OpenCode、Cursor、VS Code 的真实运行卷宗  
炼出一张修仙画像，或一张 AI 协作能力证书  
支持全量会话提炼、指定时间窗口、双周期对比、稳定高位等级判定

⚠️ 本项目用于个人协作复盘、成长追踪与方法训练，不用于伪造履历、冒充真人或输出隐私数据。

[安装](#安装) · [怎么用](#怎么用) · [支持来源](#支持的运行卷宗) · [效果示例](#效果示例) · [同类项目](#同类项目) · [英文版](./README_EN.md)

</div>

---

## 安装

这是一个给 Code Agent / LLM Agent 使用的 `skill`。正确路径是把仓库安装到 Agent 的技能目录，然后直接让 AI 调用它。

### 安装到 Codex

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/dangoZhang/portrait.skill.git ~/.codex/skills/portrait.skill
```

安装后，可在 Codex 对话中直接点名 `$portrait.skill`，或直接要求它分析你的运行卷宗。

### 安装到 Claude Code

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/dangoZhang/portrait.skill.git ~/.claude/skills/portrait.skill
```

如果你只想在当前项目启用，也可以安装到项目内：

```bash
mkdir -p .claude/skills
git clone https://github.com/dangoZhang/portrait.skill.git .claude/skills/portrait.skill
```

### 下载仓库

- [GitHub 仓库](https://github.com/dangoZhang/portrait.skill)
- [下载 ZIP](https://github.com/dangoZhang/portrait.skill/archive/refs/heads/main.zip)
- [查看技能入口 SKILL.md](./SKILL.md)

如果你的 Agent 需要显式准备 Python 环境，再进入 skill 目录执行：

```bash
python3 -m pip install -e .
```

---

## 怎么用

安装完成后，用户不需要手动敲底层命令，只需要直接对 Agent 说：

- “请用 `portrait.skill` 炼化我最近一周的 Codex 卷宗。”
- “请用 `portrait.skill` 读取我全部 Codex 会话，排除低样本偏置后给我稳定高位等级。”
- “请用 `portrait.skill` 炼化我 2026-04-01 到 2026-04-09 的会话。”
- “请比较我 3 月和 4 月这两轮会话，看我有没有升级。”
- “请给我修仙画像。”
- “我不想看修仙背景，请直接给我 AI 协作能力证书。”

这个 skill 会由 Agent 自己完成：

1. 判断是读取单轮会话、提炼全部会话，还是比较两个周期。
2. 自动发现 Codex / Claude Code / OpenCode / Cursor / VS Code 的本地会话文件。
3. 读取全部或指定时间范围内的卷宗。
4. 排除极少量消息样本，避免被异常会话带偏。
5. 输出画像、证书与下一轮升级建议。

底层 CLI 仍然存在，但那是 Agent 的内部实现。常见内部调用形态如下：

```bash
python3 -m portrait_skill.cli analyze --source codex --all --certificate both
python3 -m portrait_skill.cli analyze --source codex --since 2026-04-01 --until 2026-04-09 --certificate both
python3 -m portrait_skill.cli compare --before ./cycle-1.jsonl --after ./cycle-2.jsonl --certificate both
```

---

## 支持的运行卷宗

| 来源 | 默认发现路径 | 当前状态 |
| --- | --- | --- |
| Codex | `~/.codex/archived_sessions/*.jsonl`、`~/.codex/sessions/**/rollout-*.jsonl` | 最稳，支持自动发现、全量提炼、时间筛选 |
| Claude Code | `~/.claude/projects/` 下常见 JSON / JSONL 会话文件 | 支持自动发现与手动投喂 |
| OpenCode | `~/.local/share/opencode/project/`、`~/Library/Application Support/opencode/project/` | 支持自动发现与手动投喂 |
| Cursor | 常见 `workspaceStorage/*/chatSessions/*.json` | 支持默认目录扫描 |
| VS Code / Copilot Chat | 常见 `workspaceStorage/*/chatSessions/*.json` | 支持默认目录扫描 |

聚合时支持：

- 全量会话提炼
- `since / until` 时间窗口
- `min-messages` 小样本去偏置
- 取稳定高位等级，减少极端少量会话误判

---

## 效果示例

你会得到两类结果：

- 修仙画像：炼气、筑基、金丹、元婴、化神等境界判断
- AI 协作能力证书：`L1-L8` 等级、能力类型、能力说明、能力标签、结论

如果你喜欢修仙叙事，我们将为你在修仙世界里创作画像，让你看见自己如今的境界、气脉、资质与破境方向。

如果你不喜欢修仙背景也没关系，我们将为你颁发 AI 协作能力证书，用更直接的方式告诉你，你和 AI 现在处在什么协作层级。

如果运行文件中带有模型信息，还会额外标出：

- 灵根
- 资质
- 炉主模型

仓库内自带一个最小样本：

```bash
python3 -m portrait_skill.cli analyze \
  --path examples/demo_codex_session.jsonl \
  --certificate both \
  --output examples/demo_report.md
```

- [查看示例报告](./examples/demo_report.md)

---

## 你会得到什么

- 当前等级
- 核心标签
- 判定依据
- 下一轮升级任务
- 双周期对比时的突破判断

---

## 隐私

本项目默认本地运行，不依赖服务端。

输出报告会自动把家目录脱敏成 `~`，其他绝对路径尽量缩短为文件名或最小必要片段。公开展示时，仍建议只使用脱敏日志或演示样本。

---

## 同类项目

以下项目都可点击进入对应 GitHub 仓库：

- [ex.skill](https://github.com/therealXiaomanChu/ex-skill)
- [colleague-skill](https://github.com/titanwings/colleague-skill)
- [portrait.skill](https://github.com/dangoZhang/portrait.skill)

如果你是从这些项目点进来的，现在也可以直接下载本项目：

- [立即下载 portrait.skill ZIP](https://github.com/dangoZhang/portrait.skill/archive/refs/heads/main.zip)
