########################################################################################################################
# reinforcement_learning.py
# 12/2/2020, created by Jay
#
#
#
#
########################################################################################################################
import numpy as np
import pandas as pd


class ReinforcementLearning:
    def __init__(self, rl_setting, state_names, action_names):
        print('RL learning...')
        self.learning_model = rl_setting['learning_model']  # basic parameters for RL algo
        self.action_selection_model = rl_setting['action_selection']  # action selection
        self.state_num = len(state_names)
        self.action_num = len(action_names)
        self.state_names = state_names
        self.action_names = action_names
        #
        self.q_table = self.__init_q_table_from_states_and_actions(state_names, action_names)  # initialize q table

    # create q-table
    def __init_q_table_from_states_and_actions(self, state_name_list, action_name_list):
        """仅完成初始化，通过添加index使空间动态增长"""
        arrays = [[0] * 1] * self.state_num  # looks like ep. arrays1 = [[0], [0], [0], [0]]
        idx = pd.MultiIndex.from_arrays(arrays, names=state_name_list)
        q_table = pd.DataFrame(0, index=idx, columns=action_name_list)
        return q_table

    # action selection
    def select_action(self, state):
        self.__check_state_exist(state)
        if self.action_selection_model['model'] == 'eps-greedy':
            eps = self.action_selection_model['paras']['epsilon']
            return self.__select_action_with_eps_greedy(epsilon=eps, state=state)
        elif self.action_selection_model['model'] == 'UCB':
            pass
        elif self.action_selection_model['model'] == 'max-plus':
            pass
        else:
            raise Exception('there is no such a selection model')

    # epsilon greedy
    def __select_action_with_eps_greedy(self, epsilon, state):
        if np.random.uniform() < epsilon:  # 选择Q_value 最高的action
            # choose best action
            state_action = self.q_table.loc[state, :]  # loc是获取一列的值:取q_table的observation行，所有列
            # some actions may have the same value, randomly choose on in these actions
            action = np.random.choice(state_action[state_action == np.max(state_action)].index)  # np.max（）：取行方向的最大值
        else:
            # choose random action
            action = np.random.choice(self.action_names)
        return action

    # 检查state是否存在q table中
    def __check_state_exist(self, state):
        q_table_idx = self.q_table.index
        if q_table_idx.isin([state]).any():
            pass
        else:
            idx = pd.MultiIndex.from_tuples([state], names=self.state_names)
            df = pd.DataFrame(0, index=idx, columns=self.action_names)
            self.q_table = pd.concat([self.q_table, df])  # 将df合并
