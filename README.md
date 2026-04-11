<div align="center">

# vibecoding.skill

> *"蒸馏你的 vibecoding 记录，看你与 AI 的协作达到了什么等级。"*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Codex](https://img.shields.io/badge/Codex-Skill-111111)](https://developers.openai.com/codex/skills)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![OpenCode](https://img.shields.io/badge/OpenCode-Ready-1991FF)](https://opencode.ai)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Ready-0F766E)](https://github.com/openclaw/openclaw)
[![Download ZIP](https://img.shields.io/badge/Download-ZIP-2EA44F)](https://github.com/dangoZhang/vibecoding.skill/archive/refs/heads/main.zip)

<br>

<img src="./assets/readme/vibecoding-card.png" alt="vibecoding.skill 效果示例" width="54%" />

<br>

它会把你与 Code Agent 的真实协作记录，蒸馏成一份能直接看懂的 vibecoding 判断。<br>
你会看到自己现在处在哪个阶段、到了 L 几、最稳的习惯是什么、最拖后腿的习惯是什么，以及下一轮该怎么继续往上练。<br>

[![Codex 来源](https://img.shields.io/badge/蒸馏来源-Codex-111111)](https://developers.openai.com/codex/skills)
[![Claude Code 来源](https://img.shields.io/badge/蒸馏来源-Claude%20Code-blueviolet)](https://claude.ai/code)
[![OpenCode 来源](https://img.shields.io/badge/蒸馏来源-OpenCode-1991FF)](https://opencode.ai/docs/skills)
[![OpenClaw 来源](https://img.shields.io/badge/蒸馏来源-OpenClaw-0F766E)](https://docs.openclaw.ai/tools/skills)
[![Cursor 来源](https://img.shields.io/badge/蒸馏来源-Cursor-222222)](https://cursor.com/docs/context/skills)
[![VS Code 来源](https://img.shields.io/badge/蒸馏来源-VS%20Code-007ACC)](https://code.visualstudio.com/docs/copilot/concepts/customization)

</div>

---

## 项目介绍

`vibecoding.skill` 是一个给 Code Agent 使用的 skill。

它关注的不是“你今天问了 AI 什么”，而是“你这一段时间究竟是怎么和 AI 一起做事的”。

同样在用 AI 写代码、改项目、推进任务，有的人还停在单轮提问，有的人已经能把上下文、工具、验收、回看、并行推进这些动作练成稳定习惯。  
`vibecoding.skill` 想做的，就是把这种差异直接从真实记录里蒸出来。

它不会让你先填问卷，也不依赖自我评价。  
它会读取你与 `Codex`、`Claude Code`、`OpenCode`、`OpenClaw` 等 Code Agent 的真实协作轨迹，再把这些轨迹压成几个最关键的问题：

- 你现在属于哪个阶段
- 你的 vibecoding 到了 `L1-L10` 的哪一级
- 你最稳定的协作习惯是什么
- 你最限制升级的短板是什么
- 如果你想去更高一级，下一轮最值得刻意练什么

围绕这件事，它默认提供三类能力：

- 蒸馏你自己，或你提供轨迹的那个人的 `vibecoding` 习惯
- 根据真实习惯对照等级表，给出阶段和等级判断
- 按目标等级给出升级建议，帮助你继续往上练

最终输出通常会落成三种形式：

- 一份 `vibecoding` 报告：阶段、等级、长板、短板、判断依据
- 一张分享卡：适合截图、发群、发朋友圈、发推
- 一轮突破建议：直接告诉你下一轮该优先补哪一个动作

如果你只想知道“我最近和 AI 协作到底到什么水平了”，它会给你一个很直接的答案。  
如果你想继续往上练，它也可以把这份结果继续往前推，变成下一轮的训练计划。  
修仙叙事保留为彩蛋，默认仍然先说人话。

---

## 安装

已实机验证下面这条安装命令可用，支持安装到 `Codex`、`Claude Code`、`Cursor`、`OpenCode`、`OpenClaw`：

```bash
npx skills add https://github.com/dangoZhang/vibecoding.skill -a codex -a claude-code -a cursor -a opencode -a openclaw
```

说明：

- `VS Code` 目前保留为记录来源，不作为 `skills` CLI 的安装宿主
- `Cursor / VS Code` 的会话记录仍然可以被这个 skill 读取和分析

装好之后，直接对 Agent 说下面这些话就可以。

---

## 你可以这样用

### 看最近一段时间

```text
帮我看看我最近 14 天和 AI 协作到了什么等级，顺便告诉我我最明显的长板和短板是什么。
```

### 模仿我的习惯

```text
根据我最近两周的真实记录，总结一下我的 vibecoding 习惯。以后再和我一起做事时，尽量按我这套节奏来。
```

### 模仿某个人的习惯

```text
我给你一份同事和 AI 的协作记录。你先总结一下他的习惯，再告诉我他为什么能稳定到 L7。
```

### 指定时间窗

```text
只看 2026-04-01 到 2026-04-10 这段时间，帮我出一份报告，再看看我和前一段时间比有没有进步。
```

### 生成分享卡

```text
把我最近一周和 AI 的协作做成一张分享卡，大字只保留阶段和等级，正文尽量压成一眼能看懂的摘要。
```

### 指导升级

```text
如果我想把自己的 vibecoding 等级再往上提一档，下一轮最值得刻意练的动作是什么？
```

### 冲目标等级

```text
如果我的目标是 L7，你结合我最近这段记录，直接告诉我还差哪些关键习惯，再给我一个能照着练的计划。
```

### 彩蛋

```text
如果有彩蛋版的话，也顺手帮我做一张修仙风格的分享卡。
```

---

## 等级对照

| 综合分段 | 境界 | 等级 | 这一层的人，不一样在哪 |
| --- | --- | --- | --- |
| 0-11 | 凡人 | L1 | 还停留在单轮提问，AI 更像临时工具 |
| 12-23 | 感气 | L2 | 已知道问法会改变结果，但稳定性还不够 |
| 24-35 | 炼气 | L3 | 能做成小任务，也会边做边补要求 |
| 36-47 | 筑基 | L4 | 常见任务能稳定推进到多步完成 |
| 48-59 | 金丹 | L5 | 开始把重复打法沉淀成可复用套路 |
| 60-69 | 元婴 | L6 | 会让 AI 先走一段，再回来收方向和结果 |
| 70-77 | 化神 | L7 | 能同时调动多 Agent 和工具并行推进 |
| 78-85 | 炼虚 | L8 | 开始搭能力、搭流程，不只是在做单次任务 |
| 86-91 | 合体 | L9 | 能把这套协作带进真实项目并持续修正 |
| 92-100 | 大乘 | L10 | 能把方法沉淀下来，稳定复制给团队 |

---

<div align="center">

MIT License © [dangoZhang](https://github.com/dangoZhang)

</div>
