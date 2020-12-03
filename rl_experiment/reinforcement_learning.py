import numpy as np
import pandas as pd
from epsilon_greedy import *


class ReinforcementLearning:
    """
    # reinforcement_learning.py
    # 12/2/2020, created by Jay

    """

    def __init__(self, rl_setting, state_names, action_names):
        """Initialization"""
        print('RL learning...')
        self.learning_model = rl_setting['learning_model']  # basic parameters for RL algo
        self.action_selection_model = rl_setting['action_selection']  # action selection
        self.state_num = len(state_names)
        self.action_num = len(action_names)
        self.state_names = state_names
        self.action_names = action_names
        #
        self.q_table = self.__init_q_table_from_states_and_actions(state_names, action_names)  # initialize q table

    def __init_q_table_from_states_and_actions(self, state_name_list, action_name_list):
        """create q-table 仅完成初始化，通过添加index使空间动态增长"""
        arrays = [[0] * 1] * self.state_num  # looks like ep. arrays1 = [[0], [0], [0], [0]]
        idx = pd.MultiIndex.from_arrays(arrays, names=state_name_list)
        q_table = pd.DataFrame(0, index=idx, columns=action_name_list)
        return q_table

    #
    def select_action(self, state):
        """action  selection"""
        self.__check_state_exist(state)
        if self.action_selection_model['model'] == 'eps-greedy':
            eps = self.action_selection_model['paras']['epsilon']
            return epsilon_greedy(epsilon=eps, state=state, q_table=self.q_table, all_actions=self.action_names)
        elif self.action_selection_model['model'] == 'UCB': # to be
            pass
        else:
            raise Exception('there is no such a selection model')

    def get_q_value_by(self, state, action):
        """根据state和action读取Q值"""
        self.__check_state_exist(state)
        return self.q_table.loc[state, action]

    def update_q_table(self, pre_state, action, post_state, reward, neighbors_q):
        """ update q table """
        self.__check_state_exist(pre_state)
        self.__check_state_exist(post_state)
        if self.__check_reward_num(reward) == 'single_reward':
            self.__update_q_table_with_single_reward(pre_state=pre_state,
                                                     action=action,
                                                     post_state=post_state,
                                                     reward=list(reward.values())[0],
                                                     neighbors_q=neighbors_q)
        else:
            raise ValueError('reward value or type ERROR')

    def __update_q_table_with_single_reward(self, pre_state, action, post_state, reward, neighbors_q):
        """ update q table with a single reward value"""
        if self.learning_model['model'] == 'QL':
            alpha = self.learning_model['paras']['alpha']
            gamma = self.learning_model['paras']['gamma']
            pre_q = self.q_table.loc[pre_state, action]
            q_max_for_post_state = self.q_table.loc[post_state, :].max()
            neighbors_q_sum = sum(neighbors_q)

            q_new = pre_q * (1 - alpha) + alpha * (reward + gamma * (q_max_for_post_state + neighbors_q_sum))

            self.q_table.loc[pre_state, action] = q_new
        else:
            raise ValueError('No such a learning model')

    def __check_reward_num(self, reward):
        """判断reward的个数"""
        if len(reward) == 1:
            return 'single_reward'
        else:
            return 'multi_rewards'

    def __check_state_exist(self, state):
        """检查state是否存在q table中"""
        q_table_idx = self.q_table.index
        if q_table_idx.isin([state]).any():
            pass
        else:
            idx = pd.MultiIndex.from_tuples([state], names=self.state_names)
            df = pd.DataFrame(0, index=idx, columns=self.action_names)
            self.q_table = pd.concat([self.q_table, df])  # 将df合并
