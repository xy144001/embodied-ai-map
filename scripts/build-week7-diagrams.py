"""Rebuild diagrams of the implemented fixed-codebook WAM (2026-10-12 snapshot).

The online memory / local-code adaptation plans are deliberately excluded from
the active computation graph. Source: the two supplied Week7 HTML reports.
"""
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "public/model-architecture/week7"
COLORS = {"base": ("#15283f", "#799bcb"), "code": ("#2a2444", "#b7a3ff"),
          "train": ("#14362f", "#8ad2b7"), "teacher": ("#32291c", "#ddbc7c")}


class Figure:
    def __init__(self, name, title, subtitle, height):
        self.name, self.title, self.subtitle, self.height = name, title, subtitle, height
        self.edges, self.nodes, self.notes = [], [], []

    def box(self, x, y, width, height, title, lines, kind="base"):
        assert 0 <= x < x + width <= 1120 and 100 <= y < y + height < self.height
        fill, stroke = COLORS[kind]
        ty = y + (height - 26 * len(lines)) / 2 + 5
        self.nodes.append(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="9" fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>')
        self.nodes.append(f'<text x="{x+width/2}" y="{ty}" text-anchor="middle" font-size="21" font-weight="700" fill="#f0f4ff">{escape(title)}</text>')
        for i, line in enumerate(lines):
            self.nodes.append(f'<text x="{x+width/2}" y="{ty+30+i*26}" text-anchor="middle" font-size="17" fill="#c5d3e7">{escape(line)}</text>')

    def arrow(self, points, dashed=False):
        path = "M " + " L ".join(f"{x},{y}" for x, y in points)
        dash = ' stroke-dasharray="7 5"' if dashed else ""
        color, marker = ("#e0bc7e", "teacher") if dashed else ("#9abce9", "arrow")
        self.edges.append(f'<path d="{path}" fill="none" stroke="{color}" stroke-width="2.3"{dash} marker-end="url(#{marker})"/>')

    def wire(self, points):
        path = "M " + " L ".join(f"{x},{y}" for x, y in points)
        self.edges.append(f'<path d="{path}" fill="none" stroke="#9abce9" stroke-width="2.3"/>')

    def note(self, x, y, text, size=17, color="#b4c8e1"):
        self.notes.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}">{escape(text)}</text>')

    def save(self):
        defs = '<defs>' + ''.join(f'<marker id="{name}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="{color}"/></marker>' for name, color in [("arrow", "#9abce9"), ("teacher", "#e0bc7e")]) + '</defs>'
        svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1120 {self.height}" role="img" aria-labelledby="title desc">',
               f'<title id="title">{escape(self.title)}</title><desc id="desc">{escape(self.subtitle)}</desc>', defs,
               f'<rect width="1120" height="{self.height}" rx="12" fill="#0b1422"/>',
               '<g font-family="system-ui, Noto Sans SC, Microsoft YaHei, sans-serif">',
               f'<text x="36" y="46" font-size="29" font-weight="700" fill="#f0f4ff">{escape(self.title)}</text>',
               f'<text x="36" y="82" font-size="17" fill="#b5c7df">{escape(self.subtitle)}</text>',
               *self.edges, *self.nodes, *self.notes, '</g></svg>']
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / f"{self.name}.svg").write_text("\n".join(svg) + "\n")


f = Figure("inference", "当前推理：先选一组码，再让 WAM 生成连续动作", "已实现的固定码本链路。正式推理只使用当前信息，没有未来专家动作，也没有跨回合经验库。", 1000)
f.box(40, 120, 1040, 90, "当前情境 x", ["三视角当前图像 · 语言指令 · 14 维 qpos；每次动作队列耗尽后重新读取"])
f.box(40, 270, 440, 105, "CodePrior：按顺序采样 16 个 ID", ["2 层自回归 Transformer · 温度 T = 1", "每个动作块只采样一组完整码"], "train")
f.box(640, 270, 440, 105, "父 WAM：视频条件与缓存", ["one_pass_future_cache · 每块预填充一次", "原视频路径冻结；码不写入视频缓存"])
f.box(40, 435, 440, 110, "RVQ lookup：读取实际码向量", ["每个位置：E₀[k₀] + E₁[k₁]", "8 个位置 → 8 × 128 条件向量"], "code")
f.box(640, 435, 440, 110, "Action blocks 1–9", ["当前条件 + 带噪动作 + 去噪时刻", "得到 h：32 × 1024；主干权重冻结"])
f.box(40, 625, 1040, 110, "CodeConditioner：动作 hidden 作为 Q，8 个码向量作为 K/V", ["4-head cross-attention → 投影回 1024 → 残差相加", "注入 blocks[8] 之后，即第 9 个 Action block 后；没有额外 gate / alpha"], "train")
f.box(40, 800, 500, 100, "其余 Action blocks → 连续动作输出", ["10 次去噪共享同一组码，Q 随去噪变化", "最终预测 32 × 14 连续关节 / 夹爪命令"])
f.box(640, 800, 440, 100, "环境执行与重规划", ["执行前 28 步，随后获取新观测", "下一个 chunk 重新选码；码表本身不变"])
f.arrow([(260, 210), (260, 270)])
f.arrow([(860, 210), (860, 270)])
f.arrow([(260, 375), (260, 435)])
f.arrow([(860, 375), (860, 435)])
f.arrow([(260, 545), (260, 625)])
f.arrow([(860, 545), (860, 625)])
f.arrow([(290, 735), (290, 800)])
f.arrow([(540, 850), (640, 850)])
f.arrow([(1080, 850), (1100, 850), (1100, 165), (1080, 165)])
f.note(280, 591, "码 K/V", 18, "#c4b5f4")
f.note(880, 591, "动作 Q", 18)
f.note(40, 952, "Tokenizer 的动作重建 decoder 不参与正式输出；旧 M6 / M7 与在线码字更新均未接入。", 18)
f.save()

f = Figure("rvq", "一个动作块，为什么是 16 个 ID、8 个向量？", "RVQ = 残差向量量化：第一张表近似原向量，第二张表继续近似剩余误差。以下省略 batch 维。", 1010)
f.box(40, 120, 1040, 90, "专家动作 A*：32 步 × 14 维", ["绝对关节 / 夹爪命令 → 父模型归一化 → 每 4 步切成一个 patch"], "teacher")
for i in range(8):
    x = 40 + i * 131
    f.box(x, 265, 123, 72, f"patch {i+1}", [f"{i*4+1}–{i*4+4} 步"], "teacher")
f.box(40, 395, 300, 110, "当前情境 x", ["图像 · 指令 · qpos", "Tokenizer 自己的 ContextEncoder"])
f.box(410, 395, 670, 110, "逐 patch 编码：56 → 128", ["位置与有效步信息 + 对 context 的 cross-attention + FF", "得到 8 个 z；patch 间没有显式 self-attention"], "train")
f.box(40, 580, 220, 110, "取其中一个 zⱼ", ["128 维连续向量", "下述操作重复 8 次"], "train")
f.box(340, 580, 280, 110, "第一层 E₀：64 × 128", ["找离 zⱼ 最近的码 kⱼ,₀", "剩余 r = zⱼ − E₀[kⱼ,₀]"], "code")
f.box(710, 580, 370, 110, "第二层 E₁：64 × 128", ["找离残差 r 最近的码 kⱼ,₁", "补上第一层未表达的部分"], "code")
f.box(310, 780, 500, 110, "两个向量相加，得到一个 zqⱼ", ["zqⱼ = E₀[kⱼ,₀] + E₁[kⱼ,₁]", "保留 2 个 ID，输出 1 个 128 维向量"], "code")
f.wire([(560, 210), (560, 238)])
f.wire([(101.5, 238), (1018.5, 238)])
for i in range(8):
    center = 101.5 + i * 131
    f.arrow([(center, 238), (center, 265)])
    f.wire([(center, 337), (center, 365)])
f.wire([(101.5, 365), (1018.5, 365)])
f.arrow([(746, 365), (746, 395)])
f.arrow([(340, 450), (410, 450)])
f.arrow([(746, 505), (746, 545), (150, 545), (150, 580)])
f.arrow([(260, 635), (340, 635)])
f.arrow([(620, 635), (710, 635)])
f.arrow([(480, 690), (480, 780)])
f.arrow([(895, 690), (895, 740), (660, 740), (660, 780)])
f.note(644, 616, "残差", 17)
f.note(40, 946, "8 个 patch × 2 个 ID = 16 个 ID；查表相加后是 8 × 128 向量，不是 16 个向量。", 20, "#d8cbff")
f.note(40, 980, "码的含义依赖上下文和完整码组；不能把两张表的 128 个条目直接命名为 128 个完整技能。", 17)
f.save()

f = Figure("training", "三阶段分别训练，部署时才把它们串起来", "绿色：本阶段更新；蓝色：冻结或输入；橙色：离线专家信息。所有父 WAM 权重始终冻结。", 1060)
f.note(40, 131, "S1 / 学表示：怎样用有限的码保留动作信息？", 21, "#a8dfc9")
f.box(40, 160, 300, 115, "专家动作 A* + 当前 x", ["成功示范切成 32 步 chunk", "尾块带有效步 mask"], "teacher")
f.box(410, 160, 300, 115, "Tokenizer + 两层 RVQ", ["上下文编码 · 动作编码", "E₀ / E₁ 都学习"], "train")
f.box(780, 160, 300, 115, "重建 decoder", ["码向量 + 当前 x → 动作", "只用于离线训练 / 诊断"], "train")
f.arrow([(340, 217), (410, 217)])
f.arrow([(710, 217), (780, 217)])
f.note(40, 313, "目标：有效动作重建 + codebook loss + 0.25 × commitment；AdamW 更新，非 EMA。", 17)

f.note(40, 381, "S2 / 学选码：只看当前情境，预测专家会用的码。", 21, "#a8dfc9")
f.box(40, 410, 300, 115, "当前 x + 正确码前缀", ["Teacher forcing", "前面的 ID 由标签提供"], "teacher")
f.box(410, 410, 300, 115, "CodePrior", ["独立 ContextEncoder", "逐位置 64 类交叉熵"], "train")
f.box(780, 410, 300, 115, "冻结 Tokenizer → C*", ["A* + x 生成专家码标签", "不改变 S1 的编码方式"], "teacher")
f.arrow([(340, 467), (410, 467)])
f.arrow([(780, 467), (710, 467)], True)
f.note(40, 563, "目标：猜对下一个 ID；训练时的正确前缀，不等于部署时自己采样出的前缀。", 17)

f.note(40, 631, "S3 / 学注入：给定专家码，怎样帮助冻结的 WAM 去噪？", 21, "#a8dfc9")
f.box(40, 660, 300, 115, "冻结 Tokenizer → C*", ["仍然读取专家未来动作 A*", "不调用 CodePrior"], "teacher")
f.box(410, 660, 300, 115, "只训练 Conditioner", ["专家码 K/V + 动作 hidden Q", "第 9 个 Action block 后注入"], "train")
f.box(780, 660, 300, 115, "冻结 WAM + flow loss", ["保留原时间步权重", "梯度穿过冻结层回到接口"])
f.arrow([(340, 717), (410, 717)])
f.arrow([(710, 717), (780, 717)])
f.note(40, 813, "S3 的训练和开发选权都使用 teacher code；当前没有用预测码训练接口。", 17, "#e8c98f")

f.box(40, 870, 1040, 115, "部署的改变：当前 x → Prior 自由采样 Ĉ → 查固定表 → Conditioner / WAM", ["没有真实未来动作，也没有正确码前缀；每个 chunk 采样 16 个 ID，随后进行连续去噪。", "这处条件差异已经确认；是否是成功率下降的主因，还需要 Off / teacher / predicted 对照。"], "teacher")
f.note(40, 1027, "相同的 6,000 步不代表相同数据量：S1 / S2 batch 64；S3 batch 8，选用第 5,500 步。", 17)
f.save()
