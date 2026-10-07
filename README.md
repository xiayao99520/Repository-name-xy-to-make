# 插画风 / XY to make

面向中文新闻短视频的半调纸拼贴 B-roll 工作流。输入一段口播，Skill 会分别设计四张语义独立的 9:16 参考图，生成四份完整生图 Prompt，并输出一份即梦视频提示词。

## 处理方式

- 四张图分别理解口播，不把一张总图拆成四个连续状态。
- 每张 Prompt 保留旧流程的用途、画幅、半调纸拼贴风格、中部核心、顶部标题安全区和独立排除项。
- 四份 Prompt 全部保存并逐字校验后，四路同批调用 Codex `image_gen`；不使用前图引用。
- 网络或超时失败只补试一次，不调用视频 API，不做生成后的视觉重做。
- 即梦视频提示词继续由原 `video_prompt()` 生成。

## 交付

```text
交付/YYYY-MM-DD-主题/
├── 01-建立场景.png
├── 02-关键对象.png
├── 03-动作关系.png
├── 04-结果冲突.png
└── 05-即梦视频提示词.txt
```

四张图片拖入即梦参考图区域，复制提示词生成视频，再按需要放入剪映。

## 本地控制

`config/local-control.json` 默认启用。可用以下命令控制本机流程：

```powershell
python scripts/access_control.py --check
python scripts/access_control.py --disable
python scripts/access_control.py --enable
```

MIT 许可证和版权声明见 [LICENSE](LICENSE)。
