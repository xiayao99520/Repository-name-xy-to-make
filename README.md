# 插画风 / XY to make

面向中文新闻短视频的半调纸拼贴 B-roll 工作流。输入一段口播，内部先拆出四张语义独立画面，再生成四份完整生图 Prompt、四张 9:16 参考图和一份即梦视频提示词。

## 工作方式

- 自动理解口播，保留数字、否定、条件和对象归属。
- 内部形成详细四图方案：建立场景、关键对象、动作关系、结果冲突。
- 四份 Prompt 使用完整的用途、视觉语言、构图安全区、独立对象、中文标签、数量约束和负面限制；不把 Prompt 压缩成几句概括。
- 四份 Prompt 全部保存后，同批发出四次独立 Codex image_gen 请求；不传前图，不按完成先后改编号。
- 网络或超时失败只补试一次；只做文件完整性检查，不调用视频 API。
- 即梦提示词继续由原 `video_prompt()` 生成，禁止改写成逐秒分镜稿。

## 交付

最终目录严格包含：

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

统一使用 editorial 半调纸拼贴：黑白 halftone 摄影剪贴、彩色卡纸、奶油色描边、纸张颗粒、清晰裁切边和柔和阴影。画面铺满，主要信息位于中部核心区域；顶部保留新闻标题安全区，边缘允许有不抢语义的次要装饰。四张图共用视觉语言，但各自是完整画面，不锁定同一画板或物件坐标。

## 本地控制

`config/local-control.json` 默认启用。开始处理前会检查：

```powershell
python scripts/access_control.py --check
python scripts/access_control.py --disable
python scripts/access_control.py --enable
```

停用时不会建立素材包、调用生图或导出交付目录。开关是本机操作控制，不提供不可绕过的授权。

## 开发检查

```powershell
$env:PYTHONUTF8 = '1'
python C:\Users\Administrator\.codex\skills\.system\skill-creator\scripts\quick_validate.py .
python -B -m unittest discover -s tests -p "test_*.py" -v
```

MIT 许可证和版权声明见 [LICENSE](LICENSE)。
