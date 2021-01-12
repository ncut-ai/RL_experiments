# Reinforcement Learning Experiment
## 0. 结构说明
### 0.1 environment class
1. 表示系统环境
2. 完成数据检索
3. 完成agent动作执行
### 0.2 agent class
1. 表示路口
2. 与环境交互
### 0.3 reinforcement class
1. 与强化学习有关
2. 作为agent的组成部分
3. 包括动作选择
4. 包括Q值 update function
## 1. 基本定义
### 1.1 状态
####1.1.1 边的排队长度
<pre><code>
names: ['边的排队长度']
      types: {
        '边的排队长度': 'queue_count'，
      }
      retrieve_para: {
        '边的排队长度': 'eJ2J1',
      }
</code></pre>
<pre><code>
traci.edge.getLastStepHaltingNumber(edgeID=edge_id)
</code></pre>
#####1.1.2 红灯时间（未完成）
<pre><code>
names: ['红灯时间']
      types: {
        '红灯时间': 'red_time',
      }
      retrieve_para: {
        '红灯时间': 'eJ2J1',  
</code></pre>
<pre><code>

</code></pre>>
####1.1.3 当前相位持续时间（待修改）
<pre><code>
names: ['当前相位持续时间']
      types:{
        '当前相位持续时间': 'current_phase_duration'
      }
      retrieve_para: {
        '当前相位持续时间'：‘J1’，
      }
</code></pre>
<pre><code>
traci.trafficlight.getPhaseDuration(self.ID)
</code></pre>
####1.1.4 交通相位划分（待修改）
<pre><code>
names: ['相位划分']
      types:{
        '相位划分': 'time interval'，
      }
      retrieve_para: {
        '相位划分'：‘J1’，
</code></pre>
<pre><code>
traci.trafficlight.getNextSwitch()
</code></pre>
####1.1.5 边的平均速度
<pre><code>
names:['边的平均速度']
      types:{
        '边的平均速度': 'mean_speed'
      }
      retrieve_para: {
        '边的平均速度'：‘eJ2J1’，
      }
</code></pre>
<pre><code>
traci.edge.getLastStepMeanSpeed(edge_id)
</code></pre>
####1.1.6 边占有率
<pre><code>
names: ['占有率']
      types: {
        '占有率': 'occupancy',
      }
      retrieve_para: {
        '占有率': 'eJ2J1',
      }
</code></pre>
<pre><code>
traci.edge.getLastStepOccupancy(edgeID=edge_id)
</code></pre>
####1.1.7 边等待时间
<pre><code>
names: '等待时间'
      types: {
        '等待时间': 'waiting_time',
      }
      retrieve_para: {
        '等待时间': 'eJ2J1',
      }
</code></pre>
<pre><code>
traci.edge.getWaitingTime(edgeID=edge_id)
</code></pre>
####1.1.8 边旅行时间
<pre><code>
names: '旅行时间'
      types: {
        '旅行时间': 'travel_time',
      }
      retrieve_para: {
        '旅行时间': 'eJ2J1',
      }
</code></pre>
<pre><code>
traci.edge.getTravelTime(edgeID=edge_id)
</code></pre>
####1.1.9 边平均车辆长度
<pre><code>
names: ['平均车辆长度']
      types: {
        '平均车辆长度': 'ave_length',
      }
      retrieve_para: {
        '平均车辆长度': 'eJ2J1',
      }
</code></pre>
<pre><code>
traci.edge.getLastStepLength(edge_id)
</code></pre>
####1.1.10 车道排队长度
<pre><code>
names: ['车道排队长度']
      types: {
        '车道排队长度': 'queue_count_lane',
      }
      retrieve_para: {
        '车道排队长度': 'eJ2J1_1',
      }
</code></pre>
<pre><code>
traci.lane.getLastStepHaltingNumber(lane_id)
</code></pre>
####1.1.11 车道平均速度
<pre><code>
names:['车道平均速度']
      types:{
        '车道平均速度': 'mean_speed_lane'
      }
      retrieve_para: {
        '车道平均速度': 'eJ2J1_id',
</code></pre>
<pre><code>
traci.lane.getLastStepMeanSpeed(lane_id)
</code></pre>

####1.1.12 车道占有率
<pre><code>
names: ['车道占有率']
      types: {
        '车道占有率': 'occupancy_lane',
      }
      retrieve_para: {
        '车道占有率': 'eJ2J1_1',
      }
</code></pre>
<pre><code>
traci.lane.getLastStepOccupancy(lane_id)
</code></pre>
####1.1.13 车道等待时间
<pre><code>
names: ['车道等待时间']
      types: {
        '车道等待时间': 'waiting_time_lane'
      }
      retrieve_para: {
        '车道等待时间': 'eJ2J1_1',
      }
</code></pre>
<pre><code>
traci.lane.getWaitingTime(lane_id)
</code></pre>
####1.1.14 车道旅行时间
<pre><code>
names: ['车道旅行时间']
      types: {
        '车道旅行时间': 'travel_time_lane'
      }
      retrieve_para: {
        '车道旅行时间': 'eJ2J1_1',
      }
</code></pre>
<pre><code>
traci.lane.getTravelTime(lane_id)
</code></pre>
####1.1.15 车道平均车辆长度
<pre><code>
names: ['车道平均车辆长度']
      types: {
        '车道平均车辆长度': 'ave_length_lane',
      }
      retrieve_para: {
        '车道平均车辆长度': 'eJ2J1_1',
      }
</code></pre>
<pre><code>
traci.lane.getLastStepLength(lane_id)
</code></pre>
### 1.2 动作
####1.2.1 保持不变
<pre><code>
names: '保持不变'
      types: {
        '保持不变': 'keep',
      }
</code></pre>
####1.2.2 变换相位
<pre><code>
names: 'J1路口变换到2相位'
      types: {
        'J1路口变换到2相位': 'switch_to_phase',
      }
      retrieve_para: {
        'J1路口变换到2相位': ['J1', 2]
      }
</code></pre>
<pre><code>
traci.trafficlight.setPhase(tls_id, phase_id)
</code></pre>
####1.2.3 设置车道最大速度
<pre><code>
names: '设置最大速度'
      types: {
        '设置最大速度': 'set_max_speed',
      }
      retrieve_para: {
        '设置最大速度': ['eJ2J1_1', 80],
      }
</code></pre>

<pre><code>
traci.vehicle.SetMaxSpeed(self,lanelID,speed)
</code></pre>
####1.2.4 设置相位持续时间（需要修改）
<pre><code>
names: '增加J1相位设置新的相位持续时间'
      types: {
        '设置新的相位持续时间': 'set_phaseDuration',
      }
      retrieve_para: {
        '设置新的相位持续时间': 'J1',
      }
</code></pre>
<pre><code>
traci.edge.SetPhaseDuration(self,tlslID,phaseDuration)
</code></pre>
#### 1.2.5 设置车道速度
<pre><code>
names: '设置新的速度'
      types: {
        '设置新速度': 'set_new_speed',
      }
      retrieve_para: {
        '设置新速度': ['eJ2J1_1', 80],
</code></pre>
<pre><code>
traci.vehicle.SetSpeed(self,lanelID,speed)
</code></pre>

### 1.3 奖励
#### 1.3.1 路口总等待时间
<pre><code>
compute_type: 'single'  
names: ['路口总等待时间']
types: {
        '路口总等待时间': 'sum_waiting_time',
       }
retrieve_para: {
        '路口总等待时间': [ 'eDJ1J1', 'eJ2J1', 'eJ4J1', 'eJ1DJ7' ],
       }
</code></pre>
#### 1.3.2 路口总排队长度
<pre><code>
compute_type: 'single'  
names: ['路口总排队长度']
types: {
        '路口总排队长度': 'sum_queue_count',
       }
retrieve_para: {
        '路口总排队长度': [ 'eDJ1J1', 'eJ2J1', 'eJ4J1', 'eJ1DJ7' ],
       }
</code></pre>
#### 1.3.3 路口总旅行时间
<pre><code>
compute_type: 'single'  
names: ['路口总旅行时间']
types: {
        '路口总旅行时间': 'sum_travel_time',
       }
retrieve_para: {
        '路口总旅行时间': [ 'eDJ1J1', 'eJ2J1', 'eJ4J1', 'eJ1DJ7' ],
       }
</code></pre>
#### 1.3.4 路口占有率
<pre><code>
compute_type: 'single'  
names: ['路口总占有率']
types: {
        '路口总占有率': 'sum_occupancy'
       }
retrieve_para: {
        '路口总占有率': [ 'eDJ1J1', 'eJ2J1', 'eJ4J1', 'eJ1DJ7' ],
       }
</code></pre>
#### 1.3.5 平均速度
<pre><code>
compute_type: 'single'  
names: ['路口平均速度']
types: {
        '路口平均速度': 'ave_mean_speed'
       }
retrieve_para: {
        '路口平均速度': [ 'eDJ1J1', 'eJ2J1', 'eJ4J1', 'eJ1DJ7' ],
       }
</code></pre>
#### 1.3.6 平均车辆长度
<pre><code>
compute_type: 'single'  
names: ['路口平均车辆长度']
types: {
        '路口平均车辆长度': 'ave_length'
       }
retrieve_para: {
        '路口平均车辆长度': [ 'eDJ1J1', 'eJ2J1', 'eJ4J1', 'eJ1DJ7' ],
       }
</code></pre>
## 2. 主要模型
### 2.1 动作选择模型
#### 2.1.1 yaml配置
1. epsilon greedy  
<pre><code>
model: 'eps_greedy'    
paras: {
          'epsilon': 0.9
       }
</code></pre>

2. UCB 
<pre><code>
model: 'UCB'
paras: { }
</code></pre>

3. Boltzmann 
<pre><code>
model: 'Boltzmann'
paras: { 
    'temperature': 0.8
 }
</code></pre>

### 2.2 Q-Learning算法实现
#### 2.2.1 算法流程
rl_main_ql.py

#### 2.2.2 yaml文件配置
a. Q-Learning 算法（单路口）
<pre><code>
model: 'QL'
paras: {
          'alpha': 0.01,
          'gamma': 0.9,
          'epsilon': 0.9
        }
</code></pre>
b. Q-Learning 算法（与邻居通信）
<pre><code>
model: 'QL_with_neighbors'
paras: {
          'alpha': 0.01,
          'gamma': 0.9,
          'epsilon': 0.9
        }
</code></pre>
### 2.3 SARSA算法
#### 2.3.1 算法流程
rl_main_sarsa.py
#### yaml配置
<pre><code>
learning_model:
        model: 'sarsa'
        paras: {
          'alpha': 0.01,
          'gamma': 0.9,
        }
</code></pre>
### 2.4 Actor-Critic算法
#### 2.4.1 算法流程
rl_main_actor-critic.py
#### 2.4.2 yaml配置
<pre><code>
learning_model:
        model: 'actor-critic'
        paras: {
          'alpha': 0.01
        }
</code></pre>
### 2.5 奖励计算方法
奖励的计算结果为单一值
a. 简单计算方法  
<pre><code>
compute_type: 'single'  
names: '路口总等待时间'
types: {
        '路口总等待时间': 'sum_waiting_time',
       }
retrieve_para: {
        '路口总等待时间': [ 'eDJ1J1', 'eJ2J1', 'eJ4J1', 'eJ1DJ7' ],
       }
</code></pre>
b. 简单计算方法，进行等级划分
按指标等级划分为：低、中、高
<pre><code>
compute_type: 'single_qualitative'  
names: '路口总等待时间'
types: {
        '路口总等待时间': 'sum_waiting_time',
       }
retrieve_para: {
        '路口总等待时间': [ 'eDJ1J1', 'eJ2J1', 'eJ4J1', 'eJ1DJ7' ],
       }
</code></pre>
c. 加权计算方法  
针对两个及以上的奖励
$$
r^i_{t+1}=r^{i,1}_{t+1}+r^{i,2}_{t+1}
$$
计算公式为：
$$
r^i_{t+1}=[\eta_1\times(r^{i,j,1}_{t+1}+r^{i,j,2}_{t+1})]+[\eta_2\times(r^{i,k,1}_{t+1}+r^{i,k,2}_{t+1})]
$$

<pre><code>
compute_type: 'weighted'  
names: ['东直排队', '西直排队']
types: {
        '东直排队': 'queue',  
        '西直排队': 'queue'
       }
retrieve_para: {
        '东直排队': 'eDJ1J1',  
        '西直排队': 'eJ2J1'
       }
weight_vals: {
        '东直排队': 0.4,  
        '西直排队': 0.6
       }
</code></pre>
d. 组合计算方法
$$
r^i_{t+1}(s^i_{t+1})=\eta_1\times(\frac{1}{|H^i|}\sum_{d^i\in D^i}t^{i,d^i}_{r,t+1})+\eta_2\times(\frac{1}{J^i}\sum_{j\in J^i}\sum_{d^j\in D^j}\frac{n^{j,d^j}_{q,t+1}}{|D^j|})
$$
<pre><code>
type: 'compound'  
names: ['红灯时长', '西直排队']
types: {
        '东直排队': 'queue',  
        '西直排队': 'queue'
       }
retrieve_para: {
        '东直排队': 'eDJ1J1',  
        '西直排队': 'eJ2J1'
       }
weight_vals: {
        '东直排队': 0.4,  
        '西直排队': 0.6
       }
</code></pre>

### 2.5 网络博弈模型 （未添加）

## 3. Sumo仿真模型
1. 6个路口
2. 仅包含直行（右转影响可忽略）
## 4. 待完善部分
### a. 动作
1. 动作仅有switch，需要重新设计
### b. 学习算法
1. 其他的算法需要添加：SARSA等
### c. 结合网络博弈模型
1. Network Game 模型
### d. 结果绘图
1. analysis_main.py
