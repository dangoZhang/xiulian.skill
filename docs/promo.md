# 宣发分析与宣传帖

目标只保留三件事：

- 蒸馏你的 `vibecoding` 能力
- 给出一张可晒的分享卡
- 让你下一轮继续提升，并看见变化

## 同类项目在怎么赢

- `vercel-labs/skills` 目前约 `13.5k stars`。README 第一屏直接写 “The CLI for the open agent skills ecosystem”，下一行就是 “Supports OpenCode, Claude Code, Codex, Cursor, and 41 more”，然后立刻给 `npx skills add`。这类仓库赢在分发 friction 低。
- `anthropics/skills` 目前约 `114k stars`。它先用一句话解释 “Skills are folders of instructions, scripts, and resources...”，再马上给 Claude Code / Claude.ai / API 的真实入口。官方信任感和入口清晰度都非常强。
- Vercel 在 2026-02-20 的 `Skills Night` 里给出过生态规模：`69,000+ skills`、`2 million skill CLI installs`。这说明“可复用 agent 能力包”本身就有很强增长势能。
- Vercel 自己的 agent eval 也很直白：`Skill (default behavior)` 通过率 `53%`，加显式指令后到 `79%`，`AGENTS.md docs index` 到 `100%`。结论很明确，skill 要配一条常驻触发语。
- Cursor 产品页已经把 skills 写成真实入口：`discover and run specialized prompts and code`。VS Code 文档则明确把 skills 定义为 `package multi-step capabilities`，并说明任务匹配时会按需加载。用户会期待“装完就能直接叫出来”，不接受一长段手工教程。

## 对 vibecoding.skill 的直接要求

- 第一屏必须先放结果图，先让人想试。
- 第二屏只讲一句话卖点，不讲散文。
- 明确区分“支持安装的宿主”和“支持读取的卷宗来源”。
- 明确支持“全量会话”与“指定时间窗”，并说明默认取稳定高位，不吃单次极端值。
- 给出能直接复制的自然语言用法，少给底层命令。
- 给宿主一条常驻触发语，减少 skill 被漏调的概率。
- 修仙味可以浓，技术词不能丢；真实性来自卷宗、时间窗、token、模型、记忆对比。

## 这一轮已经补上的点

- 新增了 [AI 术语 / 修仙词表](./lexicon.md)，把正式词、废弃词和兼容层分开。
- README 里把“宿主安装”和“卷宗来源”拆开写，避免再把 Cursor / VS Code 讲混。
- README 里加入了时间窗示例，强调可以读全部会话，也可以只读某段时间。
- README 和 SKILL 都加入了宿主常驻引导语，减少 skill 不触发的问题。
- README 的安装方式改成优先 `npx skills add`，更贴近当前爆款 skill 项目的实际分发方式。

## 建议放进宿主的常驻一句

可放进 `AGENTS.md`、`CLAUDE.md`、Copilot instructions 或类似的常驻规则里：

```md
当用户想看最近与 Code Agent 的协作方式、指定时间窗内的水平、和上次相比有没有提升，或想生成可分享的结果图时，优先调用 vibecoding.skill。先读取真实轨迹并判断阶段与等级；只有用户明确说想要修仙彩蛋时才生成修仙版卡片。
```

## 宣传帖

### GitHub 发布帖

做了个 `vibecoding.skill`。

它不看自述，只读 Codex、Claude Code、OpenCode、OpenClaw、Cursor、VS Code 的真实交互轨迹，把你这一段时间的 `vibecoding` 习惯蒸馏成一张分享卡。

你会直接看到：

- 现在处在哪个阶段
- 当前是 L 几
- 这层人到底强在哪
- 下一轮该怎么提升

还能记住上次评测，下次直接告诉你是提升、停滞，还是明显进阶。

适合拿来晒，也适合拿来复盘。

### X / 即刻短帖

做了个很实用的东西：`vibecoding.skill`

它会读你真实的 code agent 轨迹，蒸馏你最近的 `vibecoding` 能力，再给你一张分享卡。

不靠自评和问卷，直接从真实会话里炼出来。

而且它会记住上次结果。下次再测，直接看你有没有明显提升。

### 小红书 / 朋友圈长帖

最近把一个一直想做的 idea 做出来了，叫 `vibecoding.skill`。

我越来越觉得，大家和 AI 协作的关键差距，在于有没有形成稳定的 vibecoding 路数。有人还停在单轮问答，有人已经能把 workflow、tools、multi-agent orchestration 跑成稳定方法。

所以我做了个 skill，直接去读真实轨迹，不靠自述，把一段时间里的协作方式压成一张分享卡。上面会写你当前的阶段、L1-L10 等级、能力判断、下一步建议，还会带上 token、样本规模、模型信息这些真实依据。

更重要的是，它会记住你上一次的结果。过一周、一个月，再测一次，就能直接看到自己有没有提升、停滞，还是明显进阶。

我现在最喜欢它的一点，是它把“和 AI 协作”从一句空话，变成了一个能持续复盘、持续迭代、还能直接晒出来的东西。

## 小红书发布版

### 第一版

标题：

`我做了个 skill，能从真实记录里看出你的 vibecoding 到了 L 几`

正文：

最近做了个我自己很想长期用的东西：`vibecoding.skill`

它做的事很直接：

- 读你和 Code Agent 的真实协作记录
- 蒸馏出你这段时间的 vibecoding 习惯
- 给出阶段、L1-L10 等级、长板、短板
- 再告诉你下一轮最该怎么练

我想做它，是因为我越来越觉得，大家和 AI 的差距，很多时候不在模型本身，而在协作方式。

有人还停在“想到什么问什么”。
有人已经会把上下文、工具、验收、回看，慢慢练成稳定 workflow。

`vibecoding.skill` 想做的，就是把这种差距直接蒸出来。

它不靠问卷，也不靠自评。
它直接看真实轨迹，所以最后出来的结果会带样本规模、token、模型这些依据。

目前它能做 3 件事：

1. 总结你自己的 vibecoding 习惯
2. 对照等级表判断你现在在哪一层
3. 如果你想冲到下一个等级，它会直接告诉你先练什么

我还给它做了一张适合分享的卡。

如果你只想知道“我最近和 AI 协作到底到什么水平了”，它会直接给答案。
如果你想继续进步，它也能继续当你的突破教练。

我自己觉得最有意思的一点是：
过一段时间再测一次，它能直接对比你和上一次有没有升级。

如果你也在高频和 Codex、Claude Code、OpenCode 这类 Code Agent 一起写东西，应该会懂这种“终于能把协作方式量化出来”的感觉。

### 修改后发布版

标题：

`你和 AI 到底会不会协作？我做了个 skill，直接从真实记录里测出来`

正文：

最近做了个很上头的小项目：`vibecoding.skill`

它会直接去读你和 Code Agent 的真实协作记录，然后给你一张结果卡：

- 你现在在哪个阶段
- 你的 vibecoding 是 L 几
- 你最稳的习惯是什么
- 你最拖后腿的习惯是什么
- 下一轮最值得刻意练哪一步

我做它的原因很简单。

很多人都在说自己“会用 AI”，但这个说法太虚了。
真正拉开差距的，往往是你会不会给上下文、会不会逼 AI 验证、会不会拆任务、会不会让它真的动手。

所以我想做一个更直接的东西：
不问你，不猜你，直接看真实记录。

看完以后，它会把这段时间的协作方式蒸成一个结果：

- 阶段
- 等级
- 判断摘要
- 突破方向

如果你愿意，还可以继续往下问：

- “蒸馏一下我最近的 vibecoding 习惯”
- “按我这套习惯以后继续和我协作”
- “如果我想冲到 L7，还差哪些关键习惯”
- “给我一张能发朋友圈/群聊的小卡片”

我自己最喜欢的是，它不是一次性的。

这周测完，过几天再测一次，它会告诉你：
你到底是在稳定进步，还是只是偶尔状态好。

对现在这种天天和 Code Agent 一起做事的人来说，我觉得这个东西会比“今天试了哪个 prompt”更有复盘价值。

如果你也在用 Codex、Claude Code、OpenCode 这些工具，可以试试看。

建议配图：

- 第一张：分享卡成品
- 第二张：README 首屏或报告截图
- 第三张：等级表局部

建议标签：

`#AI编程 #CodeAgent #Codex #ClaudeCode #VibeCoding #效率工具 #独立开发 #小众软件 #程序员日常`

## 宣发时要避免

- 先讲世界观，再讲结果图。
- 把 README 写成教程长文。
- 用一堆 badge 占掉首屏，却不给结果。
- 把“安装 skill”与“读取卷宗来源”讲混。
- 对外宣传还在讲旧的双卡、画像、证书。
- 只讲修仙，不给 token、模型、时间窗、会话数这些真实依据。

## 参考

- [vercel-labs/skills](https://github.com/vercel-labs/skills)
- [anthropics/skills](https://github.com/anthropics/skills)
- [Vercel: AGENTS.md outperforms skills in our agent evals](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)
- [Vercel: Skills Night: 69,000+ ways agents are getting smarter](https://vercel.com/blog/skills-night-69000-ways-agents-are-getting-smarter)
- [Cursor Product](https://cursor.com/product)
- [VS Code Customization](https://code.visualstudio.com/docs/copilot/concepts/customization)
