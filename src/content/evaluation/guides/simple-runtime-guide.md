---
title: SIMPLE 运行时与扩展指南：机器人本体、WBC 与成功判定（源码级）
category: evaluation
kind: guidance
organization: Embodied AI Map
releaseDate: 2026-09-14
summary: 按 SIMPLE 仓库源码梳理运行时结构，并给出三类扩展的落地路径：接入自定义机器人本体、接入自己的 WBC、以及任务成功判定的实现与排查方式；中心原则是“换数据集不必改 Task，换策略不必改 Simulator，换 WBC 不必改成功判定”。
tags: [simple, g1, whole-body-humanoid, runtime, wbc, success-check]
draft: false
references:
  - title: SIMPLE 官方仓库
    url: https://github.com/physical-superintelligence-lab/SIMPLE
  - title: SIMPLE 项目页
    url: https://psi-lab.ai/SIMPLE/
---

## 1. 运行时总览

SIMPLE 的设计中心是 Gymnasium 环境协议：环境只负责把任务状态变成观测并执行动作；任务负责场景配置、随机化和成功逻辑；机器人负责把动作解释为关节控制；策略 / Agent 负责产生动作。MuJoCo 是控制和碰撞的主物理后端，Isaac Sim 提供同步的高保真渲染通道。

```text
CLI / Gymnasium ID
        │
        ▼
Env (BaseDualSim 子类) ◄──────────── eval / sonic_wbc
        │                              │
        ├── Task 子类                  └── Agent / Policy
        │       │                         (本地、HTTP、回放)
        │       ├── DRManager + Randomizer
        │       │       └── Layout (actors / scene / cameras / lights)
        │       └── Robot + Protocols ─── ControllerCfg / Controller
        │
        ├── MuJoCo Simulator（物理、接触、控制）
        └── IsaacSim Simulator（可选，同步状态并渲染）
Agent ── ActionCmd ──► Env ── observation / info / reward / terminated ──► Agent
WBC（torque 或 decoupled_wbc） ──► Robot.apply_action ──► mjData.ctrl / 外部 SONIC
```

核心入口：`src/simple/envs/__init__.py`、`src/simple/core/task.py`、`src/simple/envs/base_dual_env.py`、`src/simple/engines/mujoco.py`。

## 2. 分层结构

| 层 | 内容 |
|---|---|
| 入口与注册 | Gym ID 在 `envs/__init__.py` 注册（例如 `simple/G1WholebodyXMoveBendCarryBoxSonic-v0` → `SonicLocoManipEnv`），并注入任务 UID；任务模块在 `tasks/__init__.py` 导入时执行 `@TaskRegistry.register(...)` |
| 核心抽象 | `Task` 定义 `reset`、观测/动作空间、`compute_reward`、`check_success`；`Robot` 定义 DOF、资源路径、FK/IK 等最小接口；`ActionCmd` 是带字符串类型和参数字典的统一动作信封 |
| 场景与资产 | `Layout` 收集 RobotActor、ObjectActor、ArticulatedObjectActor、Primitive、相机和灯光；`AssetManager` 与 Objaverse/GraspNet/primitive 资产提供 USD、MJCF、碰撞网格 |
| 执行与评测 | `EvalRunner` / `run_sonic_wbc_eval` 负责加载数据、创建环境、循环推理与写视频/统计；`VideoRecorder` 和 `StandStabilizationWrapper` 是可组合的 Gym wrapper |

双引擎：`BaseDualSim.__init__` 接收任务 UID 或 Task 实例；`sim_mode` 含 isaac 时创建全局 `SimulationApp` 与 `IsaacSimSimulator`，始终构造 `MujocoSimulator`。`SonicLocoManipEnv` 在每个控制步内执行多个 MuJoCo 子步，再按配置同步 Isaac。

域随机化与可复现：`Task.reset` 优先读取 `options` 中的 `state_dict`，否则调用 `DRManager.reset(seed)`，随后依次执行 scene、container、target、distractors、articulated、spatial、lighting、camera、material randomizer 并写入 Layout；`DRManager.load_state_dict` 按 `dr_level` 选择恢复空间、光照、材质和干扰物状态——评测因此可以复现采集时的场景，只改变指定等级的随机因素。

一个控制步的执行序列：

| 阶段 | 源码行为 | 关键数据 |
|---|---|---|
| 获取观测 | `SonicLocoManipEnv._get_obs` 读取 MuJoCo 关节位置并合并渲染帧；`_get_info` 读取每个 object 的 `xpos+xquat`，附加 `robot.prepare_obs()` 的本体感知 | `joint_qpos`、`head_stereo_left/right`、`target`、`proprio` |
| 策略产生动作 | Agent 返回 `ActionCmd`；SONIC Agent 经 ZMQ/DDS 或 HTTP policy 产生动作 | `ActionCmd.type` + 参数字典 |
| 写入执行器 | `mujoco.apply_action` 委托给 `Task.robot`；`G1Sonic.apply_action` 按类型选择弹力带、WBC torque 或 decoupled WBC 分支 | `mjData.ctrl` 或外部控制器命令 |
| 推进与判定 | MuJoCo 推进后重新取 obs/info，调用 `task.compute_reward` 与 `task.check_success`，将 `terminated` 返回给 Gym | `reward`、`terminated`、`info` |

SONIC 评测的控制频率固定为 50 Hz、物理步长 5 ms，每个控制动作对应 4 个子步；`LockstepBarrier` 用 session/sequence 与 body、左手、右手三路 ack 保证外部控制器与模拟时钟一致。

## 3. 接入自定义机器人本体

“本体模型”在 SIMPLE 中不是一个单独的类：至少要同时提供 MuJoCo 动力学模型，使用 Isaac 时提供 USD，使用运动规划/FK/IK 时提供 CuRobo/URDF 配置，并让机器人满足 SIMPLE 的 protocol 与控制器接口。

### 3.1 最小接口与注册

新建 `src/simple/robots/<my_robot>.py`，继承 `Robot`，按需混入 `Controllable`、`HasKinematics`、`HeadCamMountable`、`WristCamMountable`、`Humanoid`、`CuRoboMixin`：

```python
@RobotRegistry.register("my_robot")
class MyRobot(CuRoboMixin, Controllable, Robot, HeadCamMountable):
    uid = "my_robot"
    dof = 12                       # 不含 floating base 的可驱动 DOF
    wholebody_dof = 12             # whole-body agent 时需与动作定义一致
    mjcf_path = "robots/my_robot/my_robot.xml"
    usd_path = "robots/my_robot/my_robot.usd"
    joint_names = [...]
    init_joint_states = {name: 0.0 for name in joint_names}
    controller_cfg = ...
    head_camera_orientation = [1, 0, 0, 0]

    @property
    def head_cam_link(self):
        return "head_camera_link"
```

`RobotRegistry` 通过 `RegistryMixin.make` 缓存实例，同一 UID 的配置是单例式复用：若每个环境需要独立状态，应自行清理可变字段或使用不同 UID。任务侧通过 `Task.robot_cfg = {"uid": "my_robot"}` 或 `robot_uid` 参数接入。已有 G1 的参考实现是 `G1Sonic`。

### 3.2 MuJoCo 模型与索引一致性

对于 floating base，MuJoCo 的 `qpos` 前 7 项是位置 + 四元数，`qvel` 前 6 项是线/角速度；`G1Sonic` 据此设置 `qpos_offset=7`、`qvel_offset=6`，再按 joint name 构造 body / left-hand / right-hand 索引。自定义模型必须保证：

- MJCF joint 名称与 `joint_names` 完全匹配，actuator 名称可由 `mjData.actuator(name)` 找到；
- 手部关节（如有）能按左右侧分组，否则 `prepare_obs` 与 torque 映射会错位；
- floating root、constrained root、固定根三种布局与 `setup_control` 一致；
- 碰撞 geom/body 名称包含任务逻辑可识别的语义（例如 `target`、`hand`、`table`）。

模型不是 G1 时应重写 `setup_control`，至少返回并保存 `joints`、`actuators` 并调用 `controller.set_initial_qpos(...)`，不要照抄 G1 的字符串规则。

### 3.3 控制器与 action space

控制器配置位于 `robots/controllers`：`PDJointPosControllerCfg` 以 `joint_names`/`init_qpos` 定义关节组，`WholeBodyEEFControllerCfg` 把左右腿、腰、双臂和双手组合为一个 Dict action space。自定义控制器需要继承 `Controller`，实现 `action_space`、`set_initial_qpos`、`reset` 和（若环境直接调用）`apply_action`；`Controllable.controller` 懒加载 `controller_cfg.clazz`，配置类的构造参数与动作空间维度必须正确。

### 3.4 FK/IK、规划与资源

需要运动规划时继承 `CuRoboMixin`：从 robot_cfg YAML 读取 URDF、`base_link`、`ee_link` 与资产路径，`fk` 调用 `kin_model.get_state`，`ik` 调用 `IKSolver.solve_single`。没有 GPU/CuRobo 时实现自己的 `fk/ik/get_link_pose`，否则依赖这些 protocol 的 baseline（OpenVLA、规划器等）会失败。资源路径经 `resolve_data_path`/`resolve_res_path` 解析，注意 docker 挂载后路径仍然有效；IsaacSim 的 USD 只做渲染/物理镜像，MuJoCo 的 MJCF 才是评测执行模型。

### 3.5 为自定义机器人创建任务与环境

复制最接近的任务（如 `G1TabletopGraspMP`），修改 `robot_cfg`、传感器、DR 配置与 success 逻辑，用 `@TaskRegistry.register("my_task")` 注册，再在 `envs/__init__.py` 注册 Gym ID。需要 gravity/floating-base SONIC 行为时参考 `SonicLocoManipEnv`，不要只把普通固定基座环境改名。

## 4. 接入自己的 WBC

SIMPLE 提供两个接入面：**环境内 WBC**（作为 `ActionCmd` 执行器）和**外部 WBC**（经 SONIC 的 DDS/ZMQ lockstep 接入）。前者适合自研控制器直接调用，后者适合已有实时 WBC / 硬件桥接程序。

### 4.1 环境内 WBC：动作到 torque

Agent 返回：

```python
ActionCmd("wbc_torque",
          low_cmd=unitree_low_cmd,
          use_sensor=False,
          left_hand_cmd=left_hand_cmd,
          right_hand_cmd=right_hand_cmd)
```

`G1Sonic.apply_action` 的 `wbc_torque` 分支按 `tau = tau_ff + kp*(q_des − q) + kd*(dq_des − dq)` 计算，再按 body/hand 索引写入 torque 数组、按 `MOTOR_EFFORT_LIMIT_LIST` 裁剪后写入 `mjData.ctrl`。自定义 WBC 可复用该协议，也可在自己的 Robot 子类里新增 action 分支。

### 4.2 Decoupled WBC：策略给目标关节，Robot 做低层 PD

仓库已有完整参考：`SonicDecoupledWbcAgent` 构造 `wbc_obs`（q/dq/ddq/tau_est、floating base、IMU、wrist pose），调用 decoupled policy 得到目标配置，返回：

```python
ActionCmd("decoupled_wbc",
          target_q=body_target_q,
          left_hand_q=left_hand_target_q,
          right_hand_q=right_hand_target_q)
```

`G1Sonic` 的 decoupled 分支用 `MOTOR_KP/MOTOR_KD` 做本体 PD，双手使用固定 7 维 `hand_kp/hand_kd`，再做 torque 限幅与 floating-base 前缀处理。若 WBC 输出的是 task-space pose，建议在 Agent 内完成 IK / whole-body optimization 再变成 `target_q`，不要把 IK 逻辑塞进 MuJoCo simulator，以保持 simulator 职责单一、便于回放和离线调试。

### 4.3 外部 SONIC WBC：DDS + ZMQ + lockstep

继承 `WholeBodyControlAgent` 或 `ReplayWbcAgent`，初始化 `UnitreeSdk2Bridge` / `LockstepUnitreeBridge`，读取外部控制器的 lowcmd/hand cmd 并发布 lowstate；`LockstepBarrier` 固定 5 ms physics、20 ms control、4 子步，在每个边界冻结 proprio、发送 token，等待 body/left/right 三路相同 session/step/action ack。SONIC 评测的策略动作契约是 **78 维（64 维 token + 左右手各 7 维）、chunk 30、执行 horizon 1–30**，这是 `SonicEvalAgent` 的硬校验；不使用该 token 的 WBC 应直接走自定义 Agent/ActionCmd。

### 4.4 自定义 WBC 的适配清单

| 组件 | 必须提供 | 验证方式 |
|---|---|---|
| 观测适配 | 从 `robot.prepare_obs()` 或环境 obs 生成 q/dq/base/IMU/接触状态 | 逐字段检查 shape、单位、四元数顺序（wxyz） |
| 目标/力矩适配 | 返回 `ActionCmd`，或为 Robot 增加新 action 分支 | 空动作、极限动作与 NaN 检查；确认 torque limit 生效 |
| 时序 | 明确 `physics_dt`、`control_dt` 与子步数 | SONIC 必须是 0.005 / 0.02 / 4；普通环境按 task metadata |
| 复位 | 清空 WBC 内部滤波器、积分器、目标队列 | 环境 reset 后第一帧不应使用上一 episode 的目标 |
| 安全与诊断 | 关节/力矩裁剪、fall/stability 检查、控制延迟日志 | 用 VideoRecorder、lockstep events 与 proprio 日志回放 |

## 5. SIMPLE 如何判断任务成功

### 5.1 统一调用链

所有主要环境的 `step` 都遵循同一模式：执行动作 → 推进模拟 → 生成 info → `task.compute_reward` → `task.check_success` → 返回 `terminated`。Gym 的 `terminated=True` **只表示 Task 的成功函数返回真**，不是模型推理成功、不是预算耗尽、也不是视频写入成功；SONIC 评测再把它映射为 `TerminationReason.TASK_SUCCESS` 写入 summary。

### 5.2 实例：G1 XMove Bend Carry Box（SONIC）

`G1WholebodyXMoveBendCarryBoxTaskSonic` 的判定由三个原子条件组成：`_target_contacts(mujoco_env, "hand")` 遍历 `mjData.contact` 检查双手与箱子接触；`_target_on_table_top` 要求箱子—桌面接触且接触点 z 与桌面高度差不超过 0.05 m（避免侧面/边缘接触误判为放置）；`_box_placed_on_table` 要求双手离开箱子、箱子接触桌面上表面、箱子 COM 高于桌面 top。`compute_reward` 每次条件成立累加 0.02，`check_success` 返回 `self.reward > self.success_criteria`（默认 0.9）——即**需要连续/累计约 46 个满足条件的 50 Hz 控制步才算成功**，是带保持时间的累计门槛，而不是“一帧满足即成功”。

### 5.3 其他任务的判定模式

| 模式 | 源码例子 | 判定含义 |
|---|---|---|
| 高度归一化 | `G1TabletopGraspMP` | `(target_z − init_z)/LIFT_HEIGHT` clip 到 0–1，reward ≥ 1 成功 |
| 容器/接触 + 姿态误差 | `G1TabletopPickNPlaceMP` | 目标与 container 接触且不再与手接触，再用机器人回到初始姿态的平均误差指数衰减，reward ≥ 0.9 |
| 关节阈值 | `OpenFaucetTeleop` | articulated joint 角度超过 0.7 rad 时每步累加 0.03，否则清零 |
| 物体位移 | `PushOfficeChairTeleop` | 椅子 x 位移超过 0.8 m 时累加 0.06，否则清零 |

新增任务时按“几何/接触原子条件 → reward 累积或归一化 → 阈值函数”显式拆解，并在 `info` 中输出调试量。任务代码可以访问 MuJoCo 真实状态，而策略只能看到环境暴露的 observation——成功判定不依赖相机图像。

### 5.4 评测终止原因与排查顺序

`run_sonic_wbc_eval` 区分四种终止：`task_success`、预算耗尽、模型错误、lockstep 超时；预算耗尽时会根据最近 5 秒的奖励/距离/高度变化计算 `progressing_at_timeout`，但**不把任务标记为成功**；`success_rate = successes / len(results)` 只统计真正的 `TASK_SUCCESS`。排查成功判定的顺序：先在 `compute_reward` 打印每个原子条件（仓库的 carry-box 任务已提供 `XBENDPICK_DEBUG=1` 的 `_log_state`），再确认 info 中的 target/table 名称与 MJCF body 名称一致，最后检查 `success_criteria` 是否被 CLI 或构造参数覆盖。

## 6. 从零扩展的落地顺序

1. 只接入 MJCF + RobotRegistry + 一个能返回 qpos 的 Controller，在 `sim_mode=mujoco` 下完成 reset/step；
2. 加入 `prepare_obs`、动作索引与 torque limit；用固定 ActionCmd 验证每个关节的方向和单位；
3. 加入任务 Layout / DR 与相机；确认 info 能拿到目标、桌面、关节/接触状态；
4. 接入 WBC：先走环境内 `wbc_torque` 或 `decoupled_wbc`，再考虑外部 DDS/ZMQ lockstep；
5. 实现并单元测试 `compute_reward`/`check_success` 的原子条件；用手工构造的 qpos/contact 状态验证成功与失败边界；
6. 最后注册 Gym ID、加入评测 CLI，用 VideoRecorder 和 summary.json 检查 terminated、预算、视频与实际物理行为一致。

本页与 [SIMPLE Benchmark 条目](../../benchmarks/simple/)（任务协议与数据）及 [Psi0 × SIMPLE 复现记录](../../reproductions/simple-psi0/)（实测结果与缺陷）配套使用。
