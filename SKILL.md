---
name: gbro-jimeng-collage-broll-audited
description: 将中文口播自动拆成四张语义侧重点不同的半调纸拼贴画面；先保存四份完整 prompt，再同批独立调用 Codex 生图，按原函数生成即梦提示词并交付五文件目录。三个内部阶段默认连续执行，不等待确认、不目视验图或自动审美重做。
compatibility: 在 Codex 环境运行；默认 9:16、约 5 秒、中文提示词、四张参考图。
---

# 插画风/XY to make

把一段约 5 秒中文口播变成一个可直接交给即梦的素材包。系统负责视觉方案、四张独立生图提示词、Codex 生图、即梦视频提示词和剪映说明；用户只把图片和视频提示词交给即梦。使用用户指定时长，未指定约 5 秒。


## 执行依据

本版恢复用户指定的《部署 vox-director 项目》聊天（01a0eb0f-a6f9-7182-9947-ee05c01e534a）实际使用的半自动流程。已从原始日志还原当时 SKILL 的写入和 Codex 生图补丁，并核对票务、微信、外卖和同题抗性淀粉案例。核对材料在 [references/execution-audit.md](references/execution-audit.md) 与 [references/execution-evidence.json](references/execution-evidence.json)。

优先复现旧聊天的实际四图设计和工具调用；不能用 GitHub 原版的一张完成静帧／单隐喻组装方案覆盖已运行的四图流程，也不能把后来失败的研究面板当标准。历史 prompt 用于审计和同题复验，不作为以后替换名词的模板。

## 三个内部阶段：默认连续执行

1. **阶段 1：方案与内部建包**：理解口播，形成核心意思、场景、关键对象、动作关系、结果冲突、色彩、四张画面及组装顺序，实际保存方案并建立原内部素材包，然后继续。
2. **阶段 2：四图生成**：先写完并保存四份完整图片 prompt，全部写入成功后，同批发出四次独立的 Codex 内置 `image_gen` 请求。按原编号保存 PNG/JPG，完成轻量文件完整性检查后继续；不调用视频模型。
3. **阶段 3：即梦素材包**：按原调用生成视频提示词，核对函数输出和文件，再复制四张图片与提示词到独立交付目录。用户从交付目录拖四张图到即梦参考图区域，再复制提示词文件。

用户只给一段口播时，默认自动完成全部阶段，不等待“通过”“图片通过”等人工确认，不主动展示中间方案、图片或 prompt。历史文件和审计记录中的确认门、验图安排保留为历史依据，不作为当前执行指令。用户明确只要方案、要求暂停或指定修改范围时，按该次指示停止或限定工作。

## 视觉规则

- 保持高级 editorial 半调纸拼贴：黑白 halftone 摄影剪贴、彩色卡纸、清晰裁切边、奶油色描边、纸张颗粒和柔和阴影。
- 默认中文、9:16、约 5 秒、无对白、无配乐。
- 画面整体铺满，不制造四周大面积空白；主要主体、关键文字和动作关系放在中部核心区域。
- 顶部是新闻标题安全区：允许有背景、纸张和次要装饰，但关键对象、关键文字和冲突结果不能只放在那里。
- 边缘可有次要元素，不能让画面空，也不能抢走中部语义。
- 不要英文乱码、无关文字、logo、水印、UI、字幕段落或四格分镜。

## 四张图的拆法

四张图根据口播实际语义设计，不机械套模板，默认承担：

1. **建立场景**：政策、平台、机构、地点或主体环境。
2. **关键对象**：票、文件、商品、人物、标识等核心对象，必要中文标签要清楚。
3. **动作关系**：对象进入、推动、连接、压入或影响场景。
4. **结果冲突**：拒绝、打叉、限制、变化或最终结论。

实际执行补充：

- 先理解目标口播和上下文，再按它的语义侧重点安排四张画面。逐张决定主要表达、核心对象、物件关系、构图与必要标签；不同图可以呈现场景、对象特写、单项结果或综合结论。
- 四张共用设计语言，各自是完整画面。不要先构造一张包含全部对象的完成图，再拆成空槽、加卡片、加连线、降刻度四个状态。
- 统一半调、纸张、描边、阴影与配色方向，不锁定四张图的同一组物件、同一位置、大小和镜头构图。可依语义延续必要物件，但不强制所有物件跨图保留；也不强制每张换底色或为了变化而换场景。
- 四种角色是默认拆分角度，不是四个时间状态。旧抗性淀粉第三张直接呈现肝脏下降数据，外卖第二、第三张表现不同主体的并列权利，都不应硬套为同一个物理装置的累计动作。
- 阶段 1 在内部方案中写明四张各自的主画面与顺序、口播含义、情绪、关键物件、布局和配色，保存后直接继续。全文只用于理解目标句。
- 保留口播的否定、条件和数量归属。第四图的最终状态以口播和本次方案为准；文件名“结果冲突”不要求每个题材都出现叉号或拒绝。

## 内部完整素材包目录

```text
YYYY-MM-DD-主题/
├── 00-使用说明.txt
├── 01-隐喻方案-待确认.txt
├── 02-四张图片提示词/
│   ├── 01-建立场景.txt
│   ├── 02-关键对象.txt
│   ├── 03-动作关系.txt
│   └── 04-结果冲突.txt
├── 03-图片/
├── 05-即梦视频提示词.txt
├── 06-剪映使用说明.txt
└── visual-spec.json
```

`03-图片` 保存 Codex 生图生成的四张最终图片。以上内部目录及全部材料照常实际生成和保存，检查仅限请求成功、文件完整性、原函数输出一致及复制哈希；不制作视觉 QA 记录。`01-隐喻方案-待确认.txt` 沿用历史文件名以保持兼容，文件名中的“待确认”不要求停止等待。用户最终从后文的独立交付目录取图和提示词，即梦只负责根据它们生成动画。

## Codex 生图规则

内部方案形成并建包后，对四个完整图片提示词同批独立调用内置 `image_gen`，不要使用 Gemini、外部图片 API 或 CLI fallback。四次调用使用当前同一 Codex 生图工具接口，不代表四种不同模型。四图生成并通过文件完整性检查后，自动进入阶段 3。

### 提示词的形成方式

1. 根据本次设计的四张画面，先写本条口播共用的风格与构图边界，再分别写每张图的主要内容。实际案例使用英文图像描述，中文标签逐字写明，使用 `Use case: ads-marketing`（按题材补充说明）及 9:16 新闻 B-roll 的用途。
2. 共用内容包括纸拼贴媒介、黑白半调摄影剪贴、卡纸点色、奶油描边、纸纹与阴影、整幅铺满、中部重要内容、顶部次要内容和禁用项。它不包含锁定四张图坐标的固定场景图。
3. 每张的内容描述写清本图主要对象、作用或结果、大小关系、环境与中文标签。主题变化时重新设计这些内容；不把一条已通过的 prompt 缩成“高级拼贴”等几个风格词，也不把旧题材换几个名词继续用。
4. 旧案例采用“本次共用风格描述 + 本图独立内容”的组织方式；这不要求未来所有 prompt 字句完全相同，也不要求四张共享具体布局。不要附加 `Fixed composition for all four stills`、`add only`、`same board`、`no major relocation` 等跨图锁定要求。
5. 图片提示词直接交给 Codex。脚本写出的中文草稿不等于实际调用文本，必须用实际完整调用 prompt 保存到 `02-四张图片提示词` 的对应文件，不能只保存一句摘要。四份实际完整 prompt 必须全部写入成功，才可发出第一个生图请求；任一文件写入失败时先修复保存，不提前生成其余图片。工具返回的 revisedPrompt 若不同，单独标明；用户要求单图修改时只处理对应图并同步文本。

### 生图调用方式

四份完整 prompt 全部保存成功后，必须实际调用 `scripts/load_image_prompts.py --project <内部项目目录>`，一次读取四份文件。该脚本遇到缺失、空白或仍为建包脚本中文草稿的文件会以非零状态退出；成功才返回按 01、02、03、04 排列的四项 JSON。不要只口头声明 prompt 已准备好。如下读取和生图代码放在同一次 `functions.exec` 内执行，将目录变量替换为本次实际路径：

```javascript
// @exec: {"yield_time_ms": 120000, "max_output_tokens": 1000}
const skillDir = "C:/Users/Administrator/.codex/skills/gbro-jimeng-collage-broll-audited";
const projectDir = "<本次已建立的内部项目绝对路径>";
const quotePS = value => "'" + value.replaceAll("'", "''") + "'";
const loaded = await tools.exec_command({
  cmd: "$env:PYTHONUTF8='1'\npython " +
    quotePS(skillDir + "/scripts/load_image_prompts.py") +
    " --project " + quotePS(projectDir),
  max_output_tokens: 16000
});
if (loaded.exit_code !== 0) throw new Error("四份 prompt 未完整保存，停止生图");
const prompts = JSON.parse(loaded.output);
if (prompts.length !== 4 || prompts.some((item, i) =>
  Number(item.number) !== i + 1 || typeof item.prompt !== "string" || !item.prompt.trim()
)) throw new Error("prompt 编号或正文不完整，停止生图");

const requestImage = async prompt => {
  const result = await tools.image_gen__imagegen({
    prompt,
    transparent_background: false
  });
  if (result?.isError === true) {
    const message = (result.content ?? [])
      .filter(item => item.type === "text")
      .map(item => item.text).join("\n");
    throw new Error(message || "image_gen 返回错误");
  }
  return result;
};
prompts.forEach(item => store("imagegen_result_" + String(item.number).padStart(2, "0"), null));
store("imagegen_batch", { projectDir, requestsSucceeded: false });
const requests = prompts.map(({ prompt }) => requestImage(prompt));
const results = await Promise.allSettled(requests);

const retryIndexes = results.flatMap((item, i) =>
  item.status === "rejected" &&
  /network|timeout|timed out|ECONNRESET|ETIMEDOUT|网络|超时/i.test(
    String(item.reason?.message ?? item.reason)
  ) ? [i] : []
);
if (retryIndexes.length) {
  const retried = await Promise.allSettled(retryIndexes.map(i => requestImage(prompts[i].prompt)));
  retried.forEach((item, i) => { results[retryIndexes[i]] = item; });
}
const failed = [];
results.forEach((item, i) => {
  const number = String(i + 1).padStart(2, "0");
  if (item.status === "fulfilled") store("imagegen_result_" + number, item.value);
  else failed.push(number);
});
store("imagegen_batch", { projectDir, requestsSucceeded: failed.length === 0, failed });
text({ projectDir, savedResultNumbers: prompts.map(item => String(item.number).padStart(2, "0")).filter(number => !failed.includes(number)), failed });
if (failed.length) throw new Error("仍缺少成功请求：" + failed.join("、") + "；停止阶段 3 与最终导出");
// 后续用 load("imagegen_result_01") 等读取实际工具结果中的路径，复制原图并检查文件。
```

初次生成四图时，四次请求必须在同一批启动，不逐张 `await`，不以串行调用作为兜底；实际服务端调度由工具决定，不声称四张会同时完成。不传 `referenced_image_paths`，也不传 `num_last_images_to_include`，不将前一张传给后一张。用户明确要求修改某张图时，再按该张修改要求处理，不扩展成整组编辑链。

`Promise.allSettled` 返回结果按原输入索引对应图片编号：`results[0]` 对应 01，以此类推；不能按完成先后重新编号。请求拒绝或返回 `isError: true` 都算失败；成功结果用 `store` 按编号保留，避免 `functions.exec` 结束后丢失局部变量，后续通过 `load` 读取实际输出路径。不要用 `text` 打印完整图片结果或 base64。逐项确认请求成功、对应输出文件存在且非空，按索引把原图复制到项目 `03-图片/01-建立场景.png` 至 `04-结果冲突.png`，保留实际文件格式。四个编号必须各有一张最终文件；任一不满足时停止阶段 3 与最终导出。

仅遇到网络错误或超时导致的技术性请求失败时，用同一个已保存 prompt 对失败编号补试一次；多个失败项一起提交，成功项保留，不重新请求。补试结果仍对应原编号。其他报错、输出文件缺失／为空或补试后仍失败时，保留成功图片，如实报告缺项，不生成或交付冒充完整成功的五文件目录。不得因构图、文字效果或审美判断自动重做图片。

生成后不调用 `view_image` 目视验图，不制作拼版或视觉 QA 报告，不展示图片等待审批，也不做自动审美返工。轻量检查仅确认请求成功、文件存在非空及编号完整，不据此宣称画面中文字正确、构图合格或视觉效果通过。画面比例与设计规则继续写入 prompt；若报告尺寸，只使用实际读取到的文件元数据，不冒称精确 1080×1920。文件完整后自动继续阶段 3。


## 本地半自动脚本

恢复旧聊天实际调用的 `scripts/make_package.py`，使用系统 Python。脚本内容直接从当时的创建及补丁记录还原。它不调用 AI、不理解口播，只接收模型已经设计的本次内容，建立原有文件夹、元数据和草稿。其中 `video_prompt(speech, scene, objects, action, result, palette, duration=5)` 保留旧聊天实际生成视频提示词的六个内容参数，新增可选时长；原六参数调用仍默认 5 秒。固定文字及原有举例来自这段源码，继续实际调用，不从旧输出重新概括模板。

阶段 1 方案形成后运行，参数来自本次方案：

```text
python <本Skill目录>/scripts/make_package.py
  --speech <目标口播> --title <主题>
  --scene <本次场景> --objects <本次对象>
  --action <本次关系> --result <本次结果> --palette <本次配色>
  --output <用户指定或当前工作目录中的素材包目录> --date <本次日期>
  --duration <用户指定秒数，未指定为5>
```

然后为四张画面分别写实际完整生图 prompt，覆盖全部四份对应草稿；四份文件全部保存成功后，按上节同批调用 image_gen。默认保留脚本的目录与 visual-spec.json；不再强制额外设计一个供四图共用的固定面板、统一坐标系统或单场景运动规格。

历史脚本会提前写出视频提示词草稿；`--duration` 接受正的有限秒数，默认 5，用户指定 6 秒时传入 6，由脚本同步时长。草稿存在不代表阶段 3 已完成。四图文件完整后，按下节用同一脚本的 `--video-only` 实际调用原函数生成最终文件；不要重新运行整包生成来覆盖已有图片、生图提示词或元数据。固定段落包括叉号／封条等原举例保持源码原文，本次具体结果由 `result` 参数提供，不自行优化固定段落。

## 阶段 3：原函数生成视频提示词并交付

四图请求成功且文件完整后自动执行，不等待用户确认、不查看图片内容。核对六个参数与目标口播、本次方案及已保存的四份完整生图 prompt 一致：`speech` 为目标口播，`scene` 为本次场景，`objects` 为本次对象，`action` 为本次对象关系，`result` 为本次结果，`palette` 为本次配色。沿用本次参数；必要修正落实到对应参数后重跑。不得把分秒导演稿、四张完整画面轮流滑出／换入、翻页转场等新流程塞进参数，绕过原函数的动画顺序。

必须实际执行已有脚本，由它将六个内容参数及本次 `duration` 传给 `video_prompt()`：

```text
python <本Skill目录>/scripts/make_package.py
  --speech <目标口播> --title <与建包时相同的主题>
  --scene <本次场景> --objects <本次对象>
  --action <本次关系> --result <本次结果> --palette <本次配色>
  --output <与建包时相同的素材包父目录> --date <与建包时相同的日期>
  --video-only --duration <用户指定秒数，未指定为5>
```

`--output`、`--title`、`--date` 必须定位到已有项目。`--video-only` 只覆盖该项目的 `05-即梦视频提示词.txt`，项目不存在则报错，不创建新目录，也不改其他文件。函数只将首句时长按 `duration` 生成；除时长外，原函数的固定文字、顺序和举例不改。不得用模型自由撰写的文字、输出对比提炼的规则或其他模板代替这次实际调用；生成后不再改写成分秒导演稿，也不手工覆盖文件。

交付前确认命令成功，读取实际写入的 `05-即梦视频提示词.txt`；核对文件全文等于本次 `video_prompt()` 返回值规范末尾换行后的文本，并核对本次操作前后图片及实际生图提示词的哈希未变。若调用失败，修复调用后重跑，不用临时撰写的提示词冒充脚本结果。

完成上述实际调用与检查后，按下节复制四张最终图片和该文件到独立交付目录，用户从交付目录拖图并复制提示词正文，视频生成后自行放进剪映。原函数中的固定视角、逐件组装等要求仅在本阶段执行，不回写成四张静帧共用同一构图的限制。不添加未经确认的即梦功能或视频 API；不把助手曾建议过某个选项说成用户已实际操作过。

## 最终交付目录

这是三个内部阶段完成后的复制步骤，不设人工确认门。完整内部素材包、四份实际生图 prompt、同批四次请求、文件完整性检查、原 `video_prompt()` 调用和返回值核对都必须照常完成；不能因为内部材料不放进交付目录，就省略其实际生成或轻量核对。阶段完成依据真实调用与文件记录，不依赖用户审批或 `visual-spec.json` 的 `status` 字段，也不能只因05文件已经存在就认定阶段 3 完成。这里不恢复目视验图、视觉 QA 或自动审美重做。

完成后实际运行：

```text
python <本Skill目录>/scripts/export_delivery.py
  --project <已完成并检查的内部完整项目目录>
  --output <独立最终目标目录>
```

默认目标为 `<内部项目父目录>/交付/<内部项目名>`。同名目标已存在时另建 `<内部项目名>_02`、`_03` 等新的目录，不合并或覆盖旧交付内容。交付目录与内部项目分开，内部文件继续保留。

交付目录只含以下五个文件，保留实际图片的文件名及 PNG/JPG/JPEG 扩展名：

```text
交付/YYYY-MM-DD-主题/
├── 01-建立场景.png
├── 02-关键对象.png
├── 03-动作关系.png
├── 04-结果冲突.png
└── 05-即梦视频提示词.txt
```

导出器只对白名单中的四个编号各选唯一一张最终 PNG/JPG/JPEG，以及非空的 `05-即梦视频提示词.txt`，原字节复制并核对源文件与目标文件的哈希。缺图、同编号存在多个候选、提示词为空或哈希不一致时不交付成功；不复制 `README`、草稿、方案、spec、检查记录、缩略图或旧版本。不把整个内部图片目录直接复制过去。

导出及重新导出都只复制已完成的原文件，不再次调用生图、重写提示词、调整文字换行、压缩图片、转码或重新保存图片。确认五个文件的数量与哈希正确后，最终回复只链接交付目录，让用户直接取四张图和提示词。


## 边界

不调用 Gemini、Veo、Google SDK 或任何视频生成 API；不自动上传即梦；不生成剪映工程文件。最终视频由用户在即梦生成，再放入剪映对应口播下方。
