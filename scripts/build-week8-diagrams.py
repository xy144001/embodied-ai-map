"""Week8 implementation diagrams, based on the supplied 2026-10-20 report.
G0.5 sources: arXiv 2608.11739v1 and GalaxeaVLA commit 89f2322.
"""
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "public/model-architecture/week8"
COLORS = {"base": ("#15283f", "#799bcb"), "code": ("#2a2444", "#b7a3ff"),
          "new": ("#14362f", "#8ad2b7"), "note": ("#32291c", "#ddbc7c")}


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
        color, marker = ("#e0bc7e", "optional") if dashed else ("#9abce9", "arrow")
        self.edges.append(f'<path d="{path}" fill="none" stroke="{color}" stroke-width="2.3"{dash} marker-end="url(#{marker})"/>')

    def note(self, x, y, text, size=17, color="#b4c8e1"):
        self.notes.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}">{escape(text)}</text>')

    def save(self):
        defs = '<defs>' + ''.join(f'<marker id="{name}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="{color}"/></marker>' for name, color in [("arrow", "#9abce9"), ("optional", "#e0bc7e")]) + '</defs>'
        svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1120 {self.height}" role="img" aria-labelledby="title desc">',
               f'<title id="title">{escape(self.title)}</title><desc id="desc">{escape(self.subtitle)}</desc>', defs,
               f'<rect width="1120" height="{self.height}" rx="12" fill="#0b1422"/>',
               '<g font-family="system-ui, Noto Sans SC, Microsoft YaHei, sans-serif">',
               f'<text x="36" y="46" font-size="29" font-weight="700" fill="#f0f4ff">{escape(self.title)}</text>',
               f'<text x="36" y="82" font-size="17" fill="#b5c7df">{escape(self.subtitle)}</text>',
               *self.edges, *self.nodes, *self.notes, '</g></svg>']
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / f"{self.name}.svg").write_text("\n".join(svg) + "\n")


f = Figure("comparison", "新旧整体架构：更换码条件支路，保留 Faster-WAM", "两列为两套不同模型，不是同一次推理同时启用。当前新版基于冻结的历史 Full-only Parent。", 1100)
f.box(40, 120, 1040, 90, "共同输入 x：当前多视角图像 · 指令 · 14 维本体状态", ["Prior 只读当前信息；正式部署没有专家未来动作。"])
f.note(40, 252, "旧版 / 上下文条件 RVQ", 21, "#c5b6f5")
f.note(590, 252, "新版 / 结构化动作 codec", 21, "#a8dfc9")
f.box(40, 280, 490, 110, "旧 Prior：2 层 / 128 维 / 4 头", ["8 位置 × 2 级 → 16 个 ID", "每个 ID 取值 0…63"], "code")
f.box(590, 280, 490, 110, "新 Prior：同规模骨架，重新训练", ["64 个 arm ID（0…4095）", "再预测 128 个夹爪高 / 低字节"], "new")
f.box(40, 445, 490, 105, "旧查表：2 级向量相加", ["16 个 ID → 8 × 128 向量", "旧 codec 的 decoder 不参与正常动作输出"], "code")
f.box(590, 445, 490, 105, "新查表：4 级反投影求和＋夹爪投影", ["16 个 arm token + 32 个夹爪 token", "Z_new：48 × 128"], "new")
f.box(40, 620, 1040, 105, "共同主干计算：原生 Video K/V 缓存 + Action 前 9 个 block", ["当前图像与带噪动作走原路径 → 动作 hidden H：32 × 1024", "码不写入 Video DiT 或视频缓存；H 是两种 Conditioner 的 query。"])
f.box(40, 790, 490, 100, "旧 Conditioner：H 读取 8 个码 token", ["cross-attention 产生 δ", "原版已有 attention；不是这次才加入"], "code")
f.box(590, 790, 490, 100, "新 Conditioner：H 读取 48 个 token", ["扩展位置 / 模态编码与夹爪投影", "仍以 cross-attention 产生 δ"], "new")
f.box(40, 955, 1040, 90, "合流位置不变：blocks[8] 后 H′ = H + δ", ["其余 Action 层 → 10 次去噪 → 32 × 14 连续动作 → 最多执行 28 步，再观察、再选码。"])
for x in [285,835]:
    f.arrow([(x,210),(x,280)])
    f.arrow([(x,390),(x,445)])
    f.arrow([(x,725),(x,790)])
    f.arrow([(x,890),(x,955)])
f.arrow([(560,210),(560,620)])
f.arrow([(40,497),(20,497),(20,840),(40,840)])
f.arrow([(1080,497),(1100,497),(1100,840),(1080,840)])
f.note(40,1081,"同一动作块的 10 次去噪共享码；下一块重新预测。跨 episode 检索、写入与在线码字更新仍关闭。",17)
f.save()

f = Figure("codec", "新版动作表示：两臂共享 codec，夹爪独立保真", "图示学习 / 重建路径。正常预测码部署时，相同格式的 ID 来自新 Prior，而不是专家动作。", 1160)
f.box(40,125,1040,85,"32 步 × 14 维动作",["左右臂各 6 个关节命令 + 各 1 个连续夹爪命令；先拆开处理。"])
f.box(40,265,650,100,"双臂：每臂 32 × 6，共享同一套编码权重",["两臂放入 batch 维：B → 2B；关节维从 6 补到 9。"],"new")
f.box(750,265,330,100,"夹爪：32 × 2 个开度",["还原到官方 0…1 范围", "保留连续开度，不做二值化"],"code")
f.box(40,425,650,115,"短段 DCT + Conv / Transformer",["8 步 DCT 保留全部系数；通道 128 → 256 → 256", "3 个阶段各 2 个 self-attention block → 每臂 8 × 128 latent"],"new")
f.box(750,425,330,115,"独立 16-bit 量化",["ID = round(opening × 65535)","每步每只夹爪一个整数"],"code")
f.box(40,600,650,125,"4 级 EMA-RVQ：在低维空间量化残差",["每级：128 → 8 维 → 查 4096 项码表 → 128 维", "4 级反投影结果相加；左右臂共 64 个 ID", "训练时 EMA 更新码表；推理时固定"],"new")
f.box(750,600,330,125,"夹爪码：32 × 2 个 ID",["重建时 ID / 65535", "部署时 ID 由 Prior 预测", "不是原始浮点动作旁路"],"code")
f.box(40,835,500,120,"用途 A：检查动作能否还原",["arm decoder + 逆 DCT + 夹爪合并", "得到 32 × 14 动作，供重建 / roundtrip 执行"],"note")
f.box(580,835,500,120,"用途 B：给 WAM 提供码条件",["16 个 arm 向量 + 32 个夹爪 token", "48 × 128 → Conditioner → Action hidden"],"base")
for x in [365,915]:
    f.arrow([(x,210),(x,265)])
    f.arrow([(x,365),(x,425)])
    f.arrow([(x,540),(x,600)])
f.edges.append('<path d="M 365,725 L 365,780 M 915,725 L 915,780 M 290,780 L 915,780" fill="none" stroke="#9abce9" stroke-width="2.3"/>')
for x in [365,830,915]:
    f.edges.append(f'<circle cx="{x}" cy="780" r="4" fill="#9abce9"/>')
f.arrow([(290,780),(290,835)])
f.arrow([(830,780),(830,835)])
f.box(40,1010,1040,90,"基础版 codec 不读取图像、语言或状态；Prior 仍然需要当前情境。",["显式离散载荷：arm 768 bit + 夹爪 1024 bit = 1792 bit；旧版为 96 bit，不能称等码率比较。"],"note")
f.note(40,1135,"8 个 latent 位置已混合时间与关节信息，不等于 8 个连续时间点；新 self-attention 发生在动作特征上。",17)
f.save()

f = Figure("g05", "星海图 G0.5：一个自回归 VLM 连续生成推理与动作码", "默认主线是 VLA 的动作码解码执行。可选 flow 头单列；我们借鉴其动作表示，没有移植整个模型。", 1100)
f.box(40,140,300,105,"多视角当前图像 + 视觉历史",["预训练：5 秒窗口取 6 帧", "短时观测，不是跨回合经验库"])
f.box(410,140,300,105,"指令 / 本体标识 / 状态",["与视觉输入组成当前条件", "状态使用连续 embedding"])
f.box(40,320,300,130,"视觉编码器",["分解的空间 / 时间 attention", "融合历史后丢弃历史 token", "保留有历史信息的当前表示"])
f.box(410,320,300,130,"Qwen3.5-2B VLM",["同一个自回归 decoder", "按 next-token 目标训练", "文本与动作共享生成过程"],"new")
f.box(780,320,300,130,"生成一条 token 序列",["可选 Subtask / BBox 等推理", "随后生成结构化动作 ID", "动作可以读取前面的推理"],"new")
f.box(780,525,300,115,"ActionCodec decoder",["按部件读取实际码内容", "还原连续控制命令"],"code")
f.box(410,525,300,115,"可选 flow-matching 头",["读取自回归主干 hidden", "论文另设的替代输出路径"],"note")
f.box(780,715,300,95,"机器人执行动作块",["获取新观测后重新规划"])
f.arrow([(190,245),(190,320)])
f.arrow([(560,245),(560,320)])
f.arrow([(340,385),(410,385)])
f.arrow([(710,385),(780,385)])
f.arrow([(930,450),(930,525)])
f.arrow([(930,640),(930,715)])
f.arrow([(560,450),(560,525)],True)
f.arrow([(560,640),(560,762),(780,762)],True)
f.note(40,712,"ActionCodec：先学习动作表示，再冻结为 VLM 的动作词表接口。",17)
f.note(40,747,"官方默认 AR 路径会调用 codec decoder，码直接决定解码动作。",17)
f.note(40,840,"实线：默认自回归动作路径     虚线：可选 flow 路径（并非每次动作都串行经过它）",17,"#e4c88f")
f.box(40,900,1040,125,"我们的新接法：小型 Prior → 48 个码 token → Conditioner → Faster-WAM",["码向量先修改 Action hidden，最终动作由 Action DiT 去噪生成。", "没有使用 G0.5 的 VLM / 预训练权重、统一 CoT 生成或视觉历史模块。"],"code")
f.note(40,1068,"来源：G0.5 论文 v1 §3–4、官方仓库。图为结构关系重绘，未将该模型归类为视频预测 WAM。",16)
f.save()
