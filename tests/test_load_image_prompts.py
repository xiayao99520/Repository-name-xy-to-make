"""Ensure a generation batch cannot start with missing or draft prompts."""

import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest


sys.dont_write_bytecode = True
SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "load_image_prompts.py"
SPEC = importlib.util.spec_from_file_location("load_image_prompts", SCRIPT)
LOADER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LOADER)


class PromptPreparationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="image-prompts-")
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)
        self.prompt_dir = self.project / "02-四张图片提示词"
        self.prompt_dir.mkdir()
        for number, name in enumerate(LOADER.NAMES, start=1):
            (self.prompt_dir / name).write_text(f"Use case: ads-marketing\n第 {number} 张实际完整提示词", encoding="utf-8")

    def test_all_four_saved_prompts_loaded_in_number_order(self):
        items = LOADER.load_prompts(self.project)
        self.assertEqual([item["number"] for item in items], [1, 2, 3, 4])
        self.assertEqual(len({item["path"] for item in items}), 4)
        for number, item in enumerate(items, start=1):
            self.assertIn(f"第 {number} 张", item["prompt"])

    def test_missing_prompt_blocks_batch(self):
        (self.prompt_dir / LOADER.NAMES[2]).unlink()
        with self.assertRaisesRegex(ValueError, "第 3 张"):
            LOADER.load_prompts(self.project)

    def test_empty_prompt_blocks_batch(self):
        (self.prompt_dir / LOADER.NAMES[0]).write_text(" \n\t", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "第 1 张"):
            LOADER.load_prompts(self.project)

    def test_unreplaced_package_draft_blocks_batch(self):
        (self.prompt_dir / LOADER.NAMES[3]).write_text(
            LOADER.PACKAGE_DRAFT_PREFIX + "这是内部草稿", encoding="utf-8"
        )
        with self.assertRaisesRegex(ValueError, "第 4 张"):
            LOADER.load_prompts(self.project)


if __name__ == "__main__":
    unittest.main()
