# AI 术语 / 修仙词表

这份词表只约束对外叙事层。

底层代码、JSON 和兼容字段里仍保留 `portrait_skill`、`certificate`、`user_certificate`、`assistant_certificate` 等历史名字，方便兼容旧链路；对外文案统一使用 `修仙.skill`、`修仙卡`、`修炼报告`。

## 当前正式词表

| AI / 工程语 | 修仙写法 | 使用规则 |
| --- | --- | --- |
| vibe coding | 修为 / 修行手段 | 项目最大卖点，README 和报告主轴都围绕它展开 |
| agent / AI | AI / 分身 | 技术说明里保留 `AI`，报告叙事里可写“分身” |
| transcript / run history | 卷宗 / 行迹 | 用于真实记录、日志、会话轨迹 |
| session | 会话 / 一场闭关 | 聚合多轮时优先写“会话”，叙事层可写“闭关” |
| time window | 时间窗 / 某段闭关周期 | 公开用法优先写“时间窗” |
| prompt / prompting | 起手问法 / 起手法诀 | 首次出现建议保留 `prompt` |
| context | 根基 / 来路 / 边界 | 指用户提供的背景、约束、路径、环境 |
| workflow | 法门 / 章法 | 首次出现建议保留 `workflow` |
| skill | skill / 法门 | 产品名里保留 `skill`，叙事里可写“法门” |
| tool | 法器 | 报告叙事可写“法器”，技术层保留 `tool` |
| tool call | tool call / 分身落子 | 卡片底部样本规模里保留 `tool calls` |
| multi-agent orchestration | 役使多具分身 | 仅用于高等级能力描述 |
| verification | 收功 / 回验 | 与验收、测试、检查相关 |
| feedback loop | 回流 / 反馈回路 | 高等级能力描述里保留 `feedback loop` |
| model | 炉主模型 / 炉主 | 模型名本体不要翻译 |
| provider | 来路 | 只做辅助说明，不抢主叙事 |
| token | 耗材 / 灵气 | 卡片与报告里保留 `token` 数；修仙说明可配“耗材”“灵气” |
| capability design | 炼器炼法 | L8 以上能力描述可用 |
| system thinking | 经营章法 | L8 以上能力描述可用 |
| team enablement | 传法同门 | L10 场景可用 |
| memory / previous evaluation | 评测记忆 / 上次闭关记录 | 用于连续对比与破境判断 |
| compare / progress | 破境 / 涨功 / 停滞 | 对比报告专用 |

## 指标与判词映射

| 指标 | 强项写法 | 短板写法 | 含义 |
| --- | --- | --- | --- |
| 目标清晰度 | 道心坚定 | 道心未定 | 起手时能否说清所求与验收 |
| 上下文供给 | 根基稳固 | 根基浮动 | 是否把路径、边界、环境交代清楚 |
| 迭代修正力 | 悟性渐开 | 悟性未开 | 发现偏航后会不会及时回炉 |
| 验收意识 | 收功谨慎 | 收功不稳 | 会不会主动验证、回看与补证 |
| 协作节奏 | 气机相合 | 气机不顺 | 人与 AI 往返是否顺畅 |
| 执行落地 | 术法纯熟 | 术法生疏 | AI 会不会先做事再总结 |
| 工具调度 | 驭器纯熟 | 驭器未熟 | AI 会不会主动读文件、跑命令、查日志 |
| 验证闭环 | 收功圆满 | 收功有缺 | AI 会不会交代改动、验证、遗留问题 |
| 上下文承接 | 气脉贯通 | 气脉不畅 | AI 会不会续住主线，不乱跑题 |
| 补救适配 | 应变有方 | 应变不足 | 出错后会不会缩范围、换打法 |

## L1-L10 能力写法骨架

| 等级 | 修仙写法 | 保留的 AI 术语 |
| --- | --- | --- |
| L1 | 只得引气试手，偶能一问一答 | `single-turn prompting` |
| L2 | 已知换咒会变招，开始觉察问法之力 | `prompt steering` |
| L3 | 可循浅法炼成小事，手上已有几分火候 | `task completion` / `prompt iteration` |
| L4 | 可沿熟路反复行功，常见差事已能稳定跑通 | `workflow reuse` / `multi-step execution` |
| L5 | 可把常用术式收束成法门，遇同类卷宗不必从头起炉 | `skill abstraction` / `reusable workflow` |
| L6 | 可先替命主行过一段路，再回呈实果 | `delegated execution` / `proactive implementation` |
| L7 | 可役使多具分身并驱法器，同炉炼化一件整差 | `multi-agent orchestration` / `tool use` |
| L8 | 可炼器亦可炼法，开始经营整套修行章法 | `capability design` / `system thinking` |
| L9 | 可入真实场域来回行功，边做边回流经验 | `production loop` / `feedback loop` |
| L10 | 可将法门传与同门，复制到团队与客户场景 | `team enablement` / `workflow transfer` |

## 高风险 / 已废弃词

| 词 | 状态 | 原因 |
| --- | --- | --- |
| 画像 + 证书 双卡 | 已废弃 | 当前产品统一为一张 `修仙卡` |
| 能力画像 / AI 协作能力证书 | 已废弃 | 属于旧叙事，当前统一并入单卡 |
| 回收 | 禁用 | 语义不清，和项目目标无关 |
| 乱造门派、灵兽、神兵设定 | 禁用 | 用户明确要求贴近常见修仙小说语汇 |
| 把 `token`、`prompt`、`workflow`、`tool call` 全部硬翻译掉 | 禁用 | 会损失技术可信度 |
| 公开卡片展示自编评分数字 | 禁用 | 当前外显只给境界、等级和自然语言能力判断 |

## 兼容层保留词

这些词还会留在代码里，但不建议出现在对外宣传里：

- `portrait_skill`
- `certificate`
- `user_certificate`
- `assistant_certificate`

它们只是兼容旧命名，不代表当前品牌叙事。
