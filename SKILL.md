---
name: gbro-jimeng-collage-broll-audited
description: 将中文口播转成四张各自独立的半调纸拼贴参考图和即梦视频提示词；AI 为每张图写完整生图 Prompt，程序只按编号保存、校验并交付。
---

# 插画风/XY to make（逐图提示词试用）

本试用版恢复旧流程中真正有效的提示词链：

```text
中文口播 → AI 分别设计四个语义画面 → 四条完整独立生图 Prompt
→ 四路同批 Codex image_gen → 原 video_prompt() → 五文件交付
```

不要把场景、对象、动作和结果五参数重复塞入四张图，也不要把一张完整画面拆成四个连续状态。四张图共用半调纸拼贴、9:16、中部核心和顶部标题安全区等视觉规则；每张图的主体、动作、文字、数量、结果和排除项必须按本次口播独立设计。

## 开始前

本 Skill 仅显式调用，不替代正式版。先运行 `scripts/access_control.py --check`；失败时停止，不建立素材包或调用模型。通过后默认自动完成内部三个阶段，不请求人工确认。

## 阶段 1：逐图方案与建包

阅读 [references/image-plan.md](references/image-plan.md)。新任务使用 schema/template `3`，由 AI 为四张图分别写完整 Prompt，并在内部保留原 `video_prompt()` 所需的 `scene`、`objects`、`action`、`result`、`palette` 五个视频内容参数。

每张完整 Prompt 必须保留旧流程的共用标记：`Use case:`、`9:16`、`Premium editorial halftone paper collage`、`middle core`、顶部新闻标题安全区，以及 `no English`、`no logo`、`no watermark`、`no UI`、`no subtitles`、`no 3D`。每张都要有独立的主体和排除规则；不能出现 `same board`、`fixed composition for all four`、`no major relocation` 等锁死四张画面的句子。

运行：

```text
python <Skill目录>/scripts/prepare_package.py \
  --plan <schema3参数JSON> --output <独立内部父目录> --date <YYYY-MM-DD>
```

`image-plan.json` 保存四个 `frames[n].prompt` 的完整正文。程序不改写 Prompt，只按输入编号增加一个文件末尾换行。旧 schema1/schema2 记录可读取和重渲染，但不能用于新建素材包；需要修正时编辑 plan 后运行 `render_image_prompts.py`。

## 阶段 2：逐图 Prompt 校验与生图

先运行 `scripts/load_image_prompts.py --project <内部项目目录>`。它会把保存的四份文件与 schema3 plan 逐字比较；缺失、被手改、重复或缺少固定视觉/负面标记时停止。

四份完整 Prompt 全部加载成功后，在同一批中发出四次独立 `image_gen` 请求：

- 使用 `transparent_background: false`；
- 不传 `referenced_image_paths` 或 `num_last_images_to_include`；
- 用 `Promise.allSettled` 收齐，结果按输入索引对应 01—04；
- 只有网络或超时错误可对失败编号补试一次；
- 不调用 `view_image`，不制作视觉 QA，不因审美自动重做。

将四张成功图片按原编号复制到 `03-图片`。编号不全或文件为空时停止，不进入视频提示词和最终导出。

## 阶段 3：视频提示词与交付

四图完整后，使用同一份五参数和时长调用 `scripts/make_package.py --video-only`。文件 `05-即梦视频提示词.txt` 必须等于原 `video_prompt()` 返回值，不得自由改写成逐秒分镜稿。

最后运行 `scripts/export_delivery.py`。最终目录严格只有四张图片和 `05-即梦视频提示词.txt`，用户把它们交给即梦后自行在剪映剪辑。

## 旧流程回放验收

`tests/fixtures/v3/golden_old_thread_01a11588.json` 保存用户确认过的线程 `01a11588-eadf-7280-abf1-3f0989ad7d35` 四条 `imageGeneration.revisedPrompt`，只用于回放验证，不作为以后替换名词的模板。修改 v3 后必须运行：

```text
python -m unittest discover -s <Skill目录>/tests -q
```

测试必须证明四条旧 Prompt 逐字一致（只统一换行符比较）、同一 plan 重渲染一致、只改一帧只影响该帧、手改文件会被阻止，以及视频函数和五文件交付结构未变。通过文本回放不代表随机生图像素完全相同。

正式 Skill、旧素材包和 GitHub 主分支不在本试用版修改范围内。
