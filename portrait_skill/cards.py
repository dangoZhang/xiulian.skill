from __future__ import annotations

from html import escape
from pathlib import Path
import re
import subprocess

from .parsers import default_display_name
from .themes import get_ai_level_theme


def write_cards(payload: dict[str, object], output_dir: str | Path, certificate_choice: str = "both") -> dict[str, str]:
    del certificate_choice
    target_dir = Path(output_dir).expanduser().resolve()
    target_dir.mkdir(parents=True, exist_ok=True)
    svg_path = target_dir / "xiuxian-card.svg"
    png_path = target_dir / "xiuxian-card.png"
    svg_path.write_text(render_xiuxian_card(payload), encoding="utf-8")
    _render_png(svg_path, png_path)
    return {"card_svg": str(svg_path), "card_png": str(png_path)}


def render_xiuxian_card(payload: dict[str, object]) -> str:
    insights = _as_dict(payload.get("insights"))
    display_name = _get_display_name(payload)
    generated_at = _format_generated_at(payload.get("generated_at"))
    realm = str(insights.get("realm") or "凡人")
    rank = str(insights.get("rank") or "L1")
    ability_lines = _wrap_block([str(insights.get("ability_text") or "仍在引气试手。")], 25.0, limit=4)
    verdict_source = _string_list(insights.get("card_verdict_lines")) or _string_list(insights.get("verdict_lines"))
    verdict_lines = _wrap_block(verdict_source, 24.5, limit=6)
    breakthrough_lines = _wrap_block(_string_list(insights.get("breakthrough_lines")), 24.5, limit=4)
    theme = get_ai_level_theme(rank)

    model_name = _primary_model(payload)
    sample_name = _sample_name(payload)
    ability_panel_y = 694
    ability_panel_h = max(348, 170 + len(ability_lines) * 40 + len(verdict_lines) * 32)
    break_panel_y = ability_panel_y + ability_panel_h + 28
    break_panel_h = max(188, 112 + len(breakthrough_lines) * 30)
    footer_chip_y = break_panel_y + break_panel_h + 34
    footer_text_y = footer_chip_y + 96
    verdict_y = 970 + max(0, len(ability_lines) - 1) * 42
    breakthrough_y = break_panel_y + 110

    return f"""<svg width="1200" height="1600" viewBox="0 0 1200 1600" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="74" y1="52" x2="1134" y2="1544" gradientUnits="userSpaceOnUse">
      <stop stop-color="{_escape(str(theme.get("bg_from", "#1B1B1B")))}"/>
      <stop offset="1" stop-color="{_escape(str(theme.get("bg_to", "#101820")))}"/>
    </linearGradient>
    <radialGradient id="halo" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(926 246) rotate(141) scale(344 232)">
      <stop stop-color="{_escape(str(theme.get("halo", "#8EC5FF")))}" stop-opacity="0.24"/>
      <stop offset="1" stop-color="{_escape(str(theme.get("halo", "#8EC5FF")))}" stop-opacity="0"/>
    </radialGradient>
    <filter id="shadow" x="102" y="88" width="996" height="1458" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
      <feFlood flood-opacity="0" result="BackgroundImageFix"/>
      <feColorMatrix in="SourceAlpha" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0" result="hardAlpha"/>
      <feOffset dy="26"/>
      <feGaussianBlur stdDeviation="24"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.05 0 0 0 0 0.04 0 0 0 0 0.03 0 0 0 0.38 0"/>
      <feBlend mode="normal" in2="BackgroundImageFix" result="effect1_dropShadow_0_1"/>
      <feBlend mode="normal" in="SourceGraphic" in2="effect1_dropShadow_0_1" result="shape"/>
    </filter>
  </defs>

  <rect width="1200" height="1600" rx="48" fill="url(#bg)"/>
  <ellipse cx="926" cy="246" rx="280" ry="188" fill="url(#halo)"/>

  <g filter="url(#shadow)">
    <rect x="154" y="120" width="892" height="1368" rx="38" fill="#F7F4EC"/>
    <rect x="182" y="146" width="836" height="1316" rx="30" stroke="#FFFFFF" stroke-opacity="0.82" stroke-width="4"/>
    <rect x="182" y="146" width="836" height="128" rx="30" fill="{_escape(str(theme.get("accent", "#8EC5FF")))}"/>
    <rect x="210" y="304" width="780" height="338" rx="34" fill="{_escape(str(theme.get("panel_bg", "#162B49")))}"/>
    <rect x="210" y="{ability_panel_y}" width="780" height="{ability_panel_h}" rx="32" fill="#FFFDF8"/>
    <rect x="210" y="{break_panel_y}" width="780" height="{break_panel_h}" rx="28" fill="{_escape(str(theme.get("soft_panel", "#F7F4EC")))}"/>
  </g>

  <text x="600" y="202" fill="#12202E" font-size="28" text-anchor="middle" font-family="PingFang SC, Hiragino Sans GB, Microsoft YaHei, sans-serif" letter-spacing="4">修仙.skill</text>
  <text x="600" y="246" fill="#12202E" font-size="20" text-anchor="middle" font-family="PingFang SC, Hiragino Sans GB, Microsoft YaHei, sans-serif">蒸馏你的 vibecoding 修为</text>

  <text x="318" y="382" fill="#F8F3EA" font-size="22" font-family="PingFang SC, Hiragino Sans GB, Microsoft YaHei, sans-serif" letter-spacing="4">当前境界</text>
  <text x="318" y="500" fill="#FFFFFF" font-size="128" font-family="STKaiti, KaiTi, serif">{_escape(realm)}</text>
  <text x="318" y="556" fill="#DCE9F7" font-size="20" font-family="PingFang SC, Hiragino Sans GB, Microsoft YaHei, sans-serif">赛博修仙中的修为层次</text>

  <rect x="748" y="366" width="188" height="84" rx="42" fill="#FFFFFF" fill-opacity="0.12"/>
  <text x="842" y="402" fill="#DCE9F7" font-size="18" text-anchor="middle" font-family="PingFang SC, Hiragino Sans GB, Microsoft YaHei, sans-serif" letter-spacing="4">修为等级</text>
  <text x="842" y="540" fill="{_escape(str(theme.get("accent", "#8EC5FF")))}" font-size="120" text-anchor="middle" font-family="Inter, PingFang SC, Microsoft YaHei, sans-serif" font-weight="800">{_escape(rank)}</text>
  <text x="842" y="592" fill="#DCE9F7" font-size="20" text-anchor="middle" font-family="PingFang SC, Hiragino Sans GB, Microsoft YaHei, sans-serif">参考洛谷色阶</text>

  <text x="250" y="758" fill="#7A633F" font-size="19" font-family="PingFang SC, Hiragino Sans GB, Microsoft YaHei, sans-serif" letter-spacing="4">蒸馏能力</text>
  {_text_lines(ability_lines, x=250, y=822, font_size=33, line_height=42, fill="#1C1A16", anchor="start", family="PingFang SC, Hiragino Sans GB, Microsoft YaHei, sans-serif", weight="700")}
  <line x1="250" y1="{868 + max(0, len(ability_lines) - 1) * 42}" x2="950" y2="{868 + max(0, len(ability_lines) - 1) * 42}" stroke="#E8DFCF" stroke-width="2"/>
  <text x="250" y="{914 + max(0, len(ability_lines) - 1) * 42}" fill="#7A633F" font-size="18" font-family="PingFang SC, Hiragino Sans GB, Microsoft YaHei, sans-serif" letter-spacing="4">判词</text>
  {_text_lines(verdict_lines, x=250, y=verdict_y, font_size=26, line_height=32, fill="#2A241C", anchor="start", family="PingFang SC, Hiragino Sans GB, Microsoft YaHei, sans-serif", weight="500")}

  <text x="250" y="{break_panel_y + 52}" fill="#7A633F" font-size="18" font-family="PingFang SC, Hiragino Sans GB, Microsoft YaHei, sans-serif" letter-spacing="4">破境之法</text>
  {_text_lines(breakthrough_lines, x=250, y=breakthrough_y, font_size=28, line_height=30, fill="#241F18", anchor="start", family="PingFang SC, Hiragino Sans GB, Microsoft YaHei, sans-serif", weight="600")}

  {_chip(210, footer_chip_y, 246, "炉主", model_name, theme)}
  {_chip(477, footer_chip_y, 246, "耗材", _token_name(payload), theme)}
  {_chip(744, footer_chip_y, 246, "样本", sample_name, theme)}

  <line x1="254" y1="{footer_text_y - 28}" x2="946" y2="{footer_text_y - 28}" stroke="#DDD1BE" stroke-width="2"/>
  <text x="254" y="{footer_text_y}" fill="#8E7C61" font-size="17" text-anchor="start" font-family="PingFang SC, Hiragino Sans GB, Microsoft YaHei, sans-serif">{_escape(f'命主 · {display_name}')}</text>
  <text x="946" y="{footer_text_y}" fill="#8E7C61" font-size="17" text-anchor="end" font-family="PingFang SC, Hiragino Sans GB, Microsoft YaHei, sans-serif">{_escape(f'起炉时间 · {generated_at}')}</text>
</svg>
"""


def _chip(x: int, y: int, width: int, title: str, value: str, theme: dict[str, str]) -> str:
    return f"""
  <g>
    <rect x="{x}" y="{y}" width="{width}" height="74" rx="22" fill="#FFFFFF" fill-opacity="0.9"/>
    <rect x="{x}" y="{y}" width="{width}" height="6" rx="3" fill="{_escape(str(theme.get('accent', '#8EC5FF')))}"/>
    <text x="{x + 22}" y="{y + 34}" fill="#7A633F" font-size="16" font-family="PingFang SC, Hiragino Sans GB, Microsoft YaHei, sans-serif">{_escape(title)}</text>
    <text x="{x + 22}" y="{y + 62}" fill="#231F1A" font-size="22" font-family="Inter, PingFang SC, Microsoft YaHei, sans-serif" font-weight="700">{_escape(_truncate_text(value, 24))}</text>
  </g>"""


def _text_lines(
    lines: list[str],
    *,
    x: int,
    y: int,
    font_size: int,
    line_height: int,
    fill: str,
    anchor: str,
    family: str,
    weight: str = "400",
) -> str:
    if not lines:
        return ""
    parts = [f'<text x="{x}" y="{y}" fill="{fill}" font-size="{font_size}" text-anchor="{anchor}" font-family="{family}" font-weight="{weight}">']
    for index, line in enumerate(lines):
        dy = 0 if index == 0 else line_height
        parts.append(f'<tspan x="{x}" dy="{dy}">{_escape(line)}</tspan>')
    parts.append("</text>")
    return "".join(parts)


def _wrap_text(text: str, max_units: float, limit: int | None = None) -> list[str]:
    cleaned = " ".join((text or "").split())
    if not cleaned:
        return []
    tokens = _tokenize_for_wrap(cleaned)
    lines: list[str] = []
    current = ""
    current_units = 0.0
    for token in tokens:
        token_units = _text_units(token)
        if token_units > max_units:
            for segment in _split_long_token(token, max_units):
                segment_units = _text_units(segment)
                if current and current_units + segment_units > max_units:
                    lines.append(current)
                    current = ""
                    current_units = 0.0
                    if limit and len(lines) >= limit:
                        break
                current += segment
                current_units += segment_units
            if limit and len(lines) >= limit:
                break
            continue
        if current and current_units + token_units > max_units:
            lines.append(current)
            current = token
            current_units = token_units
            if limit and len(lines) >= limit:
                break
            continue
        current += token
        current_units += token_units
    if current and (not limit or len(lines) < limit):
        lines.append(current)
    if limit and len(lines) > limit:
        lines = lines[:limit]
    if limit and lines and len(lines) == limit and _text_units(cleaned) > sum(_text_units(line) for line in lines):
        lines[-1] = _truncate_text(lines[-1], max(2, int(max_units) - 2))
    return lines


def _wrap_block(items: list[str], max_units: float, limit: int) -> list[str]:
    lines: list[str] = []
    for item in items:
        wrapped = _wrap_text(str(item), max_units)
        if not wrapped:
            continue
        remaining = limit - len(lines)
        if remaining <= 0:
            break
        if len(wrapped) <= remaining:
            lines.extend(wrapped)
            continue
        lines.extend(wrapped[:remaining])
        lines[-1] = _truncate_text(lines[-1], max(2, int(max_units) - 2))
        break
    return lines


def _truncate_text(text: str, limit_units: int) -> str:
    total = 0.0
    result = []
    for char in text:
        units = _char_units(char)
        if total + units > limit_units:
            result.append("…")
            break
        result.append(char)
        total += units
    return "".join(result)


def _tokenize_for_wrap(text: str) -> list[str]:
    tokens: list[str] = []
    i = 0
    while i < len(text):
        char = text[i]
        if char in "（(":
            closing = "）" if char == "（" else ")"
            end = text.find(closing, i + 1)
            if end != -1:
                tokens.append(text[i : end + 1])
                i = end + 1
                continue
        if char.isspace():
            i += 1
            continue
        if ord(char) < 128:
            j = i + 1
            while j < len(text) and ord(text[j]) < 128 and text[j] not in "（(":
                j += 1
            tokens.append(text[i:j].rstrip())
            i = j
            continue
        tokens.append(char)
        i += 1
    return [token for token in tokens if token]


def _split_long_token(token: str, max_units: float) -> list[str]:
    parts: list[str] = []
    working = token
    if token.startswith(("（", "(")) and token.endswith(("）", ")")):
        opener, closer = token[0], token[-1]
        inner = token[1:-1]
        inner_parts = _split_ascii_segment(inner, max_units - 1.2)
        for index, part in enumerate(inner_parts):
            prefix = opener if index == 0 else ""
            suffix = closer if index == len(inner_parts) - 1 else ""
            parts.append(f"{prefix}{part}{suffix}")
        return parts
    if re.fullmatch(r"[\x00-\x7F]+", token):
        return _split_ascii_segment(working, max_units)
    return _split_cjk_segment(working, max_units)


def _split_ascii_segment(text: str, max_units: float) -> list[str]:
    words = re.findall(r"\S+\s*", text)
    if not words:
        return [text]
    parts: list[str] = []
    current = ""
    current_units = 0.0
    for word in words:
        word_units = _text_units(word)
        if current and current_units + word_units > max_units:
            parts.append(current.rstrip())
            current = word
            current_units = word_units
            continue
        current += word
        current_units += word_units
    if current.strip():
        parts.append(current.rstrip())
    return parts or [text]


def _split_cjk_segment(text: str, max_units: float) -> list[str]:
    parts: list[str] = []
    current = ""
    current_units = 0.0
    for char in text:
        char_units = _char_units(char)
        if current and current_units + char_units > max_units:
            parts.append(current)
            current = char
            current_units = char_units
            continue
        current += char
        current_units += char_units
    if current:
        parts.append(current)
    return parts or [text]


def _text_units(text: str) -> float:
    return sum(_char_units(char) for char in text)


def _char_units(char: str) -> float:
    if char.isspace():
        return 0.35
    if ord(char) < 128:
        return 0.58
    return 1.0


def _primary_model(payload: dict[str, object]) -> str:
    transcript = _as_dict(payload.get("transcript"))
    models = transcript.get("models")
    if isinstance(models, list) and models:
        return _truncate_text(str(models[0]).replace("openai/", "").replace("anthropic/", ""), 24)
    return "未识炉主"


def _sample_name(payload: dict[str, object]) -> str:
    transcript = _as_dict(payload.get("transcript"))
    messages = int(transcript.get("message_count") or payload.get("total_messages") or 0)
    tool_calls = int(transcript.get("tool_calls") or payload.get("total_tool_calls") or 0)
    sessions_used = payload.get("sessions_used")
    if isinstance(sessions_used, int) and sessions_used > 1:
        return _truncate_text(f"{sessions_used} 场 · {messages} messages", 24)
    return _truncate_text(f"{messages} messages · {tool_calls} tool calls", 24)


def _token_name(payload: dict[str, object]) -> str:
    transcript = _as_dict(payload.get("transcript"))
    usage = _as_dict(transcript.get("token_usage")) or _as_dict(payload.get("token_usage"))
    total = int(usage.get("total_tokens") or 0)
    return f"{total:,} token" if total else "token 未显"


def _get_display_name(payload: dict[str, object]) -> str:
    transcript = _as_dict(payload.get("transcript"))
    if transcript.get("display_name"):
        return str(transcript["display_name"])
    if payload.get("display_name"):
        return str(payload["display_name"])
    return default_display_name("user")


def _format_generated_at(value: object) -> str:
    text = str(value or "").strip()
    return text.replace("T", " ").replace("+08:00", "").replace("+00:00", " UTC")


def _string_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if str(item).strip()]


def _escape(value: str) -> str:
    return escape(value, quote=True)


def _as_dict(value: object) -> dict[str, object]:
    return value if isinstance(value, dict) else {}


def _render_png(svg_path: Path, png_path: Path) -> None:
    subprocess.run(
        [
            "rsvg-convert",
            "--dpi-x",
            "300",
            "--dpi-y",
            "300",
            str(svg_path),
            "-o",
            str(png_path),
        ],
        check=True,
    )
    subprocess.run(
        [
            "sips",
            "-s",
            "dpiWidth",
            "300",
            "-s",
            "dpiHeight",
            "300",
            str(png_path),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
