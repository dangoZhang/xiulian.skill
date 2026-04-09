from __future__ import annotations

from collections import Counter
from typing import Iterable

from .models import Analysis, Certificate, Message, MetricScore

ASSISTANT_BEHAVIOR_TEXT = {
    "执行落地": {
        "strong": "能把任务往实现上推，不只停在总结",
        "weak": "落到实现的速度还不够快",
    },
    "工具调度": {
        "strong": "会主动调度外部能力推进任务",
        "weak": "外部能力使用还不够主动",
    },
    "验证闭环": {
        "strong": "会把验证和结果确认一起推进",
        "weak": "验证动作偏少，结果确认还不够主动",
    },
    "上下文承接": {
        "strong": "能承接关键上下文，较少跑偏",
        "weak": "承接上下文还不够稳",
    },
    "补救适配": {
        "strong": "遇到阻力还能转向补救，继续推进",
        "weak": "遇到阻力时补救还不够快",
    },
}

USER_BEHAVIOR_TEXT = {
    "目标清晰度": {
        "strong": "所求明确，轻重先后都说得清楚",
        "weak": "所求仍散，轻重先后还未理顺",
    },
    "上下文供给": {
        "strong": "前因后果交代得更全，来龙去脉都备得齐",
        "weak": "前因后果交代仍少，来龙去脉还不够全",
    },
    "迭代修正力": {
        "strong": "见势不对便肯回身修正，不急着一条路走到底",
        "weak": "修正还不够勤，常常停在第一轮",
    },
    "验收意识": {
        "strong": "每到收功时都肯细看结果，不轻易草草翻过",
        "weak": "收功时看得还不够细，结果尚未盯紧",
    },
    "协作节奏": {
        "strong": "往返有序，彼此呼应，推进时不乱",
        "weak": "步调仍乱，前后呼应还不够稳",
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

ASSISTANT_LABELS = {
    "执行落地": "执行推进",
    "工具调度": "调度能力",
    "验证闭环": "结果确认",
    "上下文承接": "上下文承接",
    "补救适配": "补救适配",
}

IMAGE_CONCEPT_GROUPS = {
    "版式层级": ["标题", "副题", "小标题", "布局", "排版", "层级", "留白", "对齐", "间距", "框", "边框", "面板", "位置"],
    "文字可读": ["重叠", "可读", "看不清", "清晰", "字号", "字色", "颜色", "配色", "字距", "换行"],
    "修仙叙事": ["修仙", "境界", "灵根", "判词", "符箓", "修炼", "画像", "证书"],
    "证书表达": ["等级", "能力证书", "能力", "高级", "简练", "非修仙", "判词"],
    "导出发布": ["png", "svg", "dpi", "readme", "预览", "分享", "社交", "海报"],
    "生图约束": ["生图", "prompt", "生成", "图片", "框的位置", "最后一行", "风格", "样式"],
}

IMAGE_CONCEPT_NOTES = {
    "版式层级": "持续强调标题、判词、底部信息与信息框的层级关系，需要留白、对齐和稳定边界。",
    "文字可读": "反复要求字号、字色、换行和边界安全距离，核心诉求是清晰、不重叠、不压框。",
    "修仙叙事": "修仙画像要用常见网文修仙语汇，重点写境界、判词、破境之法，避免自造设定。",
    "证书表达": "证书必须走非修仙叙事，保留等级、能力、摘要和真实用量，适合直接分享。",
    "导出发布": "预览图要优先导出高质量 PNG，用于 README 展示和社交传播。",
    "生图约束": "生图 prompt 需要明确所有边框和信息框都必须落在最后一行文字下方，并保留安全边距。",
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

    user_level = _certificate_value(user_certificate, "level", "凡人")
    assistant_level = _certificate_value(assistant_certificate, "level", "L1")
    assistant_ability = _assistant_ability(_certificate_persona_subtitle(assistant_certificate), assistant_level)

    user_card_lines = [
        f"照此行迹，已至{user_level}之境。",
        f"{USER_XIANXIA_STRONG.get(user_top['name'], user_top['name'])}已成气候，{_metric_behavior(user_top['name'], 'strong', track='user')}。",
        f"{USER_XIANXIA_WEAK.get(user_low['name'], user_low['name'])}未稳，{_metric_behavior(user_low['name'], 'weak', track='user')}。",
        f"此番 {total_messages} 条对话，{tool_calls} 次分身，耗去 {_fmt_int(total_tokens)} 枚灵气。",
    ]
    assistant_card_lines = [
        f"{ASSISTANT_LABELS.get(assistant_top['name'], assistant_top['name'])}更稳，{_metric_behavior(assistant_top['name'], 'strong', track='assistant')}。",
        f"{ASSISTANT_LABELS.get(assistant_low['name'], assistant_low['name'])}仍需补强，{_metric_behavior(assistant_low['name'], 'weak', track='assistant')}。",
        f"样本来自 {total_messages} messages、{tool_calls} tool calls。",
    ]

    return {
        "user_summary_lines": [
            f"当前更稳的是“{USER_XIANXIA_STRONG.get(user_top['name'], user_top['name'])}”，{user_top['rationale']}",
            f"眼下拖住上限的是“{USER_XIANXIA_WEAK.get(user_low['name'], user_low['name'])}”，{user_low['rationale']}",
        ],
        "assistant_summary_lines": [
            f"AI 当前更擅长“{ASSISTANT_LABELS.get(assistant_top['name'], assistant_top['name'])}”，{assistant_top['rationale']}",
            f"AI 当前最需要补的是“{ASSISTANT_LABELS.get(assistant_low['name'], assistant_low['name'])}”，{assistant_low['rationale']}",
            f"当前等级可概括为：已能{assistant_ability}。",
        ],
        "image_concepts": image_concepts,
        "report_basis_lines": [
            "修仙画像取自：境界、协作长处、关隘、会话规模、灵根资质与破境建议。",
            "能力证书取自：等级、能力范围、强项短板，以及 messages、tool calls、token。",
        ],
        "user_card_lines": user_card_lines,
        "assistant_ability_line": f"已能{assistant_ability}。",
        "assistant_card_lines": assistant_card_lines,
        "assistant_usage_meta": f"{total_messages} messages · {tool_calls} tool calls",
        "assistant_usage_text": f"{_fmt_int(total_tokens)} token" if total_tokens else "token 未显",
    }


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
    value = mapping.get(name, {}).get(polarity)
    return value or "当前样本仍需继续观察"


def _certificate_value(certificate, key: str, default: str) -> str:
    if isinstance(certificate, Certificate):
        return str(getattr(certificate, key, default))
    if isinstance(certificate, dict):
        return str(certificate.get(key, default))
    return default


def _certificate_persona_subtitle(certificate) -> str:
    if isinstance(certificate, Certificate):
        return certificate.persona.subtitle
    if isinstance(certificate, dict):
        return str(_as_dict(certificate.get("persona")).get("subtitle", ""))
    return ""


def _assistant_ability(subtitle: str, level: str) -> str:
    if subtitle:
        cleaned = " ".join(subtitle.split())
        if cleaned.startswith("已经能"):
            cleaned = cleaned[3:]
        elif cleaned.startswith("能"):
            cleaned = cleaned[1:]
        elif cleaned.startswith("开始把"):
            cleaned = "把" + cleaned[3:]
        elif cleaned.startswith("开始拥有"):
            cleaned = "拥有" + cleaned[4:]
        elif cleaned.startswith("开始"):
            cleaned = cleaned[2:]
        cleaned = cleaned.replace("workflow", "流程").replace("skill", "技法").replace("agent", "分身")
        return cleaned
    return level


def _image_concepts(messages: list[Message]) -> list[str]:
    text = "\n".join(message.text.lower() for message in messages if getattr(message, "role", "") == "user")
    hits: list[tuple[str, int, list[str]]] = []
    for name, keywords in IMAGE_CONCEPT_GROUPS.items():
        matched = [keyword for keyword in keywords if keyword.lower() in text]
        if matched:
            hits.append((name, len(matched), matched[:4]))
    hits.sort(key=lambda item: item[1], reverse=True)
    if not hits:
        return ["当前样本里没有明显的出图指令，卡片主要依据协作行为、能力层级与过程规模生成。"]
    lines = []
    for name, _, keywords in hits[:4]:
        joined = "、".join(dict.fromkeys(keywords))
        note = IMAGE_CONCEPT_NOTES.get(name, "轨迹里对这一类要求有连续强调。")
        lines.append(f"{name}：{note} 命中词包括 {joined}。")
    return lines


def _fmt_int(value: int) -> str:
    return f"{int(value):,}"


def _as_dict(value: object) -> dict[str, object]:
    return value if isinstance(value, dict) else {}
