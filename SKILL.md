---
name: gbro-jimeng-collage-broll-audited
description: 将中文口播自动转成四张语义独立的半调纸拼贴参考图和一份即梦视频提示词；内部先完成详细四图方案与完整 Prompt，再同批独立调用 Codex 生图，最后交付五文件目录。
---

# 插画风 / XY to make

把一段中文口播转成可直接交给即梦的新闻短视频 B-roll 素材。内部完整执行方案拆解、四图 Prompt、生图、视频提示词和交付导出；用户不需要回复确认，最终只拿四张图片和一份即梦提示词。

## 开始前：本地控制

第一步必须检查本地开关，在检查成功前不要建立目录、写文件或调用模型：

```javascript
const skillDir = "C:/Users/Administrator/.codex/skills/gbro-jimeng-collage-broll-audited";
const quotePS = value => "'" + value.replaceAll("'", "''") + "'";
const access = await tools.exec_command({
  cmd: "$env:PYTHONUTF8='1'\npython " + quotePS(skillDir + "/scripts/access_control.py") + " --check",
  max_output_tokens: 2000
});
if (access.exit_code !== 0) throw new Error("当前 Skill 已停用或本地控制配置无效，停止本次处理");
```

## 固定执行链（自动完成，不向用户请求确认）

### 阶段 1：先理解口播，再形成详细四图方案

先从目标口播提炼：核心意思、情绪、场景、关键对象、动作关系、最终结果、数字和否定条件、必要中文标签、配色。然后在内部为四张图分别写清：

1. 建立场景：地点、机构、环境或主体，说明观众先看到什么。
2. 关键对象：本句最重要的对象、大小关系、材质、标签和数量归属。
3. 动作关系：对象之间具体发生的进入、连接、推动、限制、影响或并列关系。
4. 结果冲突：最终变化、结论、拒绝、限制、等待或对比结果。

四张是四个各自完整的语义画面，共用纸拼贴视觉语言，但不锁定同一画板、同一组物件、同一坐标或同一时间状态。保留口播中的否定、条件、数字和归属关系。不要把整句口播直接当成画面文字，也不要先做一张总图再拆成四个小变化。

用 `scripts/make_package.py` 建立内部素材包。`01-隐喻方案-待确认.txt` 只是历史兼容文件名，内部完成后继续，不等待用户确认。

参数必须来自本次实际方案：

```text
python <Skill目录>/scripts/make_package.py \
  --speech <目标口播> --title <主题> \
  --scene <本次场景> --objects <本次对象> \
  --action <本次动作关系> --result <本次最终结果> \
  --palette <本次配色> --output <素材包父目录> \
  --date <日期> --duration <秒数，默认5>
```

脚本生成的四份文件只是待替换草稿；模型必须把本次实际完整 Prompt 写回对应文件，不能把草稿直接交给生图工具。

### 阶段 2：写完整 Prompt，再四路并行生图

必须先写完四份实际生图 Prompt，再运行：

```text
python <Skill目录>/scripts/load_image_prompts.py --project <内部项目目录>
```

命令成功且返回四项按 01、02、03、04 排列的完整文本后，才启动第一批生图。若仍是脚本中文草稿、缺字、空白或编号错误，先补全并重新加载，不能提前生图。

每份实际 Prompt 必须达到老流程的完整度，不能只写“高级拼贴 + 场景/对象/动作/结果”概括。Prompt 按下面顺序组织：

1. **用途与画幅**：`Use case: ads-marketing`（按题材补充用途）、独立的 9:16 portrait still、新闻 B-roll。
2. **共用视觉语言**：editorial halftone paper collage、黑白半调摄影剪贴、彩色卡纸、奶油描边、纸张颗粒、裁切边、柔和纸张阴影、平面二维定格质感、非 glossy 3D。
3. **构图边界**：画面铺满；重要主体、关系和文字在中部核心区；顶部约 20% 仅放背景和次要装饰，作为新闻标题安全区。
4. **本图独立内容**：明确本图主角、对象、环境、前后关系、大小关系、动作或结果、景别和构图，不用泛化词代替具体物件。
5. **文字与数量**：中文标签逐字写出；明确“只允许出现哪些文字”；数量、排列和归属写成可数的画面约束，例如“exactly fourteen…two rows of seven”，禁止把数字语义压成模糊词。
6. **负面限制**：不要 logo、水印、UI、英文乱码、随机文字、字幕段落、四格分镜、无关人物或物件；题材有特殊排除项时逐条写明。

实际 Prompt 可用英文描述视觉和构图，中文标签必须原样放在引号中。每张图要根据本次口播重新设计，不能把历史题材换名词套用，也不能缩成几个风格词。不要加入 `same board`、`fixed composition for all four stills`、`add only`、`no major relocation` 等锁死四张画面的限制。

四份 Prompt 全部写入后，在同一批中发出四次独立 Codex `image_gen` 请求：不传前图引用，不按完成先后重新编号，不串行等待。使用 `Promise.allSettled` 收齐；只对网络或超时失败的编号补试一次，成功图片保留。生成后只做请求成功、文件存在且非空、编号完整的轻量检查，不调用 `view_image`，不制作视觉 QA，不因审美判断自动重做。

调用骨架：

```javascript
const loaded = await tools.exec_command({
  cmd: "$env:PYTHONUTF8='1'\npython " + quotePS(skillDir + "/scripts/load_image_prompts.py") +
    " --project " + quotePS(projectDir),
  max_output_tokens: 16000
});
if (loaded.exit_code !== 0) throw new Error("四份实际 Prompt 未完整保存，停止生图");
const prompts = JSON.parse(loaded.output);
if (prompts.length !== 4 || prompts.some((item, i) =>
  Number(item.number) !== i + 1 || typeof item.prompt !== "string" || !item.prompt.trim()
)) throw new Error("Prompt 编号或正文不完整，停止生图");

const requestImage = async prompt => {
  const result = await tools.image_gen__imagegen({ prompt, transparent_background: false });
  if (result?.isError === true) {
    const message = (result.content ?? []).filter(item => item.type === "text")
      .map(item => item.text).join("\n");
    throw new Error(message || "image_gen 返回错误");
  }
  return result;
};
const requests = prompts.map(({ prompt }) => requestImage(prompt));
const results = await Promise.allSettled(requests);
const retryIndexes = results.flatMap((item, i) =>
  item.status === "rejected" &&
  /network|timeout|timed out|ECONNRESET|ETIMEDOUT|网络|超时/i.test(
    String(item.reason?.message ?? item.reason)
  ) ? [i] : []
);
if (retryIndexes.length) {
  const retried = await Promise.allSettled(
    retryIndexes.map(i => requestImage(prompts[i].prompt))
  );
  retried.forEach((item, i) => { results[retryIndexes[i]] = item; });
}
const failed = [];
results.forEach((item, i) => {
  const number = String(i + 1).padStart(2, "0");
  if (item.status === "fulfilled") store("imagegen_result_" + number, item.value);
  else failed.push(number);
});
if (failed.length) throw new Error("仍缺少成功请求：" + failed.join("、"));
```

`results[0]` 永远对应 01，依此类推；完成先后不能改变编号。成功结果用 `store` 按编号保留，随后读取工具返回的实际图片路径，按原索引复制到内部 `03-图片/01-建立场景` 至 `04-结果冲突`，保留实际扩展名。四个编号都必须存在且非空，才进入阶段 3；失败项如实保留并停止最终导出。

### 阶段 3：原函数生成即梦提示词并导出

四图文件完整后，使用同一份六参数方案运行：

```text
python <Skill目录>/scripts/make_package.py \
  --speech <目标口播> --title <相同主题> \
  --scene <相同场景> --objects <相同对象> \
  --action <相同动作关系> --result <相同最终结果> \
  --palette <相同配色> --output <相同素材包父目录> \
  --date <相同日期> --duration <时长> --video-only
```

该命令只更新已有项目的 `05-即梦视频提示词.txt`。必须核对文件全文等于原 `video_prompt()` 返回值；不得自由改写成逐秒分镜稿。

然后运行：

```text
python <Skill目录>/scripts/export_delivery.py \
  --project <内部项目目录> \
  --output <独立交付目录>
```

导出器只复制四张唯一编号图片和非空的 `05-即梦视频提示词.txt`，原字节复制并校验哈希。缺图、重复编号、空提示词或哈希不一致时停止交付；已有同名目录时创建编号版本。

## 视觉规则

- 高级 editorial 半调纸拼贴：黑白 halftone 摄影剪贴、彩色卡纸、奶油色描边、纸张颗粒、清晰裁切边和柔和阴影。
- 默认中文、9:16、画面铺满、无对白、无配乐。
- 主要主体、关键文字和动作关系位于中部核心区域；顶部只放背景和不重要的装饰，留给新闻标题。
- 边缘可以有次要纸片填充，但不能抢走中部语义。
- 四张图是四个语义侧重点各自完整的画面，不是同一画板的四个时间状态。
- 不要英文乱码、无关文字、Logo、水印、UI、字幕段落或四格分镜。

## 内部目录和最终交付

内部项目保留完整材料：

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

最终只向用户交付：

```text
交付/YYYY-MM-DD-主题/
├── 01-建立场景.png
├── 02-关键对象.png
├── 03-动作关系.png
├── 04-结果冲突.png
└── 05-即梦视频提示词.txt
```

## 边界

不自动上传即梦，不生成剪映工程文件，不调用视频生成 API。用户在即梦生成视频后，再自行放入剪映对应口播下方。
