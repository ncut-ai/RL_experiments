# Reinforcement Learning Experiment
## 结构说明
### environment class
1. 表示系统环境
2. 完成数据检索
3. 完成agent动作执行
### agent class
1. 表示路口
2. 与环境交互
### reinforcement class
1. 与强化学习有关
2. 作为agent的组成部分
3. 包括动作选择
4. 包括Q值 update function
## 主要模型
### action selection models
1. epsilon greedy
2. UCB
### learning models
1. Q-Learning 算法（单路口）
2. Q-Learning 算法（与邻居通信）
### 网络博弈模型
## Sumo仿真模型
1. 6个路口
2. 仅包含直行（右转影响可忽略）
## 待完善部分
### 动作
1. 动作仅有switch，需要重新设计
2. 其他的算法需要添加：SARSA等
3. Network Game 模型
