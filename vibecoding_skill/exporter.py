from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path

from .cards import write_cards


def export_bundle(
    *,
    payload: dict[str, object],
    markdown: str,
    output_dir: str | Path,
    card_style: str = "default",
    archive: bool = False,
    slug: str | None = None,
) -> dict[str, str]:
    root = Path(output_dir).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)

    display_name = _display_name(payload)
    export_slug = _slugify(slug or display_name or "vibecoding-profile")
    assets_dir = root / "assets"
    cards = write_cards(payload, assets_dir, style=card_style)

    report_path = root / "REPORT.md"
    profile_path = root / "PROFILE.md"
    skill_path = root / "SKILL.md"
    readme_path = root / "README.md"
    json_path = root / "snapshot.json"

    report_path.write_text(markdown, encoding="utf-8")
    profile_path.write_text(_render_profile(payload), encoding="utf-8")
    skill_path.write_text(_render_skill(payload, export_slug), encoding="utf-8")
    readme_path.write_text(_render_readme(payload, export_slug), encoding="utf-8")
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    result = {
        "export_dir": str(root),
        "share_skill_dir": str(root),
        "share_readme": str(readme_path),
        "share_profile": str(profile_path),
        "share_report": str(report_path),
        "share_json": str(json_path),
        "card_svg": cards["card_svg"],
        "card_png": cards["card_png"],
    }
    if archive:
        zip_path = root.parent / f"{root.name}.zip"
        _zip_dir(root, zip_path)
        result["share_zip"] = str(zip_path)
    return result


def _render_readme(payload: dict[str, object], export_slug: str) -> str:
    name = _display_name(payload)
    rank = _insight(payload, "rank", "L1")
    stage = _insight(payload, "stage", "试手期")
    ability = _insight(payload, "ability_text", "这套协作还在试手期。")
    generated_at = str(payload.get("generated_at") or "")
    usage_line = _insight(payload, "usage_line", "")
    lines = [
        f"# {name} 的 vibecoding 导出包",
        "",
        f"这是从真实协作记录里导出的可分享 skill 包，当前判断为 `{stage} · {rank}`。",
        "",
        "## 分享哪个文件",
        "",
        "- 想让别人直接装进 Agent：分享整个目录，或压缩后的 zip。",
        "- 想让别人快速看懂这套做法：分享 `PROFILE.md`。",
        "- 想让别人看完整判断依据：分享 `REPORT.md`。",
        "- 想发群或发社交平台：分享 `assets/vibecoding-card.png`。",
        "",
        "## 这包里有什么",
        "",
        "- `SKILL.md`：可直接安装给 Agent 的技能入口。",
        "- `PROFILE.md`：压缩后的习惯画像，适合转发和快速阅读。",
        "- `REPORT.md`：完整报告，包含判断依据和突破建议。",
        "- `snapshot.json`：结构化结果，方便二次开发。",
        "- `assets/`：分享卡图片。",
        "",
        "## 这套习惯的摘要",
        "",
        f"- 等级：`{rank}`",
        f"- 阶段：`{stage}`",
        f"- 判断：{ability}",
    ]
    if usage_line:
        lines.append(f"- 取样规模：`{usage_line}`")
    if generated_at:
        lines.append(f"- 导出时间：`{generated_at}`")
    lines.extend(
        [
            "",
            "## 如何安装",
            "",
            "把整个目录交给支持 skills 的 Agent 宿主即可，本地路径或 zip 都可以。",
            "",
            "```bash",
            f"npx skills add /path/to/{export_slug} -a codex",
            "```",
            "",
            "## 装好之后可以直接说",
            "",
            "- 按这份 vibecoding 习惯和我一起做事。",
            "- 先模仿这套协作节奏，再开始当前任务。",
            "- 按这份画像指出我最该补的动作。",
        ]
    )
    return "\n".join(lines).strip() + "\n"


def _render_skill(payload: dict[str, object], export_slug: str) -> str:
    name = _display_name(payload)
    rank = _insight(payload, "rank", "L1")
    habit_lines = _list_insight(payload, "habit_profile_lines")
    mimic_lines = _list_insight(payload, "mimic_lines")
    breakthrough_lines = _list_insight(payload, "breakthrough_lines")
    coaching_lines = _list_insight(payload, "coaching_focus_lines") + _list_insight(payload, "coaching_drill_lines")
    prompt_examples = [
        f"按 {name} 这套 vibecoding 节奏和我一起推进这个任务。",
        f"先模仿 {name} 的协作习惯，再开始当前项目。",
        "如果这套做法里有明显短板，边做边提醒我，不要等到最后再说。",
    ]
    lines = [
        "---",
        f"name: {export_slug}",
        f"description: 模仿{name}的 vibecoding 习惯，按这套节奏协作，并在需要时指出如何升级。",
        "---",
        "",
        f"# {name} 的 vibecoding skill",
        "",
        "## Read First",
        "",
        "先读 [PROFILE.md](./PROFILE.md) 和 [REPORT.md](./REPORT.md)。",
        "",
        "## Default Behavior",
        "",
        f"默认按这份画像里的协作节奏工作，当前参考等级是 `{rank}`。",
        "- 开局先收束目标、上下文、约束和验收口径。",
        "- 能直接执行就直接执行，不停在空分析里。",
        "- 保留这套习惯里的强项，主动规避报告里指出的短板。",
        "- 每轮完成后补一句回看：做了什么、还缺什么、下一步是什么。",
        "",
        "## Distilled Habits",
        "",
    ]
    for item in habit_lines:
        lines.append(f"- {item}")
    if mimic_lines:
        lines.extend(["", "## How To Mimic"])
        for item in mimic_lines:
            lines.append(f"- {item}")
    if breakthrough_lines or coaching_lines:
        lines.extend(["", "## How To Improve"])
        for item in breakthrough_lines + coaching_lines:
            lines.append(f"- {item}")
    lines.extend(["", "## Good Prompts", ""])
    for item in prompt_examples:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            "- 如果当前用户、仓库或系统指令和这份画像冲突，以更高优先级指令为准。",
            "- 事实不够时先补信息，不要硬装得像。",
            "- 这份 skill 的目标是复现协作节奏，不是扮演人格。",
        ]
    )
    return "\n".join(lines).strip() + "\n"


def _render_profile(payload: dict[str, object]) -> str:
    name = _display_name(payload)
    rank = _insight(payload, "rank", "L1")
    stage = _insight(payload, "stage", "试手期")
    ability = _insight(payload, "ability_text", "还在试手。")
    usage_line = _insight(payload, "usage_line", "")
    generated_at = str(payload.get("generated_at") or "")
    habit_lines = _list_insight(payload, "habit_profile_lines")
    mimic_lines = _list_insight(payload, "mimic_lines")
    verdict_lines = _list_insight(payload, "verdict_lines")
    breakthrough_lines = _list_insight(payload, "breakthrough_lines")
    modern_lines = _list_insight(payload, "modern_signal_lines")
    user_summary = _list_insight(payload, "user_summary_lines")
    assistant_summary = _list_insight(payload, "assistant_summary_lines")
    model_name = _primary_model(payload)

    lines = [
        f"# {name} 的 vibecoding 画像",
        "",
        f"- 等级：`{rank}`",
        f"- 阶段：`{stage}`",
        f"- 主用模型：`{model_name}`",
        f"- 能力摘要：{ability}",
    ]
    if usage_line:
        lines.append(f"- 取样规模：`{usage_line}`")
    if generated_at:
        lines.append(f"- 生成时间：`{generated_at}`")
    if habit_lines:
        lines.extend(["", "## 这套习惯是什么"])
        for item in habit_lines:
            lines.append(f"- {item}")
    if user_summary or assistant_summary:
        lines.extend(["", "## 关键观察"])
        for item in user_summary + assistant_summary:
            lines.append(f"- {item}")
    if verdict_lines:
        lines.extend(["", "## 判词"])
        for item in verdict_lines:
            lines.append(f"- {item}")
    if mimic_lines:
        lines.extend(["", "## 如果想模仿这套做法"])
        for item in mimic_lines:
            lines.append(f"- {item}")
    if breakthrough_lines:
        lines.extend(["", "## 如果想继续升级"])
        for item in breakthrough_lines:
            lines.append(f"- {item}")
    if modern_lines:
        lines.extend(["", "## 现代协作信号"])
        for item in modern_lines:
            lines.append(f"- {item}")
    return "\n".join(lines).strip() + "\n"


def _insight(payload: dict[str, object], key: str, default: str) -> str:
    insights = payload.get("insights")
    if isinstance(insights, dict):
        value = insights.get(key)
        if isinstance(value, str) and value:
            return value
    return default


def _list_insight(payload: dict[str, object], key: str) -> list[str]:
    insights = payload.get("insights")
    if not isinstance(insights, dict):
        return []
    value = insights.get(key)
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def _display_name(payload: dict[str, object]) -> str:
    for key in ("display_name",):
        value = payload.get(key)
        if isinstance(value, str) and value:
            return value
    transcript = payload.get("transcript")
    if isinstance(transcript, dict):
        value = transcript.get("display_name")
        if isinstance(value, str) and value:
            return value
    return "码奸"


def _primary_model(payload: dict[str, object]) -> str:
    transcript = payload.get("transcript")
    if isinstance(transcript, dict):
        models = transcript.get("models")
        if isinstance(models, list) and models:
            return str(models[0])
    models = payload.get("models")
    if isinstance(models, list) and models:
        top = models[0]
        if isinstance(top, dict):
            return str(top.get("name") or top.get("model") or "未知模型")
        if isinstance(top, str):
            return top
    return "未知模型"


def _slugify(text: str) -> str:
    base = re.sub(r"[^A-Za-z0-9._-]+", "-", text.strip()).strip("-._")
    return base.lower() or "vibecoding-profile"


def _zip_dir(root: Path, target: Path) -> None:
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            archive.write(path, arcname=path.relative_to(root.parent))
