import pandas as pd
import numpy as np


class QLearningTable:
    # 初始化
    def __init__(self, actions):
        self.actions = actions  # 动作是一个列表list
        self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)  # 初始Q表 # columns是之前说的列名。     #DataFrame是Python中Pandas库中的一种数据结构，它类似excel，是一种二维表。

    def __choose_action(self, queque_count, epsilon): #observation表示当前交叉口的状态s
        """选择动作"""
        self.check_state_exist(queque_count) #检测本state是否在q_table 中存在

        if np.random.uniform() < epsilon: #选择Q_value 最高的action
            #choose best action
            state_action = self.q_table.loc[queque_count, :]  #loc是获取一列的值:取q_table的observation行，所有列
            # some actions may have the same value, randomly choose on in these actions
            action = np.random.choice(state_action[state_action == np.max(state_action)].index) #np.max（）：取行方向的最大值
        else:
            # choose random action
            action = np.random.choice(self.actions)
        return action

    def select_action(self, queque_count, epsilon):
        """调用选择动作函数"""
        return self.__choose_action(queque_count, epsilon)

    def __update_qtable(self, queque_count, action_chosen, this_step_reward, new_queque_count, nbrQ, alpha, gamma):
        """学习过程，更新Q表"""
        self.check_state_exist(new_queque_count)  # 检测q_table中是否存在new_queque_count
        self.check_state_exist(queque_count)      # 检测q_table中是否存在queque_count
        self.nbrQ = nbrQ
        old_q_max = self.q_table.loc[queque_count, action_chosen]
        nbr_qmax_sum = sum(nbrQ)
        new_q_max = self.q_table.loc[new_queque_count, :].max()
        q_update = old_q_max * (1 - alpha) + alpha * (this_step_reward + gamma * (new_q_max + nbr_qmax_sum))
        self.q_table.loc[queque_count, action_chosen] = q_update
        return q_update

    def update_qtable(self, queque_count, action_chosen, this_step_reward, new_queque_count, nbrQ, alpha, gamma):
        """调用更新Q表的方法"""
        return self.__update_qtable(queque_count, action_chosen, this_step_reward, new_queque_count, nbrQ, alpha, gamma)

    def __check_state_exist(self, state):
        """检查状态是否存在"""
        if state not in self.q_table.index:
            # append new state to q table
            self.q_table = self.q_table.append(
                pd.Series(
                    [0] * len(self.actions),
                    index=self.q_table.columns,
                    name=state,
                )
            )

    def check_state_exist(self, state):
        """调用检查状态的函数"""
        return self.__check_state_exist(state)


    def __get_max_q(self, state):
        """获得最大Q值"""
        self.__check_state_exist(state)  #检查状态是否存在
        MaxQ = self.q_table.loc[state, :].max()
        return MaxQ

    def get_max_q(self, state):
        """调用获得最大Q值的方法"""
        return self.__get_max_q(state)