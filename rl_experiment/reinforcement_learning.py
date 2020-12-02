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
        #
        self.q_table = self.__init_q_table_from_states_and_actions(state_names, action_names)  # initialize q table

    # create q-table
    def __init_q_table_from_states_and_actions(self, state_name_list, action_name_list):
        """仅完成初始化，通过添加index使空间动态增长"""
        arrays = [[] * 1] * self.state_num # looks like ep. arrays1 = [[0], [0], [0], [0]]
        idx = pd.MultiIndex.from_arrays(arrays, names=state_name_list)
        q_table = pd.DataFrame(np.nan, index=idx, columns=action_name_list)
        return q_table
