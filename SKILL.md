---
name: gbro-jimeng-collage-broll-audited
description: 将中文口播自动转成四张语义独立的半调纸拼贴参考图和一份即梦视频提示词；先保存四份完整生图 Prompt，再同批独立调用 Codex 生图，完成五文件交付。
---

# 插画风 / XY to make

把一段中文口播转成可直接交给即梦的新闻短视频 B-roll 素材。默认自动完成内部方案、四图生图、视频提示词和交付导出，不等待人工确认，不展示中间材料。

## 开始前：本地控制

第一步必须检查本地开关，且在检查成功前不要建立目录、写文件或调用模型：

```javascript
const skillDir = "C:/Users/Administrator/.codex/skills/gbro-jimeng-collage-broll-audited";
const quotePS = value => "'" + value.replaceAll("'", "''") + "'";
const access = await tools.exec_command({
  cmd: "$env:PYTHONUTF8='1'\npython " + quotePS(skillDir + "/scripts/access_control.py") + " --check",
  max_output_tokens: 2000
});
if (access.exit_code !== 0) throw new Error("当前 Skill 已停用或本地控制配置无效，停止本次处理");
```

用户可以在 Skill 目录运行：

```text
python scripts/access_control.py --disable
python scripts/access_control.py --enable
```

停用时停止全部生成和导出；启用后继续执行下面的完整流程。开关是透明的本机操作控制，不联网，也不提供不可绕过的代码授权。

## 固定执行链

### 阶段 1：理解口播并建立内部素材包

从本次中文口播提炼：核心场景、关键对象、动作关系、最终结果和配色，并为四张图分别安排完整画面。全文只用于理解目标句，不把全文直接塞进画面。

实际运行：

```text
python <Skill目录>/scripts/make_package.py
  --speech <目标口播> --title <主题>
  --scene <本次场景> --objects <本次对象>
  --action <本次动作关系> --result <本次最终结果>
  --palette <本次配色> --output <素材包父目录>
  --date <日期> --duration <秒数，默认5>
```

脚本建立完整内部目录并写出四份待替换的 Prompt 草稿。草稿必须被本次实际完整生图 Prompt 覆盖，不能直接拿草稿调用生图。

### 阶段 2：四张独立参考图

四份完整 Prompt 全部保存成功后，运行一次：

```text
python <Skill目录>/scripts/load_image_prompts.py --project <内部项目目录>
```

只有命令成功并返回四项按 01、02、03、04 排列的 JSON，才允许发出生图请求。

四次请求必须在同一批启动，使用同一个 Codex `image_gen` 工具：

```javascript
const loaded = await tools.exec_command({
  cmd: "$env:PYTHONUTF8='1'\npython " +
    quotePS(skillDir + "/scripts/load_image_prompts.py") +
    " --project " + quotePS(projectDir),
  max_output_tokens: 16000
});
if (loaded.exit_code !== 0) throw new Error("四份 Prompt 未完整保存，停止生图");
const prompts = JSON.parse(loaded.output);
if (prompts.length !== 4 || prompts.some((item, i) =>
  Number(item.number) !== i + 1 || typeof item.prompt !== "string" || !item.prompt.trim()
)) throw new Error("Prompt 编号或正文不完整，停止生图");

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

调用要求：

- 四份 Prompt 全部保存后才启动第一批请求；不逐张等待，不使用串行兜底。
- 不传前图引用，不把前一张图作为后一张的编辑输入。
- 按原输入索引保存结果，完成先后不改变图片编号。
- 只对网络或超时失败的编号补试一次；成功图片不重做。
- 不调用 `view_image`，不制作拼图，不做视觉 QA，不因审美判断自动重生。
- 四个编号都成功且文件存在、非空后，才进入阶段 3；否则说明缺项并停止交付。

### 阶段 3：生成即梦提示词并导出

四图完整后，使用同一份六参数方案重新运行脚本：

```text
python <Skill目录>/scripts/make_package.py
  --speech <目标口播> --title <相同主题>
  --scene <相同场景> --objects <相同对象>
  --action <相同动作关系> --result <相同最终结果>
  --palette <相同配色> --output <相同素材包父目录>
  --date <相同日期> --duration <秒数，默认5> --video-only
```

`--video-only` 只覆盖已有项目的 `05-即梦视频提示词.txt`。必须核对该文件等于本次 `video_prompt()` 返回值；不得改写成逐秒分镜稿或临时手写提示词。

确认四张图片、四份实际 Prompt、视频提示词和文件完整性后，运行：

```text
python <Skill目录>/scripts/export_delivery.py \
  --project <已完成的内部项目目录> \
  --output <独立交付目录>
```

导出器只复制四张唯一编号图片和非空的 `05-即梦视频提示词.txt`，保留扩展名、原始字节和哈希。交付目录存在时创建 `_02`、`_03` 等新版本；缺图、重复编号、空提示词或哈希不一致时停止。

## 视觉规则

- 高级 editorial 半调纸拼贴：黑白 halftone 摄影剪贴、彩色卡纸、奶油色描边、纸张颗粒和柔和阴影。
- 默认中文、9:16、画面铺满、无对白、无配乐。
- 主要主体、关键文字和动作关系位于中部核心区域；顶部只放背景和次要装饰，留给新闻标题。
- 边缘可以有次要纸片填充，但不能抢走中部语义。
- 四张图是四个语义侧重点各自完整的画面，不锁定同一画板、同一组物件或同一套坐标。
- 根据本次口播重新设计场景、对象、动作和结果；保持否定关系、数量归属和必要中文标签。
- 不要英文乱码、无关文字、Logo、水印、UI、字幕段落或四格分镜。

四张图默认承担四种设计角度：

1. 建立场景：地点、机构、平台、政策或主体环境。
2. 关键对象：票、文件、商品、人物、标识或数据对象。
3. 动作关系：对象之间正在发生的进入、连接、推动、限制或影响。
4. 结果冲突：最终变化、限制、拒绝、结论或并列结果。

这四种角度不是同一画板的四个时间状态。画面可以根据口播变化主角、景别和构图，同时保持统一纸拼贴设计语言。

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
