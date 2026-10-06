# 插画风 / XY to make

面向中文新闻短视频的半调纸拼贴 B-roll 工作流。输入一段口播，自动准备四张语义独立的 9:16 参考图和一份可复制到即梦的视频提示词。

## 能力

- 自动理解口播，安排场景、对象、动作关系和结果冲突。
- 先写完四份完整生图提示词，再同批发出四次独立 Codex 生图请求。
- 生成结果按原编号保存；网络或超时失败只对失败编号补试一次。
- 使用确定性的 `video_prompt()` 生成即梦提示词，不改写成逐秒分镜稿。
- 最终单独导出四张图片和 `05-即梦视频提示词.txt`，原字节复制并校验哈希。

## 使用方式

用户只需提供一段中文口播。Skill 自动完成内部方案、四图生图、视频提示词和交付导出。默认使用中文、9:16、约 5 秒；用户指定时长时沿用指定时长。

交付目录严格包含：

```text
交付/YYYY-MM-DD-主题/
├── 01-建立场景.png
├── 02-关键对象.png
├── 03-动作关系.png
├── 04-结果冲突.png
└── 05-即梦视频提示词.txt
```

把四张图片拖入即梦参考图区域，复制提示词文件内容生成视频，再按需要放入剪映。

## 视觉规则

统一使用 editorial 半调纸拼贴：黑白 halftone 摄影剪贴、彩色卡纸、奶油色描边、纸张颗粒和柔和阴影。画面铺满，主要信息位于中部核心区域；顶部保留新闻标题安全区，边缘可以有不抢语义的次要装饰。

四张图是四个语义侧重点各自完整的画面，不锁定同一块画板、同一组物件或同一套坐标。提示词中的中文标签、数量和否定关系随本次口播重新设计。

## 本地控制

`config/local-control.json` 默认启用。开始处理前会检查这个开关：

```powershell
python scripts/access_control.py --check
python scripts/access_control.py --disable
python scripts/access_control.py --enable
```

停用时不会调用生图、建立素材包或导出交付目录。开关是本机操作控制，不提供加密授权；拿到源码的人仍可能自行修改代码。

## 开发检查

```powershell
$env:PYTHONUTF8 = '1'
python C:\Users\Administrator\.codex\skills\.system\skill-creator\scripts\quick_validate.py .
python -B -m unittest discover -s tests -p "test_*.py" -v
```

## 目录

- `SKILL.md`：运行规则和交付协议。
- `scripts/`：建包、Prompt barrier、导出和本地开关脚本。
- `tests/`：导出、Prompt barrier 和本地开关测试。
- `evals/`：行为验收用例。

MIT 许可证和版权声明见 [LICENSE](LICENSE)。
