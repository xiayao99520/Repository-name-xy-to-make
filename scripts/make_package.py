#!/usr/bin/env python3
"""Build a minimal Jimeng package from approved images and a visual plan."""

from __future__ import annotations

import argparse
from datetime import date
import re
import shutil
from pathlib import Path


def image_count(duration: float) -> int:
    """Round a 4–8 second video up to the existing 2/3/4-image tiers."""
    if duration < 4 or duration > 8:
        raise ValueError("视频时长必须在 4 到 8 秒之间")
    if duration <= 4:
        return 2
    if duration <= 6:
        return 3
    return 4
STYLE = (
    "高级半调纸拼贴，黑白 halftone 摄影剪贴，彩色卡纸，清晰裁切边，"
    "暖奶油色描边，细腻纸张颗粒，柔和纸张阴影，二维定格动画质感，非写实 3D。"
)


def clean_name(value: str) -> str:
    value = re.sub(r"[\\/:*?\"<>|\r\n]+", " ", value).strip()
    value = re.sub(r"\s+", " ", value)
    return (value or "未命名项目")[:48]


def build_prompt(args: argparse.Namespace, count: int) -> str:
    last = count
    return f"""请使用我上传的 {count} 张参考图，按 1→2→{last} 的顺序，生成一条 {args.duration} 秒、9:16 竖屏的半调纸拼贴二维定格动画。

对应口播：{args.voiceover}
全文上下文仅用于理解语义，不要把全文写到画面中。
核心场景：{args.scene}
关键对象：{args.objects}
允许的动作：{args.action}
最终结果：{args.result}

动画顺序：先保持第 1 张图的场景构图；再让指定对象在画面中部按上述允许的动作小幅运动；最后形成第 {last} 张图的结果并停留片刻。未被指定的对象保持静止。

视觉风格：{STYLE}

硬性限制：只使用上传参考图中已有的对象。禁止新增人物、物体、建筑、道具、图标、Logo、UI、装饰或背景元素。禁止额外文字、字幕、标题、英文、数字、字母、乱码、随机标记、问号、感叹号、箭头、叉号和其他符号；只有参考图中已经存在且本提示词明确要求保留的中文标签才允许出现。参考图中的对象身份、数量、形状、材质、颜色、中文标签、相对位置和纸张风格必须保持不变，不得变形、融合、替换、重绘、补全或复制。只允许上述“允许的动作”，运动幅度小而清楚。

固定镜头，固定视角，固定 9:16 画幅。禁止切镜、转场、推拉、摇移、旋转、变焦、3D 化、镜头抖动、视角改变和整张图淡入。无对白、无配乐、无水印。最后一帧保持结果构图。"""


def make(args: argparse.Namespace) -> Path:
    count = image_count(args.duration)
    if len(args.images) != count:
        raise ValueError(f"{args.duration} 秒必须提供 {count} 张图片，实际收到 {len(args.images)} 张")

    output = Path(args.output).expanduser().resolve()
    title = clean_name(args.voiceover[:24])
    project = output / f"{args.date or date.today().isoformat()}-{title}"
    if project.exists():
        raise FileExistsError(f"输出目录已存在：{project}")
    project.mkdir(parents=True)

    for index, source in enumerate(args.images, start=1):
        source_path = Path(source).expanduser().resolve()
        if not source_path.is_file():
            raise FileNotFoundError(source_path)
        suffix = source_path.suffix.lower() or ".png"
        shutil.copy2(source_path, project / f"{index:02d}{suffix}")

    (project / "即梦视频提示词.txt").write_text(
        build_prompt(args, count) + "\n", encoding="utf-8"
    )
    return project


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a minimal Jimeng collage package")
    parser.add_argument("--transcript", required=True, help="full transcript")
    parser.add_argument("--voiceover", required=True, help="voiceover segment to visualize")
    parser.add_argument("--duration", type=float, required=True, help="4 到 8 秒，可用小数")
    parser.add_argument("--scene", required=True)
    parser.add_argument("--objects", required=True)
    parser.add_argument("--action", required=True)
    parser.add_argument("--result", required=True)
    parser.add_argument("--image", dest="images", action="append", required=True)
    parser.add_argument("--output", default=".")
    parser.add_argument("--date", help="override YYYY-MM-DD")
    args = parser.parse_args()
    project = make(args)
    print(project)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
