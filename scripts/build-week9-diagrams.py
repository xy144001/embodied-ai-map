"""Week9 diagrams redrawn from the supplied weekly review; no external assets."""
from html import escape
from pathlib import Path
OUT=Path(__file__).resolve().parents[1]/'public/model-architecture/week9'
COLORS={'base':('#15283f','#799bcb'),'train':('#14362f','#8ad2b7'),'future':('#32291c','#ddbc7c'),'local':('#2a2444','#b7a3ff')}
class Figure:
 def __init__(self,name,title,subtitle,height):self.name=name;self.height=height;self.title=title;self.subtitle=subtitle;self.edges=[];self.nodes=[];self.notes=[]
 def box(self,x,y,w,h,title,lines,kind='base'):
  fill,stroke=COLORS[kind];ty=y+(h-26*len(lines))/2+5
  self.nodes.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>')
  self.nodes.append(f'<text x="{x+w/2}" y="{ty}" text-anchor="middle" font-size="21" font-weight="700" fill="#f0f4ff">{escape(title)}</text>')
  for i,line in enumerate(lines):self.nodes.append(f'<text x="{x+w/2}" y="{ty+30+26*i}" text-anchor="middle" font-size="17" fill="#c5d3e7">{escape(line)}</text>')
 def arrow(self,points,dash=False):
  d='M '+' L '.join(f'{x},{y}' for x,y in points);attr=' stroke-dasharray="7 5"' if dash else '';color='#e0bc7e' if dash else '#9abce9';marker='optional' if dash else 'arrow'
  self.edges.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2.3"{attr} marker-end="url(#{marker})"/>')
 def note(self,x,y,s,size=17,color='#b4c8e1'):self.notes.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}">{escape(s)}</text>')
 def save(self):
  defs='<defs>'+''.join(f'<marker id="{n}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="{c}"/></marker>' for n,c in [('arrow','#9abce9'),('optional','#e0bc7e')])+'</defs>'
  s=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1120 {self.height}" role="img" aria-labelledby="title desc">',f'<title id="title">{escape(self.title)}</title><desc id="desc">{escape(self.subtitle)}</desc>',defs,f'<rect width="1120" height="{self.height}" rx="12" fill="#0b1422"/>','<g font-family="system-ui, Noto Sans SC, Microsoft YaHei, sans-serif">',f'<text x="36" y="46" font-size="29" font-weight="700" fill="#f0f4ff">{escape(self.title)}</text>',f'<text x="36" y="82" font-size="17" fill="#b5c7df">{escape(self.subtitle)}</text>',*self.edges,*self.nodes,*self.notes,'</g></svg>'];OUT.mkdir(parents=True,exist_ok=True);(OUT/(self.name+'.svg')).write_text('\n'.join(s)+'\n')
f=Figure('evolution','路线演变：从独立选码，到配套预训练的动作策略','三列是不同研究分支；右列为当前准备中的适配，不表示已经取得训练后的闭环结果。',1110)
for x,label in [(36,'旧：独立 Prior + WAM'),(397,'中间：通用 VLM 直接预测'),(758,'当前：官方 G0.5 Base')]:
 f.note(x,128,label,19,'#a8dfc9');f.box(x,160,326,100,'当前观察 / 状态 / 指令',['部署输入均不含专家未来动作'])
f.box(36,325,326,135,'独立小 Prior',['读取 WAM / VAE 当前特征','预测本地自训码本 ID'],'local')
f.box(397,325,326,135,'通用 Qwen3-VL-4B',['新增动作接口；LoRA 等训练','没有继承 Faster-WAM 动作权重'],'local')
f.box(758,325,326,135,'官方 G0.5 Base',['已有机器人动作预训练','计划全参数适配视觉与 VLM'],'train')
f.box(36,535,326,115,'查表 → Conditioner',['码向量注入 Action hidden','选码与内容利用需分别诊断'],'local')
f.box(397,535,326,115,'更换动作输出形式',['自回归码 / 并行码 / 连续头','绕开旧 WAM Conditioner'],'local')
f.box(758,535,326,115,'官方词表与序列化',['在 RoboTwin 监督动作码 CE','复用原配接口与码本'],'train')
f.box(36,725,326,115,'Faster-WAM 生成动作',['最终仍由 Action DiT 去噪','新码本往返好，预测链仍差'])
f.box(397,725,326,115,'直接执行预测动作',['码经自训 codec；或连续输出','能拟合，泛化与闭环仍差'])
f.box(758,725,326,115,'固定官方 ActionCodec',['解码 32 步动作，先执行 8 步','无 memory AR 基线待训练'])
for x in [199,560,921]:
 for a,b in [(260,325),(460,535),(650,725)]:f.arrow([(x,a),(x,b)])
f.box(36,935,1048,110,'下一阶段：先验证官方 Base 的 AR 基线，再比较跨 episode 经验',['未来 memory 优先改变动作生成条件 / 选码倾向；当前未启用跨回合记忆，也不在线更新码表。'],'future')
f.arrow([(921,840),(921,935)],True)
f.note(36,1080,'依据：10-27 周报。G0.5 与中间分支都使用现成 VLM；更重要的区别是机器人预训练与成套接口。',17);f.save()
f=Figure('training','当前 G0.5 适配：训练动作策略，固定 ActionCodec','图示为报告核对的计划；快照时正式训练 0 更新。绿色将更新，蓝色固定，虚线为训练梯度。',1090)
f.box(40,140,500,110,'当前三相机 + 状态 + 指令',['头部 / 左腕 / 右腕；obs_size = 1','当前不使用 CoT 或跨 episode memory'])
f.box(600,140,480,110,'专家未来 32 步动作',['只用于构造监督标签','不会成为部署输入'])
f.box(40,345,500,150,'G0.5 Base：视觉 + VLM',['内部 PatchMerger、Transformer、动作词表','原参数参与全参数策略微调','继承官方机器人预训练，当前计划更新'],'train')
f.box(600,345,480,150,'固定官方 ActionCodec encoder + RVQ',['torch.no_grad() 编码专家动作','码表不因标签生成而 EMA 更新','匹配官方布局、词表与归一化'])
f.box(40,565,500,90,'自回归动作码概率 / ID',['训练计算 CE；部署生成编号'],'train')
f.box(600,565,480,90,'固定离散动作标签',['与策略的动作码概率计算 CE'])
f.box(390,725,340,100,'动作码 CE 损失',['梯度只回到策略参数'],'train')
f.box(600,890,480,100,'部署：固定 codec decoder → 动作',['32 步中先执行 8 步，再观察和生成'])
for x in [290,840]:
 f.arrow([(x,250),(x,345)]);f.arrow([(x,495),(x,565)])
f.arrow([(290,655),(290,775),(390,775)])
f.arrow([(840,655),(840,775),(730,775)])
f.arrow([(560,725),(560,420),(540,420)],True)
f.arrow([(290,775),(290,940),(600,940)])
f.note(40,1040,'训练：专家动作 → 固定编码标签 → CE。部署：当前观察 → VLM 预测 ID → 固定解码器 → 连续动作。',17);f.save()
