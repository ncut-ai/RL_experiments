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
#### 1.1.1 定义：在yaml中
#### 1.1.2 实现
### 1.2 动作
#### 1.2.1 定义：在yaml中
#### 1.2.2 实现
### 1.3 奖励
#### 1.3.1 允许的定义
#### 1.3.2 实现
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
### 2.4 奖励计算方法
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
