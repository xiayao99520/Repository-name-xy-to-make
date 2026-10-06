#!/usr/bin/env python3
"""Load all four saved image prompts before a parallel image generation batch."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


NAMES = (
    "01-建立场景.txt",
    "02-关键对象.txt",
    "03-动作关系.txt",
    "04-结果冲突.txt",
)
PACKAGE_DRAFT_PREFIX = "请生成一张用于即梦图生视频参考的成品静帧。"


def load_prompts(project: Path) -> list[dict[str, object]]:
    prompt_dir = project.expanduser().resolve() / "02-四张图片提示词"
    items = []
    for number, name in enumerate(NAMES, start=1):
        path = prompt_dir / name
        if not path.is_file():
            raise ValueError(f"缺少第 {number} 张的生图提示词：{path}")
        prompt = path.read_text(encoding="utf-8-sig")
        if not prompt.strip() or prompt.lstrip().startswith(PACKAGE_DRAFT_PREFIX):
            raise ValueError(f"第 {number} 张尚未写好实际生图提示词：{path}")
        items.append({"number": number, "path": str(path), "prompt": prompt})
    return items


def main() -> int:
    parser = argparse.ArgumentParser(description="一次读取四份已保存的实际生图提示词")
    parser.add_argument("--project", type=Path, required=True)
    args = parser.parse_args()
    try:
        items = load_prompts(args.project)
    except (OSError, ValueError, UnicodeError) as exc:
        parser.error(str(exc))
    print(json.dumps(items, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
