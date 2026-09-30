"""Exact, repo-native SVG diagrams for the supplied 2026-09-30 Memory-WAM notes.
Run explicitly when editing these figures; no runtime/network dependency.
"""
from pathlib import Path
from html import escape as e
OUT=Path(__file__).resolve().parents[1]/'public/model-architecture/week5'
OUT.mkdir(parents=True,exist_ok=True)
C={'frozen':('#14253a','#577ba8'),'train':('#12342f','#67bda4'),'branch':('#292442','#a398df'),'data':('#33291c','#b69559'),'plain':('#152437','#647a97')}
class Diagram:
 def __init__(self,key,title,subtitle,height):self.key=key;self.title=title;self.subtitle=subtitle;self.height=height;self.nodes={};self.lines=[];self.notes=[]
 def n(self,key,x,y,w,h,title,lines=(),kind='plain'):
  self.nodes[key]=(x,y,w,h,title,lines,kind);return self
 def edge(self,a,b,side='down',points=None,dash=False,label=None):
  ax,ay,aw,ah,*_=self.nodes[a];bx,by,bw,bh,*_=self.nodes[b]
  if points:pts=points
  elif side=='right':pts=[(ax+aw,ay+ah/2),(bx,by+bh/2)]
  elif side=='left':pts=[(ax,ay+ah/2),(bx+bw,by+bh/2)]
  else:
   sx,sy=ax+aw/2,ay+ah;ex,ey=bx+bw/2,by;my=(sy+ey)/2
   pts=[(sx,sy),(sx,my),(ex,my),(ex,ey)]
  d='M '+' L '.join(f'{x:g},{y:g}' for x,y in pts)
  self.lines.append(f'<path d="{d}" fill="none" stroke="#97b8ee" stroke-width="2" marker-end="url(#arrow)"'+(' stroke-dasharray="7 6"' if dash else '')+'/>')
  if label:self.notes.append((pts[len(pts)//2][0]+8,pts[len(pts)//2][1]-9,label,15))
  return self
 def note(self,x,y,text,size=17):self.notes.append((x,y,text,size));return self
 def save(self):
  a=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 {self.height}" role="img" aria-labelledby="title desc">',f'<title id="title">{e(self.title)}</title><desc id="desc">{e(self.subtitle)}</desc>', '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#97b8ee"/></marker></defs>',f'<rect width="1100" height="{self.height}" rx="12" fill="#091522"/>','<g font-family="system-ui, Noto Sans SC, Microsoft YaHei, sans-serif">',f'<text x="36" y="43" font-size="27" font-weight="700" fill="#f0f5ff">{e(self.title)}</text>',f'<text x="36" y="76" font-size="17" fill="#a9bdd9">{e(self.subtitle)}</text>']+self.lines
  for key,(x,y,w,h,title,lines,kind) in self.nodes.items():
   assert 0<=x<x+w<=1100 and 85<=y<y+h<self.height,(self.key,key)
   fill,stroke=C[kind];a.append(f'<g data-node="{key}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
   total=25+len(lines)*24;top=y+(h-total)/2+20
   a.append(f'<text x="{x+w/2:g}" y="{top:g}" text-anchor="middle" font-size="20" font-weight="650" fill="#edf4ff">{e(title)}</text>')
   for i,line in enumerate(lines):a.append(f'<text x="{x+w/2:g}" y="{top+26+i*24:g}" text-anchor="middle" font-size="17" fill="#bdd0e9">{e(line)}</text>')
   a.append('</g>')
  for x,y,t,size in self.notes:a.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="#a7bddb">{e(t)}</text>')
  a.append('</g></svg>');(OUT/f'{self.key}.svg').write_text('\n'.join(a)+'\n')
# Branching, not cumulative upgrades.
d=Diagram('evolution','架构演变：从哪里分支，就回答哪一个问题','箭头表示结构／实验来源，不表示全部权重或模块逐版累积。',1120)
d.n('v1',360,115,380,80,'动作侧 V1 / Mean',('旧 M7：逐候选修正，再等权平均',),'frozen')
d.n('video',40,250,300,100,'视频 Memory-WAM V2',('视频 adapter ＋动作 M7','独立保留；本周没有叠加'),'plain')
d.n('auto',400,250,660,100,'旧 Auto：先判断类别，再选择该类 bank / M6 / M7',('已知任务的混合运行；仍按类别隔离经历',),'frozen')
d.n('relation',400,410,660,100,'Relation：增强单条 memory 与当前场景的关系',('单任务 Relation → 每任务独立 M7 的 Relation-Auto','当前 state / language / observation → 关系 query'),'train')
d.n('paths',40,590,320,120,'改参数共享',('Private / Hybrid','Shared-Small / Shared','5 类、10 类分别联合训练'),'branch')
d.n('candidate',390,590,320,120,'改候选聚合',('冻结完整 Relation','只训练候选间 Q/K','单任务 · 新场景池与顺序'),'branch')
d.n('adapt',740,590,320,120,'改可训练范围',('M7-only / LoRA-only / Joint','Joint：动作局部 LoRA＋M7','单任务；仍用 Mean'),'branch')
d.n('fixed',740,780,320,90,'固定 Joint 6000 步',('父模型、M7、M6 全部冻结',),'frozen')
d.n('proxy',390,950,320,90,'Proxy-Gate',('只训新 gate：动作去噪 MSE',),'train')
d.n('outcome',740,950,320,90,'Outcome-Gate',('同结构新 gate：终局收益 BCE',),'train')
d.edge('v1','video').edge('v1','auto').edge('auto','relation').edge('relation','paths').edge('relation','candidate').edge('relation','adapt').edge('adapt','fixed').edge('fixed','proxy').edge('fixed','outcome')
d.note(40,1090,'候选 Attention、共享通路、Joint 是分支；最新 Gate 仅接在固定 Joint 外。').save()
# Relation, with two different attentions and per-action coefficient.
d=Diagram('relation','Relation：先理解当前场景，再读一条历史','离线训练：完整 M7 可训练；原 WAM 冻结。外层多个候选仍然 Mean。',1090)
d.n('state',40,110,300,78,'当前 state',('[1,38] · GT 几何辅助',),'data').n('lang',400,110,300,78,'有效文本 tokens',('[1,L,4096] · 冻结编码',),'frozen').n('obs',760,110,300,78,'当前首帧图像 tokens',('[1,16,3072] · 4×4 池化',),'frozen')
d.n('ctx',350,235,400,88,'多模态关系 context',('投影到 128 维；self-attention＋FFN','1 状态＋L 文本＋16 图像 tokens'),'train')
d.n('h',40,370,260,90,'动作 hidden h',('block28 后 [1,32,1024]','＋位置／去噪时刻'),'frozen')
d.n('q',350,370,400,90,'动作位置自己的 query q',('hidden 对 context 做 cross-attention','[1,32,128]'),'train')
d.n('m',790,495,270,90,'历史片段 mᵢ',('16×91 → memory encoder','仅已执行状态与动作'),'data')
d.n('read',350,495,400,90,'q 读取该片段的 tokens',('memory cross-attention → rᵢ','[1,32,128]'),'train')
d.n('f',40,635,470,68,'fᵢ = concat(q, rᵢ)',('256 维输出特征',),'train').n('z',590,635,470,68,'zᵢ = concat(q, rᵢ, q×rᵢ, |q−rᵢ|)',('512 维关系特征',),'train')
d.n('out',40,745,470,78,'residual 输出网络',('256 → 128 → 1024',),'train').n('g',590,745,470,78,'关系系数 gᵢ = sigmoid(·)',('[1,32,1] · 每动作位置一个数',),'train')
d.n('single',220,875,660,74,'形成完整单条增量 Δᵢ = FP32(hᵢ) − FP32(h)',('hᵢ = h ＋ cast(gᵢ × residual)；保留 dtype 舍入',),'branch')
d.n('mean',220,995,660,62,'候选完整 Δᵢ 等权平均，加回同一个 h',(),'branch')
d.edge('state','ctx').edge('lang','ctx').edge('obs','ctx').edge('ctx','q').edge('h','q','right').edge('q','read').edge('m','read','left').edge('read','f').edge('read','z').edge('f','out').edge('z','g').edge('out','single').edge('g','single').edge('single','mean').edge('h','single',points=[(40,415),(18,415),(18,912),(220,912)]).edge('h','mean',points=[(40,415),(18,415),(18,1026),(220,1026)]).save()
# Parameter sharing: no cross-class raw memory.
d=Diagram('paths','多任务通路：共享参数，经历仍按类别隔离','绿色为本轮联合训练的 M7；蓝色为冻结模块；紫色为本轮变化的输出通路。',1070)
d.n('class',40,120,320,88,'语言 → 冻结分类器',('预测类别 c；不读真实任务答案',),'frozen').n('bank',420,120,640,88,'只取类别 c 的成功历史 → hard → 原 M6',('K 个合格片段；共享专家不是 memory 条目',),'data')
d.n('enc',40,270,1020,100,'联合训练的共享关系编码器',('h / state / language / 当前首帧 / time → query ＋类别 c 的 embedding','逐候选读 memory → fᵢ = 256 维；zᵢ = 512 维'),'train')
d.n('private',40,440,320,110,'当前类别专属输出',('Private_c(fᵢ)','256 → r_private → 1024'),'branch').n('router',420,440,290,110,'共享专家 router',('zᵢ → 4 个分数','逐候选／动作位置选 Top-2'),'train').n('experts',760,440,300,110,'4 个共享输出专家',('只计算选中动作行','256 → r_shared → 1024'),'branch')
d.n('sum',40,625,1020,90,'专属输出 ＋ 被选共享输出的归一加权和',('乘原关系系数 gᵢ → 完整 Δᵢ → 候选间仍均匀 Mean',),'branch')
d.n('configs',40,775,1020,195,'保持激活瓶颈宽度 32；总参数量与计算量并未完全匹配',('Private：32 ＋ 0          Hybrid：16 ＋ 2×8','Shared-Small：8 ＋ 2×12          Shared：0 ＋ 2×16','rank 是带 SiLU 的中间宽度，不是固定线性矩阵的秩','Shared 仍保留每类 embedding、旧 M6 与同类 bank'),'plain')
d.edge('class','bank','right').edge('class','enc').edge('bank','enc').edge('enc','private').edge('enc','router').edge('enc','experts').edge('router','experts','right').edge('private','sum').edge('experts','sum').edge('sum','configs')
d.note(40,1027,'每方法、每合集只有一个共享 M7 实例；5 类与 10 类网络分别从零输出开始训练。').save()
# Candidate attention is not Relation or skill router.
d=Diagram('candidate','候选 Attention：给完整修正建议分配比例','离线训练：只更新两个无 bias 的 128→64 投影，共 16,384 参数。',935)
d.n('source',160,115,780,90,'冻结完整 Relation：K 个候选各走原 single_output',('同一个 h、context、时刻和噪声 → q、rᵢ、完整 Δᵢ',),'frozen')
d.n('q',40,280,300,80,'动作 query q',('[1,32,128]',),'frozen').n('r',400,280,300,80,'候选召回 rᵢ',('[K,1,32,128]',),'frozen').n('d',760,280,300,80,'完整最终 Δᵢ',('[K,1,32,1024]','含原关系系数 gᵢ'),'frozen')
d.n('wq',40,435,300,70,'训练 Wq：128 → 64',(),'train').n('wk',400,435,300,70,'训练 Wk：128 → 64',(),'train')
d.n('softmax',40,575,660,100,'scoreᵢ = Wq(q) · Wk(rᵢ) / √64',('沿候选维 softmax → wᵢ [K,1,32,1]','每动作位置、每去噪步分别加权'),'train')
d.n('sum',160,745,780,90,'Δ = Σ wᵢ Δᵢ；只加回一次 h',('继续冻结动作后缀；没有 Hybrid 专家，也不使用 utility 加权',),'branch')
d.edge('source','q').edge('source','r').edge('source','d').edge('q','wq').edge('r','wk').edge('wq','softmax').edge('wk','softmax').edge('softmax','sum').edge('d','sum',points=[(910,360),(910,710),(550,710),(550,745)])
d.note(40,880,'起点严格等价 Mean；候选重排不变 ≠ episode 历史顺序不敏感。').save()
# Adaptation: show correct cache boundary and changes to effective backbone.
d=Diagram('joint','Joint：让动作后两层配合 memory 学习','离线训练图。原 WAM 参数仍冻结；有效动作变换因新增 LoRA 而改变。',1130)
d.n('prefix',40,115,470,94,'冻结文本／视频与动作 blocks 0–27',('缓存边界移到 block27 后','hidden27：[1,32,1024]'),'frozen')
d.n('context',620,115,440,94,'冻结条件与候选准入',('语言／视频 K/V／当前首帧／状态','原 bank → hard → 冻结 M6'),'frozen')
d.n('b28',40,270,470,82,'动作 block28 ＋ rank8 LoRA',('原参数冻结；只训练新增 LoRA',),'train')
d.n('m7',620,395,440,106,'完整 Relation M7 继续训练',('h ＋ context ＋ K 个候选','完整 residual 仍 Mean-Utility','不叠加 Candidate-Attention'),'train')
d.n('h',40,415,470,82,'block28 输出 h',('[1,32,1024]',),'plain')
d.n('add',40,570,470,75,'h ＋ Δ_mean',(),'branch')
d.n('b29',40,710,470,82,'动作 block29 ＋ rank8 LoRA',('原后缀处理保持',),'train')
d.n('head',620,710,440,82,'输出 head ＋ rank8 LoRA',('预测 [1,32,14]',),'train')
d.n('loss',620,865,440,95,'成功轨迹动作去噪 MSE',('梯度回到 LoRA 与完整 M7','原采样器负责后续去噪／动作生成'),'data')
d.edge('prefix','b28').edge('b28','h').edge('context','m7').edge('h','m7','right').edge('h','add').edge('m7','add',points=[(840,501),(840,605),(510,605)]).edge('add','b29').edge('b29','head','right').edge('head','loss')
d.note(40,875,'LoRA：499,824 参数').note(40,910,'Relation M7：1,626,957 参数').note(40,1015,'M7-only：只续训 M7；LoRA-only：不使用 M7；Joint：两者一起训练。').note(40,1051,'Joint-off：关闭同一 Joint 的 memory；它与另训的 LoRA-only 不是同一套权重。').note(40,1087,'为突出可训练位置，省略原文本／视频条件到动作 blocks 的连线；这些原条件继续保留。').save()
# Gate inference.
d=Diagram('gate','最新 Gate：缩放已经聚合好的整块增量','离线训练仅更新新 DecisionGate；Joint 的 WAM、LoRA、M7、M6 全部冻结。',1090)
d.n('h',40,115,430,90,'固定 Joint → block28 后 h',('[1,32,1024]','含已训练后冻结的 LoRA'),'frozen')
d.n('rel',610,115,450,90,'冻结 Relation ＋原 M6 准入',('所有合格候选 → 原 Mean 输出 h_mean','仍使用原当前多模态 context'),'frozen')
d.n('delta',40,275,430,85,'实际增量 Δ = FP32(h_mean) − FP32(h)',('取原 Mean 已完成 dtype 转换的输出',),'frozen')
d.n('q',610,275,450,85,'query q 沿动作位置平均',('[1,32,128] → [1,128]',),'frozen')
d.n('stats',40,425,430,110,'4 个数值统计',('Δ RMS、h RMS','cos(Δ,h)、K/10','K/10 只是缩放，不是候选上限'),'plain')
d.n('features',610,425,450,110,'132 维 gate 输入 · detach',('128 维 query 摘要 ＋ 4 项统计','无终局标签、seed 或未来观测'),'frozen')
d.n('gate',610,605,450,105,'唯一训练模块：DecisionGate',('LayerNorm132 → Linear64 → SiLU','Linear1 → sigmoid；8,841 参数'),'train')
d.n('apply',40,790,1020,90,'h_out = cast(FP32(h) ＋ g × Δ)',('每次去噪调用一个 g；统一缩放 [1,32,1024] 的整块增量',),'branch')
d.n('tail',220,955,660,72,'冻结 Joint 后缀 → 原去噪更新与动作执行',('含已训练后冻结的 block29 / head LoRA',),'frozen')
d.edge('h','rel','right').edge('h','delta').edge('rel','delta').edge('rel','q').edge('delta','stats').edge('q','features').edge('stats','features','right').edge('features','gate').edge('gate','apply').edge('delta','apply',points=[(40,317),(20,317),(20,835),(40,835)]).edge('h','apply',points=[(255,115),(255,98),(1080,98),(1080,855),(1060,855)]).edge('apply','tail')
d.note(40,680,'初始 g=0.5；范围 0–1。').note(40,717,'只缩小，不翻向、不放大、不重选候选。').save()
# Gate training and offline labels: no leaking label online.
d=Diagram('supervision','相同新 gate，只改变监督来源','离线配对只来自开发集；终局结果是训练标签，绝不进入在线 gate 输入。',1140)
d.n('q',160,115,780,95,'257 个非空 memory 决策点：恢复相同初态与真实动作前缀',('核对物理状态和实际输入观测；固定同一个 Joint 父模型',),'data')
d.n('off',40,280,470,90,'Off：当前 chunk 关闭 memory',('后续所有 chunk 也关闭',),'frozen').n('on',590,280,470,90,'On：当前 chunk 开启原 Mean',('后续所有 chunk 也关闭',),'frozen')
d.n('diff',160,445,780,105,'514 条闭环 → 比较官方终局成败',('救回 28 → 标签 1；损伤 27 → 标签 0','202 个 tie 留档，但排除出两组训练'),'data')
d.n('data',160,625,780,100,'两组相同的 55 个有效 query：38 训练 / 17 验证',('相同固定 noise / timestep、132 维特征、结构与 g=0.5 初始化','仅新 gate 可训练；父 Joint 全部冻结'),'plain')
d.n('proxy',40,800,470,130,'Proxy-Gate：成功动作去噪 MSE',('g × 固定 Mean residual','经冻结后缀预测动作 target','允许梯度通过后缀传回 gate'),'train').n('outcome',590,800,470,130,'Outcome-Gate：终局收益 BCE',('同结构 gate 的 logit','标签：当前 chunk 开启能否救回','仅更新这一个 gate'),'train')
d.edge('q','off').edge('q','on').edge('off','diff').edge('on','diff').edge('diff','data').edge('data','proxy').edge('data','outcome')
d.note(40,1000,'已完成两组各 3000 步训练；正式评测仍进行中（报告截点 2026-09-30 11:08:39）。').note(40,1036,'比较的是局部单 chunk 干预标签与代理监督；尚不是持续注入的全局收益或整网强化学习。').save()
print('Generated 7 exact SVG diagrams.')
