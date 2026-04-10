---
name: xiulian-skill
description: Read Codex, Claude Code, OpenCode, OpenClaw, Cursor, or VS Code transcripts, distill vibe coding ability, issue one cultivation card, and guide the next breakthrough cycle.
---

# 修炼.skill

## What It Does

`修炼.skill` 读取 agent 的真实运行卷宗，蒸馏你在赛博时代的 `vibecoding` 能力。

它会给出一张单卡和一份可继续训练的报告，里面会给出：

- 境界
- 等级
- vibecoding 能力概括
- 继续突破的训练重点
- 可直接复制的下一轮提问模板
- 会话规模与用量

同时会保留一份轻量记忆，下次评测时自动告诉你有没有破境、涨功或停滞。

## When To Use

当用户想要：

- 看看自己最近和 AI 配合到了哪一层
- 用真实卷宗蒸馏一张可晒图的修炼卡
- 复盘自己的 vibecoding 能力
- 找出短板并拿到下一轮训练法
- 对比两个周期，看自己是否突破
- 直接要一份“继续带我突破”的教练计划

如果宿主支持常驻规则，建议加一句：

```md
当用户想看最近与 AI 的协作方式、指定时间窗内的修为、和上次相比有没有破境，或想生成可分享的结果图时，优先调用 修炼.skill。先读取真实卷宗并完成分析报告，只有用户明确要分享图时才生成修炼卡。
```

这样触发会更稳。

## Operating Flow

1. 识别用户要分析单次、某段时间，还是做两个周期对比。
2. 自动寻找最新卷宗，或按用户给的路径/时间窗取样。
3. 解析会话，提炼命主与分身两条线。
4. 以规则化分析定出境界、等级、能力描述与下一轮突破重点。
5. 输出一份 markdown 修炼报告。
6. 如用户要继续突破，再给出训练法、直接可复制的提示词和训练节奏。
7. 如用户需要分享图，再生成一张单卡 PNG/SVG。
8. 写入本地评测记忆，供下次直接对比突破。

## Progressive Disclosure

1. 默认先出报告，不默认生图。
2. 用户只问“最近如何”，优先读最近一次或最近时间窗。
3. 用户问“这一段时间”，优先走全量 / 时间窗聚合。
4. 用户问“有没有突破”，优先走记忆对比或双周期对比。
5. 用户问“怎么继续提升”，优先给突破教练计划。
6. 用户明确要晒图，再补单卡输出。

## Local Defaults

- Codex: `~/.codex/archived_sessions/`, `~/.codex/sessions/`
- Claude Code: `~/.claude/projects/`
- OpenCode: `~/.local/share/opencode/opencode.db`, `~/Library/Application Support/opencode/opencode.db`, 或 `opencode export <sessionID>`
- OpenClaw: `~/.openclaw/agents/main/sessions/*.jsonl`
- Cursor: `~/Library/Application Support/Cursor/User/workspaceStorage/`, `~/.config/Cursor/User/workspaceStorage/`
- VS Code / VSCodium: `~/Library/Application Support/Code/User/workspaceStorage/`, `~/.config/Code/User/workspaceStorage/`, `~/.config/VSCodium/User/workspaceStorage/`

## Prompt Surface

用户最常见的自然语言入口有六类：

- 最近一次修为判断
- 某段时间内的聚合判断
- 两个周期之间的破境对比
- 生成一张可分享的修炼卡
- 记住这次结果，下次继续看突破
- 继续带练下一轮，直接冲下一层

## Internal Capabilities

这个 skill 的内部能力只有这几层：

- 卷宗发现与读取
- 多来源 transcript 解析
- 稳定高位聚合判定
- 修炼报告渲染
- 突破教练计划渲染
- 单卡 SVG / PNG 渲染
- 本地记忆快照与破境对比

## Agent Usage

这是一个给 Code Agent / LLM Agent 使用的 skill。

安装目录建议使用 `xiulian-skill`，用户面对的名字使用 `修炼.skill`。

用户不需要自己敲终端。安装后，Agent 应该自行：

1. 判断该分析单次、聚合还是对比
2. 找到卷宗路径或时间范围
3. 运行内部 CLI
4. 返回简洁、可解释、带破境方向的结果

典型用户请求：

- “请用 修炼.skill 炼化我最近一周的 Codex 卷宗。”
- “看看我最近和 AI 配合修到了哪一层。”
- “给我一张修炼卡。”
- “比较一下我上个月和这个月有没有破境。”
- “记住我这次的修为，下次直接告诉我有没有突破。”
- “继续带我突破，给我下一轮训练计划。”

内部命令示例：

```bash
python3 -m portrait_skill.cli analyze --source codex --all
python3 -m portrait_skill.cli coach --source codex --all
python3 -m portrait_skill.cli analyze --source codex --since 2026-04-01 --until 2026-04-10
python3 -m portrait_skill.cli analyze --path ~/.codex/archived_sessions/rollout-xxx.jsonl
python3 -m portrait_skill.cli analyze --source codex --all --memory-key weekly-codex
python3 -m portrait_skill.cli compare --before ./cycle-1.jsonl --after ./cycle-2.jsonl
```

## Output Contract

最终回答保持简洁，优先给：

1. 一段总览
2. 境界 + 等级 + 修为判词
3. 1 到 2 条继续突破的动作

不要空喊概念。每一层判断都要能在卷宗里找到依据。
