from __future__ import annotations

from .models import Analysis, Certificate, Message

USER_BEHAVIOR_TEXT = {
    "目标清晰度": {
        "strong": "道心定得住，起手就能点明所求",
        "weak": "题眼还不够收束，时有旁枝牵神",
    },
    "上下文供给": {
        "strong": "根基交代得足，来路、边界、卷宗都摆得清楚",
        "weak": "来路与边界仍薄，分身得边做边猜",
    },
    "迭代修正力": {
        "strong": "一见偏航便肯回炉，修法不僵",
        "weak": "回炉修正偏慢，常卡在第一口气",
    },
    "验收意识": {
        "strong": "收功时肯看实证，火候稳",
        "weak": "收功火候未足，验收与回看仍薄",
    },
    "协作节奏": {
        "strong": "往返有序，气脉相接，能一路推到落地",
        "weak": "往返气机仍乱，前后呼应不够稳",
    },
}

ASSISTANT_BEHAVIOR_TEXT = {
    "执行落地": {
        "strong": "肯先落子再回话，能把差事推向成形",
        "weak": "落子偏慢，仍有停在空谈处的时刻",
    },
    "工具调度": {
        "strong": "会役使外器外法，一并催动进度",
        "weak": "役器仍少，法器与分身还未尽展",
    },
    "验证闭环": {
        "strong": "会自带回验与收功，结果更稳",
        "weak": "回验仍薄，收功时还欠一锤定音",
    },
    "上下文承接": {
        "strong": "能续住主线气脉，不易走散",
        "weak": "续脉仍有松动，长回合里易失焦点",
    },
    "补救适配": {
        "strong": "遇阻能换法换势，继续破局",
        "weak": "遇阻时转身仍慢，补漏不够及时",
    },
}

USER_XIANXIA_STRONG = {
    "目标清晰度": "道心坚定",
    "上下文供给": "根基稳固",
    "迭代修正力": "悟性渐开",
    "验收意识": "收功谨慎",
    "协作节奏": "气机相合",
}

USER_XIANXIA_WEAK = {
    "目标清晰度": "道心未定",
    "上下文供给": "根基浮动",
    "迭代修正力": "悟性未开",
    "验收意识": "收功不稳",
    "协作节奏": "气机不顺",
}

ASSISTANT_XIANXIA = {
    "执行落地": "术法落地",
    "工具调度": "驭器调度",
    "验证闭环": "收功回验",
    "上下文承接": "续脉承题",
    "补救适配": "转圜破局",
}

ABILITY_LIBRARY = {
    "L1": "只得引气试手，偶能一问一答（single-turn prompting）",
    "L2": "已知换咒会变招，开始觉察问法之力（prompt steering）",
    "L3": "可循浅法炼成小事，手上已有几分火候（task completion / prompt iteration）",
    "L4": "可沿熟路反复行功，常见差事已能稳定跑通（workflow reuse / multi-step execution）",
    "L5": "可把常用术式收束成法门，遇同类卷宗不必从头起炉（skill abstraction / reusable workflow）",
    "L6": "可先替命主行过一段路，再回呈实果（delegated execution / proactive implementation）",
    "L7": "可役使多具分身并驱法器，同炉炼化一件整差（multi-agent orchestration / tool use）",
    "L8": "可炼器亦可炼法，开始经营整套修行章法（capability design / system thinking）",
    "L9": "可入真实场域来回行功，边做边回流经验（production loop / feedback loop）",
    "L10": "可将法门传与同门，复制到团队与客户场景（team enablement / workflow transfer）",
}

IMAGE_CONCEPT_GROUPS = {
    "版式层级": ["标题", "副题", "小标题", "布局", "排版", "层级", "留白", "对齐", "间距", "框", "边框", "面板", "位置"],
    "文字可读": ["重叠", "可读", "看不清", "清晰", "字号", "字色", "颜色", "配色", "字距", "换行"],
    "修仙叙事": ["修仙", "境界", "灵根", "判词", "符箓", "修炼", "画像", "证书", "修仙小说"],
    "分享传播": ["png", "svg", "dpi", "readme", "预览", "分享", "社交", "海报", "爆款"],
    "生图约束": ["生图", "prompt", "生成", "图片", "框的位置", "最后一行", "风格", "样式"],
}

IMAGE_CONCEPT_NOTES = {
    "版式层级": "宣传图更看重一眼识别与稳定层级，标题、主字、正文和底部信息必须分明。",
    "文字可读": "用户持续强调清晰、留白和安全边距，卡片必须保证小字可读、正文不压框。",
    "修仙叙事": "世界观要贴近常见修仙小说语汇，重点是境界、功法、破境，不可乱造设定。",
    "分享传播": "这张卡既是评测结果，也是可晒图的社交物料，需优先照顾转发时的辨识度。",
    "生图约束": "如果交给模型生图，必须明确最后一行文字下方仍要保留完整安全边距。",
}


def build_analysis_insights(analysis: Analysis) -> dict[str, object]:
    return _build_insights(
        messages=analysis.transcript.messages,
        user_metrics=analysis.user_metrics,
        assistant_metrics=analysis.assistant_metrics,
        user_certificate=analysis.user_certificate,
        assistant_certificate=analysis.assistant_certificate,
        total_messages=len(analysis.transcript.messages),
        tool_calls=analysis.transcript.tool_calls,
        total_tokens=analysis.transcript.token_usage.total_tokens,
    )


def build_aggregate_insights(analyses: list[Analysis], aggregate: dict[str, object]) -> dict[str, object]:
    messages = [message for analysis in analyses for message in analysis.transcript.messages]
    return _build_insights(
        messages=messages,
        user_metrics=aggregate.get("user_metrics", []),
        assistant_metrics=aggregate.get("assistant_metrics", []),
        user_certificate=aggregate.get("user_certificate", {}),
        assistant_certificate=aggregate.get("assistant_certificate", {}),
        total_messages=int(aggregate.get("total_messages", 0) or 0),
        tool_calls=int(aggregate.get("total_tool_calls", 0) or 0),
        total_tokens=int(_as_dict(aggregate.get("token_usage")).get("total_tokens", 0) or 0),
    )


def _build_insights(
    *,
    messages: list[Message],
    user_metrics,
    assistant_metrics,
    user_certificate,
    assistant_certificate,
    total_messages: int,
    tool_calls: int,
    total_tokens: int,
) -> dict[str, object]:
    user_items = _metric_items(user_metrics)
    assistant_items = _metric_items(assistant_metrics)
    user_top, user_low = _top_and_low(user_items)
    assistant_top, assistant_low = _top_and_low(assistant_items)
    image_concepts = _image_concepts(messages)

    realm = _certificate_value(user_certificate, "level", "凡人")
    rank = _certificate_value(assistant_certificate, "level", "L1")
    ability_text = _ability_text(rank)
    user_top_name = USER_XIANXIA_STRONG.get(user_top["name"], user_top["name"])
    user_low_name = USER_XIANXIA_WEAK.get(user_low["name"], user_low["name"])
    assistant_top_name = ASSISTANT_XIANXIA.get(assistant_top["name"], assistant_top["name"])
    assistant_low_name = ASSISTANT_XIANXIA.get(assistant_low["name"], assistant_low["name"])

    verdict_lines = [
        f"观此番行迹，已至{realm}，修为列{rank}。",
        f"所长在{user_top_name}与{assistant_top_name}，{_metric_behavior(user_top['name'], 'strong', track='user')}，{_metric_behavior(assistant_top['name'], 'strong', track='assistant')}。",
        f"关隘在{user_low_name}与{assistant_low_name}，{_metric_behavior(user_low['name'], 'weak', track='user')}，{_metric_behavior(assistant_low['name'], 'weak', track='assistant')}。",
    ]
    breakthrough_lines = _merge_growth_lines(user_certificate, assistant_certificate)

    return {
        "realm": realm,
        "rank": rank,
        "ability_text": ability_text,
        "usage_line": f"{_fmt_int(total_tokens)} token · {total_messages} messages · {tool_calls} tool calls" if total_tokens else f"{total_messages} messages · {tool_calls} tool calls",
        "verdict_lines": verdict_lines,
        "breakthrough_lines": breakthrough_lines,
        "user_summary_lines": [
            f"命主当前最稳的是“{user_top_name}”，{user_top['rationale']}",
            f"拖住上限的是“{user_low_name}”，{user_low['rationale']}",
        ],
        "assistant_summary_lines": [
            f"分身当前最稳的是“{assistant_top_name}”，{assistant_top['rationale']}",
            f"最该补的是“{assistant_low_name}”，{assistant_low['rationale']}",
            f"蒸馏出的 vibecoding 修为可概括为：{ability_text}",
        ],
        "image_concepts": image_concepts,
        "report_basis_lines": [
            "单卡取材自：境界、等级、能力描述、短长板、真实会话规模与破境建议。",
            "传播层重点是：大境界字、等级色、可晒图能力判词，以及下一轮修炼方向。",
        ],
    }


def _merge_growth_lines(user_certificate, assistant_certificate) -> list[str]:
    merged: list[str] = []
    for item in _certificate_list(user_certificate, "growth_plan") + _certificate_list(assistant_certificate, "growth_plan"):
        cleaned = _xianxiaize_growth(item)
        if cleaned and cleaned not in merged:
            merged.append(cleaned)
    return merged[:2] or ["守住一条主线，下轮只修一处短板，再图破境。"]


def _xianxiaize_growth(text: str) -> str:
    cleaned = " ".join((text or "").split())
    replacements = {
        "要求 AI 说明“改了什么、怎么验、哪里还没验”": "每次收功，都把改动、回验与未尽之处交代清楚。",
        "鼓励 AI 先读仓库、跑命令、看真实日志，再给方案": "先探卷宗与来路，再起法阵，不可空谈起手。",
        "让 AI 在下一轮任务里强制执行“实现 -> 验证 -> 回报”节奏": "下轮行功只许走“落子、回验、回报”三步法。",
        "每一轮收功时，都要附上看得见的凭据": "每次收功，都要留下看得见的实证。",
        "下次闭关前，先把诉求写成“目标 + 约束 + 输出物 + 验收”四段式": "下次起手前，先写明所求、边界、产物与验收。",
        "待下一轮问答结束，再来看境界变化": "待下一轮行功毕，再观是否破境。",
    }
    for src, dst in replacements.items():
        cleaned = cleaned.replace(src, dst)
    while cleaned.endswith("。。"):
        cleaned = cleaned[:-1]
    return cleaned


def _metric_items(metrics) -> list[dict[str, object]]:
    items: list[dict[str, object]] = []
    for item in metrics:
        if hasattr(item, "name") and hasattr(item, "score"):
            items.append({"name": str(item.name), "score": int(item.score), "rationale": str(getattr(item, "rationale", ""))})
        elif isinstance(item, dict) and "name" in item:
            items.append({"name": str(item.get("name", "")), "score": int(item.get("score", 0) or 0), "rationale": str(item.get("rationale", ""))})
    return items


def _top_and_low(items: list[dict[str, object]]) -> tuple[dict[str, object], dict[str, object]]:
    if not items:
        empty = {"name": "未定", "score": 0, "rationale": "当前样本仍需继续观察。"}
        return empty, empty
    ordered = sorted(items, key=lambda item: int(item.get("score", 0)), reverse=True)
    return ordered[0], ordered[-1]


def _metric_behavior(name: str, polarity: str, track: str) -> str:
    mapping = USER_BEHAVIOR_TEXT if track == "user" else ASSISTANT_BEHAVIOR_TEXT
    return mapping.get(name, {}).get(polarity, "当前样本仍需继续观察。")


def _certificate_value(certificate, key: str, default: str) -> str:
    if isinstance(certificate, Certificate):
        return str(getattr(certificate, key, default))
    if isinstance(certificate, dict):
        return str(certificate.get(key, default))
    return default


def _certificate_list(certificate, key: str) -> list[str]:
    if isinstance(certificate, Certificate):
        value = getattr(certificate, key, [])
    elif isinstance(certificate, dict):
        value = certificate.get(key, [])
    else:
        value = []
    return [str(item) for item in value if str(item).strip()]


def _ability_text(rank: str) -> str:
    return ABILITY_LIBRARY.get(rank, "已得一门可用法门（workflow practice）")


def _image_concepts(messages: list[Message]) -> list[str]:
    text = "\n".join(message.text.lower() for message in messages if getattr(message, "role", "") == "user")
    hits: list[tuple[str, int, list[str]]] = []
    for name, keywords in IMAGE_CONCEPT_GROUPS.items():
        matched = [keyword for keyword in keywords if keyword.lower() in text]
        if matched:
            hits.append((name, len(matched), matched[:4]))
    hits.sort(key=lambda item: item[1], reverse=True)
    if not hits:
        return ["当前样本里没有额外宣发要求，这张卡主要依据真实修为、等级与破境方向生成。"]
    lines = []
    for name, _, keywords in hits[:4]:
        joined = "、".join(dict.fromkeys(keywords))
        lines.append(f"{name}：{IMAGE_CONCEPT_NOTES.get(name, '这一类要求在轨迹里被反复提及。')} 命中词包括 {joined}。")
    return lines


def _fmt_int(value: int) -> str:
    return f"{int(value):,}"


def _as_dict(value: object) -> dict[str, object]:
    return value if isinstance(value, dict) else {}
