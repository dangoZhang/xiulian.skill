---
name: vibecoding-skill
description: Distill vibecoding ability from real code-agent traces, judge stage and level, and optionally render a xianxia easter-egg card.
---

# vibecoding.skill

## What It Does

`vibecoding.skill` 默认先做一件事：

把真实协作轨迹翻译成一份人能立刻看懂的 `vibecoding` 判断。

基础输出只有四层：

- 阶段
- 等级
- 一段人话判断
- 下一步

如果用户继续追问，再按需补：

- 为什么是这一层
- 一张分享卡
- 下一轮怎么突破

## Positioning

这个 skill 的主语是 `vibecoding`。

修仙只是彩蛋层，不是默认判断层。  
默认回答优先用常见 AI / Agent 语言，把能力、短板和突破动作说清楚。  
只有用户明确要求“境界感”“修仙味”时，才切换到修仙叙事。

## When To Use

当用户想要：

- 看看自己最近和 AI 协作到了什么阶段
- 判断自己是“还在试”还是已经形成稳定工作流
- 复盘最近一轮为什么推进顺 / 为什么总卡住
- 拿到下一轮可以立刻照做的突破建议
- 生成一张可分享的 vibecoding 卡

## Progressive Disclosure

1. 默认先读最近一次或用户指定时间窗。
2. 默认先输出人话版判断：现在在哪一层，最强项是什么，最短板是什么，下一步先补什么。
3. 用户问“为什么”，再补依据和拆解。
4. 用户问“给我一张卡”时先给默认分享卡。
5. 用户问“怎么提升”，再补突破建议；明确想要修仙风格时再给彩蛋版。

## Operating Flow

1. 判断是单次、时间窗聚合，还是双周期对比。
2. 自动寻找可用轨迹并完成解析。
3. 先用常见 AI 语言概括能力层级。
4. 再把结果投影成境界与等级。
5. 用户需要修仙彩蛋时，再切到修仙词汇表和修仙卡模板。

## Language Rules

- 默认不用硬扯修仙。
- 默认先说人话，再加修仙映射。
- `prompt`、`tool use`、`verification`、`context`、`workflow` 这类词优先保留常见 AI 说法。
- 修仙叙事只在标题、判词、分享卡和少量比喻里出现。
- 一旦修仙说法开始妨碍理解，立即退回人话。

## Good Prompts

- “看看我最近两周和 Code Agent 协作到了什么水平。先用人话说。”
- “别只告诉我等级。告诉我这轮最拖后腿的是哪一个习惯。”
- “帮我把最近 10 天的轨迹炼成一张分享卡，大字只保留阶段和等级。”
- “如果我想从 L4 冲到 L5，下一轮最值得补的一个动作是什么？”

## Output Contract

默认回答优先给：

1. 一段总览
2. 阶段 + 等级
3. 一段人话判断
4. 一条最关键的突破方向

用户继续追问时，再补更长的拆解、词汇映射和分享卡。
