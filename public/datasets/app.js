const legacyDatasets = Array.isArray(window.DATASET_CATALOG) ? window.DATASET_CATALOG : [];
const masterDatasets = Array.isArray(window.MASTER_DATASET_CATALOG) ? window.MASTER_DATASET_CATALOG : [];
const recentResources = Array.isArray(window.RECENT_RESOURCES) ? window.RECENT_RESOURCES : [];
const recentResourceStats = window.RECENT_RESOURCE_STATS || {};
const collectionImpact = Array.isArray(window.COLLECTION_IMPACT) ? window.COLLECTION_IMPACT : [];
const legacyByName = new Map(legacyDatasets.map((item) => [item.name.toLowerCase(), item]));
const datasets = masterDatasets.length
  ? masterDatasets.map((item) => ({ ...(legacyByName.get(item.name.toLowerCase()) || {}), ...item }))
  : legacyDatasets;

const collectionSystems = [
  {
    name: "ALOHA / GELLO", type: "机械同构", priority: 6, focus: "通用采集基础", copy: "用与目标机械臂结构相近的leader设备直接控制机器人。", tradeoff: "高精度 · 低跨本体",
    image: "./images/collection/aloha.png", imageAlt: "ALOHA双臂操作与ACT动作序列示意", imageCredit: "ALOHA官方项目",
    contains: "通常记录多视角RGB、机器人关节状态和leader产生的关节目标。ALOHA公开示例以HDF5 episode保存；GELLO主要公开采集软硬件，而不是一个统一的大规模数据集。",
    use: "搭建并标定leader设备，遥操作完成任务，同步记录相机、关节状态和关节目标；筛选成功episode后，可用于行为克隆或ACT等模仿学习方法。",
    links: [{ label: "ALOHA项目", url: "https://tonyzhaozh.github.io/aloha/" }, { label: "GELLO项目", url: "https://wuphilipp.github.io/gello_site/" }],
  },
  {
    name: "BridgeData / DROID", type: "VR / 手柄", priority: 7, focus: "通用采集基础", copy: "用VR控制器或手柄在多场景、多站点采集真实机械臂轨迹。", tradeoff: "跨场景强 · 数据规模大",
    image: "./images/collection/droid.png", imageAlt: "DROID便携式机器人数据采集装置", imageCredit: "DROID官方项目",
    contains: "BridgeData V2包含约6万条轨迹；DROID包含约7.6万条、350小时的多场景操作数据。常见字段有多视角RGB、机器人状态、动作、语言和相机标定。",
    use: "可从RLDS/TFDS或项目loader读取episode，先确认动作坐标系、控制频率与相机字段，再用于行为克隆、VLA预训练或跨场景泛化实验。",
    links: [{ label: "BridgeData V2", url: "https://rail-berkeley.github.io/bridgedata/" }, { label: "DROID", url: "https://droid-dataset.github.io/" }],
  },
  {
    name: "RH20T", type: "力反馈工作站", priority: 8, focus: "通用采集基础", copy: "通过力反馈设备采集接触丰富的多模态机器人操作。", tradeoff: "多模态强 · 标定复杂",
    image: "./images/collection/rh20t.png", imageAlt: "RH20T力反馈、多相机与机器人采集工作站", imageCredit: "RH20T官方项目",
    contains: "包含11万余段序列，覆盖多视角RGB-D、关节与TCP状态、力/力矩、音频和部分触觉，并提供多种机器人配置及配对人体示范。",
    use: "先按任务和机器人配置下载数据包，使用官方API读取并校准不同传感器；训练前通常还要统一频率、选择模态并转换为模型需要的episode格式。",
    links: [{ label: "RH20T项目与数据", url: "https://rh20t.github.io/" }, { label: "RH20T API", url: "https://github.com/rh20t/rh20t_api" }],
  },
  {
    name: "UMI", type: "手持 robot-free", priority: 5, focus: "跨本体上游", copy: "用手持夹爪在机器人不到场时采集真实环境示范。", tradeoff: "高吞吐 · 需可行性修复",
    image: "./images/collection/umi.png", imageAlt: "UMI手持式robot-free采集设备与应用示例", imageCredit: "UMI官方项目",
    contains: "主要记录手持设备的RGB视频、SLAM恢复的相机/夹爪轨迹和夹爪状态。它是人类示范，不天然包含目标机器人的关节状态和可直接执行动作。",
    use: "完成相机与夹爪标定后采集视频，用SLAM恢复轨迹，再结合目标机器人的工作空间、碰撞和控制约束转换动作，常用于Diffusion Policy等模仿学习管线。",
    links: [{ label: "UMI项目", url: "https://umi-gripper.github.io/" }, { label: "UMI代码", url: "https://github.com/real-stanford/universal_manipulation_interface" }],
  },
  {
    name: "HumanPlus", type: "视觉人体", priority: 2, focus: "Full-body优先", copy: "从人体视频和姿态估计生成humanoid全身动作参考与任务示范。", tradeoff: "便携 · 易受遮挡影响",
    image: "./images/collection/humanplus.gif", imageAlt: "HumanPlus人体示范到humanoid全身动作映射", imageCredit: "HumanPlus官方项目",
    contains: "包含人体RGB姿态、机器人本体、第一视角RGB和全身动作，并公开代码、模型及部分运动先验与任务资源。",
    use: "先估计人体姿态，再做人体到机器人的retargeting。用于Full-body时还需低层全身控制器、平衡和接触约束，不能把人体关键点直接当作机器人关节命令。",
    links: [{ label: "HumanPlus项目", url: "https://humanoid-ai.github.io/" }, { label: "HumanPlus代码", url: "https://github.com/MarkFzp/humanplus" }],
  },
  {
    name: "H2O / OmniH2O", type: "全身运动目标", priority: 1, focus: "Full-body优先", copy: "把人体全身姿态转换为humanoid参考动作并由低层策略执行。", tradeoff: "全身自然 · 控制链更长",
    image: "./images/collection/omnih2o.png", imageAlt: "OmniH2O人体动作重定向、仿真训练和真实部署流程", imageCredit: "OmniH2O官方项目",
    contains: "包含人体姿态、机器人本体状态、动作和任务观测；OmniH2O还公开6项日常任务数据。重点是全身运动参考与控制，而非传统单臂episode集合。",
    use: "将人体动作retarget为机器人参考运动，在仿真中训练全身跟踪策略，再部署到真实humanoid；做任务学习时还要额外记录视觉、物体状态和任务结果。",
    links: [{ label: "H2O", url: "https://human2humanoid.com/" }, { label: "OmniH2O", url: "https://omni.human2humanoid.com/" }],
  },
  {
    name: "TWIST", type: "MoCap + RL/BC", priority: 3, focus: "Full-body优先", copy: "用动作捕捉采集腿、躯干和双臂协同的全身运动。", tradeoff: "全身精度高 · 场地成本高",
    image: "./images/collection/twist.png", imageAlt: "TWIST全身模仿系统官方横幅", imageCredit: "TWIST官方仓库",
    contains: "公开内容包括MoCap人体动作、训练用运动数据、模型和代码，覆盖全身操作、腿部操作、locomotion与表达动作；它不是一个统一的多任务机器人数据集。",
    use: "通过MoCap采集目标运动，retarget到humanoid，再用强化学习或行为克隆训练跟踪策略；需保留接触、根部姿态和原始/转换后动作以检查误差。",
    links: [{ label: "TWIST项目", url: "https://yanjieze.com/projects/TWIST/" }, { label: "TWIST代码", url: "https://github.com/YanjieZe/TWIST" }],
  },
  {
    name: "Open-TeleVision / AnyTeleop", type: "沉浸式视觉遥操作", priority: 4, focus: "Full-body扩展", copy: "用头显、手部跟踪和主动视觉控制humanoid上身、双臂与灵巧手。", tradeoff: "跨平台强 · 需重定向",
    contains: "Open-TeleVision侧重沉浸式主动视觉和humanoid上身/双臂；AnyTeleop覆盖多机械臂与灵巧手。两者通常产出视觉、本体状态、手/臂动作和相机位姿，但下游轨迹分散在各项目中，不构成单一数据集。",
    use: "先标定头显、相机和机器人坐标系，再将人体手臂/手部动作重定向为机器人命令。若扩展到真正Full-body，还需另接腿部运动、平衡与安全控制器。",
    links: [{ label: "Open-TeleVision", url: "https://robot-tv.github.io/" }, { label: "AnyTeleop", url: "https://yzqin.github.io/anyteleop/" }],
  },
];

collectionSystems.sort((a, b) => a.priority - b.priority);
const collectionImpactByName = new Map(collectionImpact.map((item) => [item.name, item]));
collectionSystems.forEach((item) => Object.assign(item, collectionImpactByName.get(item.name) || {}));
// Keep directory cards consistent with the dedicated collection-system impact audit.
// Some system rows were originally matched only by their project page and therefore
// carried a zero citation count even though the same paper was verified in the
// collection audit (for example, TWIST). Prefer the audited value when available.
datasets.forEach((item) => {
  const impact = collectionImpactByName.get(item.name);
  if (!impact) return;
  if (Number(impact.citation_count || 0) > Number(item.citation_count || 0)) item.citation_count = impact.citation_count;
  if (Number(impact.impact_score || 0) > Number(item.impact_score || 0)) item.impact_score = impact.impact_score;
  if (item.resource_type === "采集系统" && impact.citation_count) item.influence_tier = item.influence_tier === "新近/小众" ? "较高影响" : item.influence_tier;
});

const datasetSupplements = {
  "open-x-embodiment-aggregate": {
    resourceType: "聚合数据集",
    subdatasetCount: "72个独立子数据集",
    registeredCount: "69项进入Open X注册下载清单；3项需从原项目获取",
    scopeCount: "62项首次公开于2022—2024；其余10项为2018—2021年的基础数据",
    contentSummary: "子集覆盖单臂、双臂、移动操作、导航及少量四足平台，采集方式、控制频率、相机数量和动作空间各不相同。Open X的作用是把它们转换为RLDS并提供统一入口，不是重新采集一套同质数据。",
    episodeSizeSummary: "67项同时披露episode数和下载体积：加权平均约3.80 MB/episode；按数据集分别计算的中位数约11.36 MB；第1—第3四分位约3.05—27.45 MB；范围约0.19—197.62 MB。",
    caveat: "这是下载体积除以episode数的粗估，不是训练时的固定内存大小。时长、相机数量、分辨率、深度、音频、力觉和压缩方式都会让不同子集相差数百倍。",
    missingDownloads: "未注册的3项：QUT Dynamic Grasping（812 episodes）、MPI Muscular Proprioception（256 episodes）、ALOHA（451 episodes）。",
    links: [
      { label: "查看72项审计CSV", url: "./downloads/open_x_72_subdatasets_audit.csv", download: true },
      { label: "下载可筛选工作簿", url: "./downloads/open_x_72_subdatasets_audit.xlsx", download: true },
      { label: "Open X官方表", url: "https://docs.google.com/spreadsheets/d/1rPBD77tk60AEIGZrGSODwyyzs5FgCU9Uz3h-3_t2A9g/edit#gid=0" },
    ],
  },
};

const tierPriority = { "核心": 0, "扩展": 1, "对照": 2, "上游": 3, "非full-body": 4 };
const taskGroupOrder = [
  "全身移动与操作",
  "移动、导航与平衡",
  "工具与接触操作",
  "双臂协作",
  "抓取与基础操作",
  "人体动作与运动跟踪",
  "长时程与多任务",
  "语言与人机交互",
  "仿真任务与数据生成",
  "其他 / 任务待细分",
];

const supplementFor = (item) => datasetSupplements[item.lineage_id] || null;
const openXItem = datasets.find((item) => item.lineage_id === "open-x-embodiment-aggregate" || item.name === "Open X-Embodiment");
if (openXItem) {
  Object.assign(openXItem, {
    category: "跨本体真实机器人聚合数据集",
    collection_system: "72个既有独立数据集汇聚",
    trajectories: "2419193",
    access_status: "69项可从Open X清单获取；3项需查原项目",
    limitations: "聚合条目不能按1个独立数据集统计；动作语义、控制频率、相机配置和许可仍按72个来源分别解释。full-body数据占比很低。",
  });
}

const $ = (selector) => document.querySelector(selector);
const text = (value, fallback = "未统一披露") => value && value.trim() ? value.trim() : fallback;
const unique = (values) => [...new Set(values.filter(Boolean))].sort((a, b) => a.localeCompare(b, "zh-CN"));
const escapeHtml = (value = "") => value.replace(/[&<>'"]/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" })[char]);

function sourceGroup(item) {
  const haystack = `${item.category} ${item.origin} ${item.full_body_tier}`;
  if (/商业|内部/.test(haystack)) return "商业 / 内部";
  if (item.full_body_tier === "上游" || /人类|MoCap|人体/.test(item.origin)) return "人类上游";
  if (/仿真|生成|合成/.test(item.origin)) return "仿真 / 生成";
  if (/真实机器人|humanoid/.test(item.origin)) return "真实机器人";
  return "混合 / 其他";
}

function taskGroup(item) {
  const value = `${item.tasks || ""} ${item.category || ""} ${item.learning_goal || ""}`.toLowerCase();
  if (/全身|whole.?body|loco-manipulation|双足|humanoid|平衡|跌倒|恢复/.test(value)) return "全身移动与操作";
  if (/导航|navigation|locomotion|行走|移动|巡检/.test(value)) return "移动、导航与平衡";
  if (/工具|装配|旋拧|接触|力觉|触觉|插拔/.test(value)) return "工具与接触操作";
  if (/双臂|bimanual|双手|协作/.test(value)) return "双臂协作";
  if (/抓取|放置|grasp|pick|place|操作|manipulation/.test(value)) return "抓取与基础操作";
  if (/人体|mocap|运动跟踪|动作先验|模仿/.test(value)) return "人体动作与运动跟踪";
  if (/长时程|long.?horizon|多任务|组合/.test(value)) return "长时程与多任务";
  if (/语言|language|交互|人机|社会/.test(value)) return "语言与人机交互";
  if (/仿真|生成|benchmark|任务库/.test(value)) return "仿真任务与数据生成";
  return "其他 / 任务待细分";
}

function verificationDisplay(value = "") {
  return value.replace(/论文已核验/g, "论文单源核验");
}

function isAvailable(item) {
  const status = item.access_status || "";
  return /(可下载|开放|可用|获取|申请|部分|公开子集|签署许可)/.test(status) && !/(未开放|未确认|待核验)/.test(status);
}

function compactScale(item) {
  const values = [];
  if (item.hours) values.push(`${item.hours} h`);
  if (item.trajectories) values.push(`${item.trajectories} 轨迹/片段`);
  if (item.tasks_count) values.push(`${item.tasks_count} 任务`);
  if (values.length) return values.join(" · ");
  if (item.resource_type === "采集系统") return `系统类资源：${systemRole(item)}；不等同于统一数据集`;
  if (item.resource_type === "数据生成器") return "生成能力见项目；不等于现成轨迹数量";
  if (item.resource_type === "Benchmark/任务库") return "任务/实例规模见项目说明";
  return "论文未披露可统一比较的规模";
}

function systemRole(item) {
  const textValue = `${item.name || ""} ${item.tasks || ""} ${item.origin || ""} ${item.full_body_tier || ""}`;
  if (/humanoid|全身|locomotion|平衡|双足/.test(textValue)) return "全身示范、运动先验或遥操作";
  if (/采集|teleop|遥操作|leader|VR|手柄|robot-free|人体/.test(textValue)) return "示范采集与动作映射";
  if (/仿真|生成|benchmark|任务库/.test(textValue)) return "仿真 rollout 或合成数据";
  return "真实机器人轨迹采集";
}

function populateMetrics() {
  const mainWindow = datasets.filter((item) => item.time_scope === "2022—2026主窗口");
  $("#metricTotal").textContent = mainWindow.length || datasets.length;
  $("#metricCore").textContent = mainWindow.filter((item) => item.full_body_tier === "核心").length;
  $("#metricUpstream").textContent = mainWindow.filter((item) => item.full_body_tier === "上游").length;
  $("#metricOpen").textContent = mainWindow.filter((item) => item.access_bucket === "可直接下载").length;
}

function renderRecentResources() {
  const container = $("#recentGrid");
  if (!container) return;
  container.innerHTML = recentResources.map((item) => `
    <article class="recent-card resource ${item.full_body_tier === "核心" ? "fullbody" : ""}">
      <div class="recent-meta"><span>${escapeHtml(String(item.year))}</span><b>${escapeHtml(item.resource_type)}</b><i>${escapeHtml(item.full_body_tier)}</i></div>
      <h3>${escapeHtml(item.name)}</h3>
      <p>${escapeHtml(item.tasks || "任务信息见正式资源目录")}</p>
      <div class="recent-access"><b>${escapeHtml(item.access_bucket)}</b><span>${escapeHtml(item.verification_state)}</span></div>
      <div class="recent-relation">${escapeHtml(item.access_status)}</div>
      <a href="${escapeHtml(item.project_url || item.primary_url)}" target="_blank" rel="noreferrer">${item.project_url ? "查看项目/数据入口" : "查看论文中的资源说明"} ↗</a>
    </article>
  `).join("");
}

function renderCollectionSystems() {
  $("#collectionGrid").innerHTML = collectionSystems.map((item, index) => `
    <button class="collection-card" type="button" data-collection="${index}" aria-label="查看 ${escapeHtml(item.name)} 的数据内容和使用说明">
      ${item.image ? `<span class="collection-visual"><img src="${escapeHtml(item.image)}" alt="${escapeHtml(item.imageAlt)}" loading="lazy" /><small>素材：${escapeHtml(item.imageCredit)}</small></span>` : '<span class="collection-visual collection-placeholder" aria-hidden="true"><b>策略</b><i>→</i><b>采集</b><i>→</i><b>回流</b></span>'}
      <span class="collection-card-meta"><span class="collection-index">C${String(index + 1).padStart(2, "0")} · ${escapeHtml(item.type)}</span><span class="collection-focus ${item.focus === "Full-body优先" ? "primary" : item.focus === "Full-body扩展" ? "extension" : ""}">${escapeHtml(item.focus)}</span></span>
      ${Number.isFinite(item.citation_count) ? `<span class="collection-impact">论文合计引用 ${item.citation_count.toLocaleString("zh-CN")} 次 · 核验至2026-09-02</span>` : ""}
      <h3>${escapeHtml(item.name)}</h3>
      <p>${escapeHtml(item.copy)}</p>
      <b>${escapeHtml(item.tradeoff)}</b>
      <span class="collection-cta">查看数据与用法 →</span>
    </button>
  `).join("");
  document.querySelectorAll(".collection-card").forEach((card) => card.addEventListener("click", () => openCollectionDetail(Number(card.dataset.collection))));
}

function openCollectionDetail(index) {
  const item = collectionSystems[index];
  if (!item) return;
  const links = item.links.map((link) => `<a href="${escapeHtml(link.url)}" target="_blank" rel="noreferrer">${escapeHtml(link.label)} ↗</a>`).join("");
  const visual = item.image ? `<figure class="collection-detail-visual"><img src="${escapeHtml(item.image)}" alt="${escapeHtml(item.imageAlt)}" /><figcaption>素材来源：${escapeHtml(item.imageCredit)}；原项目入口见下方链接。</figcaption></figure>` : "";
  $("#dialogContent").innerHTML = `<article class="detail collection-detail">
    <p class="eyebrow">采集系统 · ${escapeHtml(item.type)}</p>
    <h2 id="dialogTitle">${escapeHtml(item.name)}</h2>
    <p class="detail-lead">${escapeHtml(item.copy)} ${escapeHtml(item.tradeoff)}。</p>
    ${visual}
    ${item.citation_count !== undefined ? `<section class="detail-block impact-detail"><h3>影响力与使用情况</h3><p><b>论文合计引用 ${Number(item.citation_count).toLocaleString("zh-CN")} 次</b>。${escapeHtml(item.adoption || "真实用户人数没有统一公开统计，引用量和公开下游谱系仅作为可复核代理。")}</p><p class="detail-caveat">引用数不是用户人数，也不能直接代表数据质量；新系统会因发布时间短而被低估。</p></section>` : ""}
    ${item.datasets ? `<section class="detail-block"><h3>已经产出或带动的数据</h3><p>${escapeHtml(item.datasets)}</p></section>` : ""}
    <section class="detail-block"><h3>数据里通常有什么</h3><p>${escapeHtml(item.contains)}</p></section>
    <section class="detail-block"><h3>如何开始使用</h3><p>${escapeHtml(item.use)}</p></section>
    <div class="detail-links">${links}</div>
  </article>`;
  $("#detailDialog").showModal();
}

function populateFilters() {
  const type = $("#typeFilter");
  unique(datasets.map((item) => item.resource_type)).forEach((value) => type.insertAdjacentHTML("beforeend", `<option value="${escapeHtml(value)}">${escapeHtml(value)}</option>`));
  const tier = $("#tierFilter");
  unique(datasets.map((item) => item.full_body_tier)).forEach((value) => tier.insertAdjacentHTML("beforeend", `<option value="${escapeHtml(value)}">${escapeHtml(value)}</option>`));
  const origin = $("#originFilter");
  unique(datasets.map(sourceGroup)).forEach((value) => origin.insertAdjacentHTML("beforeend", `<option value="${escapeHtml(value)}">${escapeHtml(value)}</option>`));
  const access = $("#accessFilter");
  unique(datasets.map((item) => item.access_bucket)).forEach((value) => access.insertAdjacentHTML("beforeend", `<option value="${escapeHtml(value)}">${escapeHtml(value)}</option>`));
  const task = $("#taskFilter");
  unique(datasets.map(taskGroup)).forEach((value) => task.insertAdjacentHTML("beforeend", `<option value="${escapeHtml(value)}">${escapeHtml(value)}</option>`));
}

function cardTemplate(item) {
  const task = text(item.tasks, "任务信息待核验");
  const modalities = text(item.modalities, "模态信息待核验");
  const verificationState = item.verification_state || (item.evidence_level === "A" ? "来源与开放状态已核验" : "来源字段待补");
  const evidenceLabel = verificationState === "论文已核验·未见独立入口" ? "论文单源核验" : verificationState.includes("开放待确认") ? "来源已核验" : verificationState.includes("已核验") ? "已交叉核验" : "来源待补";
  const evidenceTitle = item.verification_note || verificationDisplay(verificationState);
  return `
    <button class="dataset-card" type="button" data-id="${escapeHtml(item.id)}" aria-label="查看 ${escapeHtml(item.name)} 详情">
      <span class="card-top"><span class="dataset-id">${escapeHtml(item.id)} · ${escapeHtml(item.year)}</span><span class="evidence ${item.evidence_level === "B" ? "b" : "evidence-a"}" title="${escapeHtml(evidenceTitle)}">${escapeHtml(evidenceLabel)}</span></span>
      <h3>${escapeHtml(item.name)}</h3>
      <p class="dataset-subtitle">${escapeHtml(item.embodiment || item.robot_platform || item.category)}</p>
      <div class="badges">${supplementFor(item) ? '<span class="badge aggregate">聚合条目</span>' : ""}<span class="badge">${escapeHtml(item.full_body_tier)}</span><span class="badge task-badge">${escapeHtml(taskGroup(item))}</span><span class="badge">${escapeHtml(sourceGroup(item))}</span>${item.resource_type === "采集系统" ? `<span class="badge system-role">${escapeHtml(systemRole(item))}</span>` : ""}<span class="badge">${escapeHtml(item.access_bucket || item.access_status || "状态未核验")}</span>${item.influence_tier ? `<span class="badge influence">${escapeHtml(item.influence_tier)}</span>` : ""}</div>
      <dl class="dataset-facts">
        <div><dt>影响</dt><dd>${Number(item.citation_count || 0).toLocaleString("zh-CN")} 次论文引用${item.citation_count ? "" : "（新近或未形成引用）"}</dd></div>
        <div><dt>规模</dt><dd>${escapeHtml(compactScale(item))}</dd></div>
        <div><dt>任务</dt><dd>${escapeHtml(task)}</dd></div>
        <div><dt>模态</dt><dd>${escapeHtml(modalities)}</dd></div>
      </dl>
    </button>`;
}

function compareResourcePriority(a, b) {
  const accessPriority = { "可直接下载": 0, "需申请/注册": 1, "部分开放/分散获取": 2, "仅代码/论文": 3, "未发现公开入口": 4, "未公开/内部": 5, "开放状态待核验": 6 };
  return (tierPriority[a.full_body_tier] ?? 99) - (tierPriority[b.full_body_tier] ?? 99)
    || (accessPriority[a.access_bucket] ?? 9) - (accessPriority[b.access_bucket] ?? 9)
    || Number(b.impact_score || 0) - Number(a.impact_score || 0)
    || Number(b.citation_count || 0) - Number(a.citation_count || 0)
    || a.name.localeCompare(b.name, "zh-CN");
}

function filteredDatasets(ignoreTask = false) {
  const query = $("#searchInput").value.trim().toLowerCase();
  const scope = $("#scopeFilter").value;
  const type = $("#typeFilter").value;
  const tier = $("#tierFilter").value;
  const origin = $("#originFilter").value;
  const access = $("#accessFilter").value;
  const task = $("#taskFilter").value;
  const evidence = $("#evidenceFilter").value;
  return datasets.filter((item) => {
    const corpus = Object.values(item).join(" ").toLowerCase();
    return (!query || corpus.includes(query))
      && (scope === "all" || item.time_scope === scope)
      && (type === "all" || item.resource_type === type)
      && (tier === "all" || item.full_body_tier === tier)
      && (origin === "all" || sourceGroup(item) === origin)
      && (access === "all" || item.access_bucket === access)
      && (ignoreTask || task === "all" || taskGroup(item) === task)
      && (evidence === "all" || item.evidence_level === evidence);
  }).sort(compareResourcePriority);
}

function taskGroupRank(value) {
  const rank = taskGroupOrder.indexOf(value);
  return rank === -1 ? taskGroupOrder.length : rank;
}

function groupedCatalogMarkup(result, idPrefix = "catalog") {
  const groups = new Map();
  result.forEach((item) => {
    const group = taskGroup(item);
    if (!groups.has(group)) groups.set(group, []);
    groups.get(group).push(item);
  });
  return [...groups.entries()]
    .sort(([a], [b]) => taskGroupRank(a) - taskGroupRank(b))
    .map(([group, items]) => `
      <section class="task-group-section" aria-labelledby="${idPrefix}-${taskGroupRank(group)}-title">
        <div class="task-group-header">
          <div><span class="task-group-kicker">TASK GROUP ${String(taskGroupRank(group) + 1).padStart(2, "0")}</span><h3 id="${idPrefix}-${taskGroupRank(group)}-title">${escapeHtml(group)}</h3></div>
          <span class="task-group-count">${items.length} 项</span>
        </div>
        <div class="catalog-grid task-group-grid">${items.map(cardTemplate).join("")}</div>
      </section>
    `).join("");
}

function renderTaskNavigation(result) {
  const container = $("#taskNavigation");
  if (!container) return;
  const selectedTask = $("#taskFilter")?.value || "all";
  const counts = new Map();
  result.forEach((item) => counts.set(taskGroup(item), (counts.get(taskGroup(item)) || 0) + 1));
  container.innerHTML = ["全部任务", ...taskGroupOrder]
    .filter((label) => label === "全部任务" || counts.has(label))
    .map((label) => {
      const value = label === "全部任务" ? "all" : label;
      const count = label === "全部任务" ? result.length : counts.get(label);
      return `<button type="button" class="task-nav-chip${value === selectedTask ? " active" : ""}" data-task="${escapeHtml(value)}"><span>${escapeHtml(label)}</span><b>${count}</b></button>`;
    }).join("");
  container.querySelectorAll(".task-nav-chip").forEach((button) => button.addEventListener("click", () => {
    $("#taskFilter").value = button.dataset.task;
    renderCatalog();
  }));
}

function renderCatalog() {
  const result = filteredDatasets();
  $("#catalogGrid").innerHTML = groupedCatalogMarkup(result);
  $("#resultCount").textContent = `${result.length} 条结果`;
  $("#emptyState").hidden = result.length !== 0;
  document.querySelectorAll("#catalogGrid .dataset-card").forEach((card) => card.addEventListener("click", () => openDetail(card.dataset.id)));
  renderTaskNavigation(filteredDatasets(true));
}

function renderFullbodyCatalog() {
  const result = datasets
    .filter((item) => item.time_scope === "2022—2026主窗口" && ["核心", "扩展", "对照"].includes(item.full_body_tier))
    .sort(compareResourcePriority);
  $("#fullbodyCatalogGrid").innerHTML = groupedCatalogMarkup(result, "fullbody");
  document.querySelectorAll("#fullbodyCatalogGrid .dataset-card").forEach((card) => card.addEventListener("click", () => openDetail(card.dataset.id)));
}

function detailCell(label, value) {
  return `<div><dt>${escapeHtml(label)}</dt><dd>${escapeHtml(text(value))}</dd></div>`;
}

function openDetail(id) {
  const item = datasets.find((entry) => entry.id === id);
  if (!item) return;
  const supplement = supplementFor(item);
  const links = [
    item.primary_url ? `<a href="${escapeHtml(item.primary_url)}" target="_blank" rel="noreferrer">主要来源 ↗</a>` : "",
    item.project_url && item.project_url !== item.primary_url ? `<a href="${escapeHtml(item.project_url)}" target="_blank" rel="noreferrer">官方项目/数据入口 ↗</a>` : "",
    item.semantic_scholar_url ? `<a href="${escapeHtml(item.semantic_scholar_url)}" target="_blank" rel="noreferrer">引用记录 ↗</a>` : "",
    item.secondary_url ? `<a href="${escapeHtml(item.secondary_url)}" target="_blank" rel="noreferrer">补充来源 ↗</a>` : "",
    ...(supplement?.links || []).map((link) => `<a href="${escapeHtml(link.url)}" ${link.download ? "download" : 'target="_blank" rel="noreferrer"'}>${escapeHtml(link.label)}${link.download ? " ↓" : " ↗"}</a>`),
  ].filter(Boolean).join("");
  const supplementCells = supplement ? `
      ${detailCell("条目类型", supplement.resourceType)}
      ${detailCell("子数据集", supplement.subdatasetCount)}
      ${detailCell("时间窗覆盖", supplement.scopeCount)}
      ${detailCell("Open X可获取性", supplement.registeredCount)}
  ` : "";
  const supplementBlock = supplement ? `
    <section class="detail-block aggregate-detail">
      <h3>72个子数据集包含什么</h3><p>${escapeHtml(supplement.contentSummary)}</p>
      <h3>一个episode大约多大</h3><p>${escapeHtml(supplement.episodeSizeSummary)} ${escapeHtml(supplement.caveat)}</p>
      <h3>3项不在Open X下载清单</h3><p>${escapeHtml(supplement.missingDownloads)}</p>
    </section>
  ` : "";
  $("#dialogContent").innerHTML = `<article class="detail">
    <p class="eyebrow">${escapeHtml(item.id)} · ${escapeHtml(item.year)} · ${escapeHtml(verificationDisplay(item.verification_state || "核验状态待补"))}</p>
    <h2 id="dialogTitle">${escapeHtml(item.name)}</h2>
    <p class="detail-lead">${escapeHtml(item.category)}。${escapeHtml(item.learning_goal || "学习目标未统一披露")}。</p>
    <dl class="detail-grid">
      ${detailCell("Full-body层级", item.full_body_tier)}
      ${detailCell("来源", item.origin)}
      ${detailCell("本体", item.embodiment)}
      ${detailCell("机器人平台", item.robot_platform)}
      ${detailCell("任务", item.tasks)}
      ${detailCell("模态", item.modalities)}
      ${detailCell("规模", compactScale(item))}
      ${detailCell("对象 / 场景", [item.objects_count && `${item.objects_count} 对象`, item.scenes_count && `${item.scenes_count} 场景`].filter(Boolean).join(" · "))}
      ${detailCell("采集系统", item.collection_system)}
      ${detailCell("遥操作", item.teleoperation)}
      ${detailCell("同步 / 标定", item.synchronization)}
      ${detailCell("控制频率", item.control_frequency)}
      ${detailCell("存储格式", item.storage_format)}
      ${detailCell("Episode结构", item.episode_structure)}
      ${detailCell("动作表示", item.action_representation)}
      ${detailCell("开放状态", item.access_status)}
      ${detailCell("影响力层级", item.influence_tier)}
      ${detailCell("论文引用", `${Number(item.citation_count || 0).toLocaleString("zh-CN")} 次（Semantic Scholar，核验至2026-09-02）`)}
      ${detailCell("核验状态", verificationDisplay(item.verification_state))}
      ${detailCell("核验说明", item.verification_note)}
      ${detailCell("许可", item.license)}
      ${detailCell("核验日期", item.last_verified)}
      ${supplementCells}
    </dl>
    ${supplementBlock}
    <h3>已知限制</h3><p>${escapeHtml(text(item.limitations))}</p>
    <div class="detail-links">${links}</div>
  </article>`;
  $("#detailDialog").showModal();
}

function bindEvents() {
  ["#searchInput", "#scopeFilter", "#typeFilter", "#tierFilter", "#originFilter", "#accessFilter", "#taskFilter", "#evidenceFilter"].forEach((selector) => {
    $(selector).addEventListener(selector === "#searchInput" ? "input" : "change", renderCatalog);
  });
  $("#resetFilters").addEventListener("click", () => {
    $("#searchInput").value = "";
    $("#scopeFilter").value = "2022—2026主窗口";
    $("#typeFilter").value = "all";
    $("#tierFilter").value = "all";
    $("#originFilter").value = "all";
    $("#accessFilter").value = "all";
    $("#taskFilter").value = "all";
    $("#evidenceFilter").value = "all";
    renderCatalog();
  });
  $("#showAllCollectionSystems").addEventListener("click", () => {
    $("#searchInput").value = "";
    $("#scopeFilter").value = "2022—2026主窗口";
    $("#typeFilter").value = "采集系统";
    $("#tierFilter").value = "all";
    $("#originFilter").value = "all";
    $("#accessFilter").value = "all";
    $("#taskFilter").value = "all";
    $("#evidenceFilter").value = "all";
    renderCatalog();
  });
  $("#dialogClose").addEventListener("click", () => $("#detailDialog").close());
  $("#detailDialog").addEventListener("click", (event) => {
    if (event.target === $("#detailDialog")) $("#detailDialog").close();
  });
}

populateMetrics();
renderRecentResources();
renderCollectionSystems();
populateFilters();
bindEvents();
renderFullbodyCatalog();
renderCatalog();
