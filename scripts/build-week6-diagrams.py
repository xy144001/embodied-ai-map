"""Reproducible SVG figures for the proposed codebook architecture (2026-10-08).
These are design diagrams, not records of an implemented model.
"""
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "public/model-architecture/week6"
COLORS = {
    "base": ("#15283f", "#799bcb"),
    "code": ("#2a2444", "#b7a3ff"),
    "train": ("#14362f", "#8ad2b7"),
    "plan": ("#32291c", "#ddbc7c"),
}


class Figure:
    def __init__(self, name, title, subtitle, height):
        self.name, self.height = name, height
        self.title, self.subtitle = title, subtitle
        self.edges, self.nodes, self.notes = [], [], []

    def box(self, x, y, width, height, title, lines, kind="base"):
        assert x >= 0 and x + width <= 1120 and y + height < self.height
        fill, stroke = COLORS[kind]
        text_y = y + (height - 26 * len(lines)) / 2 - 1
        parts = [f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="9" fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>',
                 f'<text x="{x+width/2}" y="{text_y}" text-anchor="middle" font-size="21" font-weight="700" fill="#f0f4ff">{escape(title)}</text>']
        for i, line in enumerate(lines):
            parts.append(f'<text x="{x+width/2}" y="{text_y+30+i*26}" text-anchor="middle" font-size="17" fill="#c0d0e7">{escape(line)}</text>')
        self.nodes.extend(parts)

    def arrow(self, points, dashed=False):
        color = "#dfbc7d" if dashed else "#95b9ed"
        marker = "update" if dashed else "arrow"
        dash = ' stroke-dasharray="8 6"' if dashed else ""
        path = "M " + " L ".join(f"{x},{y}" for x, y in points)
        self.edges.append(f'<path d="{path}" fill="none" stroke="{color}" stroke-width="2.4"{dash} marker-end="url(#{marker})"/>')

    def note(self, x, y, text, size=17, color="#acbfdc"):
        self.notes.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}">{escape(text)}</text>')

    def save(self):
        defs = '<defs>' + ''.join(f'<marker id="{name}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="{color}"/></marker>' for name, color in [("arrow", "#95b9ed"), ("update", "#dfbc7d")]) + '</defs>'
        svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1120 {self.height}" role="img" aria-labelledby="title desc">',
               f'<title id="title">{escape(self.title)}</title><desc id="desc">{escape(self.subtitle)}</desc>', defs,
               f'<rect width="1120" height="{self.height}" rx="12" fill="#0b1422"/>',
               '<g font-family="system-ui, Noto Sans SC, Microsoft YaHei, sans-serif">',
               f'<text x="36" y="47" font-size="29" font-weight="700" fill="#f0f4ff">{escape(self.title)}</text>',
               f'<text x="36" y="83" font-size="17" fill="#b3c5df">{escape(self.subtitle)}</text>',
               *self.edges, *self.nodes, *self.notes, '</g></svg>']
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / f"{self.name}.svg").write_text("\n".join(svg) + "\n")


f = Figure("architecture", "Memory-WAM 第二版：可更新行为码本", "候选 A：显式读取码内容，保留连续动作生成。全部新增模块与更新规则均待验证。", 1040)
f.box(40, 135, 300, 112, "当前可用信息", ["观测 O · 指令 L · 状态 s", "不读取真实未来动作 / 结果"])
f.box(410, 135, 300, 112, "WAM 当前条件", ["保留现有感知与条件路径", "不要求生成完整未来视频"])
f.box(780, 135, 300, 112, "动作生成的输入", ["带噪动作 Aτ · 去噪时刻 τ", "每块内保持码本版本一致"])
f.box(40, 335, 300, 102, "状态条件选择器 R", ["选码或短码序列", "部署仅使用当前信息"], "train")
f.box(40, 505, 300, 120, "行为码本 Cᵛ", ["有限、可复用的码向量", "表示类型与容量待比较"], "code")
f.box(410, 505, 300, 120, "码条件接口 U", ["读入实际码值", "生成条件 / 轻量调制"], "train")
f.box(780, 505, 300, 120, "连续 Action DiT", ["结合当前条件与码条件", "逐步生成连续动作块"])
f.box(780, 750, 300, 105, "环境执行", ["实际动作与状态变化", "结果发生之后才记录"])
f.box(410, 750, 300, 105, "已发生经历 + 反馈", ["成功 / 失败 / 可靠阶段信号", "不把失败当正确动作标签"], "plan")
f.box(40, 750, 300, 105, "拟议反馈更新器", ["改变码值或可更新增量", "优化目标与规则尚待设计"], "plan")
f.arrow([(340, 191), (410, 191)])
f.arrow([(560, 247), (560, 285), (190, 285), (190, 335)])
f.arrow([(710, 191), (741, 191), (741, 400), (855, 400), (855, 505)])
f.arrow([(930, 247), (930, 505)])
f.arrow([(190, 437), (190, 505)])
f.arrow([(340, 565), (410, 565)])
f.arrow([(710, 565), (780, 565)])
f.arrow([(930, 625), (930, 750)])
f.arrow([(780, 802), (710, 802)])
f.arrow([(410, 802), (340, 802)], True)
f.arrow([(190, 750), (190, 625)], True)
f.note(365, 548, "码值", 15)
f.note(728, 548, "条件", 15)
f.note(218, 690, "反馈到达后更新", 17, "#e0c38f")
f.note(218, 718, "下一边界切换版本", 17, "#e0c38f")
f.note(948, 692, "连续动作", 16)
f.box(40, 910, 1040, 70, "同权重 Off：真正绕过码条件接口，检验码本带来的净作用", ["改码本内容 ≠ 只改选码概率；去噪 latent 在变化 ≠ 码本参数在学习。"], "code")
f.note(40, 1013, "实线：生成与执行的信息流     虚线：拟议的反馈更新     紫色：码本     绿色：新增调用接口", 16)
f.save()

f = Figure("training", "码本怎么训练：先学表示，再学调用，最后检验更新", "三项能力分别验证；真实未来只用于离线目标。静态码本是第一阶段，不替代可更新记忆的目标。", 1110)
f.note(40, 131, "01 / 离线学表示：码能否保留行动所需的信息？", 21, "#bba9ff")
f.box(40, 165, 280, 105, "离线经验", ["动作片段 / 可观测变化", "具体表示待比较"])
f.box(420, 165, 280, 105, "编码 + VQ / RVQ", ["连续 latent → 有限码", "学习行为表示"], "code")
f.box(800, 165, 280, 105, "重建 / 预测接口", ["重建选定目标", "检验信息是否被保留"], "train")
f.arrow([(320, 217), (420, 217)])
f.arrow([(700, 217), (800, 217)])
f.note(40, 309, "标准 VQ：重建 + 码本项 + 承诺项，或采用 EMA 等更新；检查实际梯度路径。", 17)
f.note(40, 342, "重建误差下降只是表示指标，不能直接替代任务成功率。", 17)

f.note(40, 408, "02 / 学会调用：只看当前情境，能否选对并用好这些码？", 21, "#90d9be")
f.box(40, 445, 280, 110, "当前部署可用条件", ["视觉 / 语言 / 状态", "不能看真实后续动作"])
f.box(420, 445, 280, 110, "选择器 + 码条件接口", ["预测码，读取码值", "学习如何影响动作"], "train")
f.box(800, 445, 280, 110, "连续动作生成器", ["正确加权的动作目标", "检查闭环控制效果"])
f.box(420, 625, 280, 85, "离线构造的码标签", ["只作训练监督"], "code")
f.arrow([(320, 500), (420, 500)])
f.arrow([(700, 500), (800, 500)])
f.arrow([(560, 625), (560, 555)], True)
f.note(40, 753, "分别检查选码是否正确、生成器是否绕过码，以及同权重 Off 的净差异。", 17)

f.note(40, 819, "03 / 部署适应：有了反馈，改变码本能否让后续表现更好？", 21, "#e3c48d")
f.box(40, 855, 280, 110, "执行后的可用反馈", ["结果与已执行经历", "终局结果不直接给梯度"], "plan")
f.box(420, 855, 280, 110, "待设计的内容更新", ["明确更新哪个张量", "明确优化信号从哪里来"], "plan")
f.box(800, 855, 280, 110, "新码本的后续评测", ["固定 / 只改路由 / 改内容", "同时检查旧能力与成本"], "plan")
f.arrow([(320, 910), (420, 910)], True)
f.arrow([(700, 910), (800, 910)], True)
f.note(40, 1020, "候选：反馈重放、价值估计或有限扰动比较；算法尚未选定，交互与训练预算必须匹配。", 17)
f.note(40, 1064, "研究目标：表示有用 → 调用有用 → 更新有用。不能用前一项的成功替代后一项的证据。", 17)
f.save()
