import pandas as pd
import numpy as np

from epsilon_greedy import epsilon_greedy
from q_learning_single_local import q_learning_local_only
from q_learning_with_neighbors import q_learning_with_neighbors


class ReinforcementLearning:
    ## 初始化强化学习类
    """
    # reinforcement_learning.py
    # 12/2/2020, created by Jay

    """
    def __init__(self, rl_setting, neighbors, action_names):
        ##类的初始化， 属性rl_setting, 属性neighbors, 属性action_names
        """Initialization"""
        print('RL learning...')
        self.learning_model = rl_setting['learning_model']  # basic parameters for RL algo
        self.action_selection_model = rl_setting['action_selection']  # action selection
        self.neighbors = neighbors
        self.action_num = len(action_names)
        self.action_names = action_names

        #
        self.q_table =self.__get_zone_neighbors_q_table(neighbors)

## 得到zone的Q表
    def __init_q_table_from_states_and_actions(self, action_name_list):
        arrays = [[0] * 1]
        idx = arrays
        q_table = pd.DataFrame(0, index=idx, columns=action_name_list, dtype=np.int)

        return q_table

## 生成每个zone的包含邻居的Q表  zone1 = {zone2_Q表， zone3_Q表}
    def __get_zone_neighbors_q_table(self, neighbors):
        zone_neighbors_q_table = {}
        for elem in neighbors:
            zone_q_table = self.__init_q_table_from_states_and_actions(action_name_list=self.action_names)
            zone_neighbors_q_table[elem] = zone_q_table
        # print(zone_neighbors_q_table)
        return zone_neighbors_q_table

#### 下面每一个函数使用时都需要先确定是哪个Q表

    #
    def select_action_eps_greedy_neighbors(self, states):
        actions = {}
        for elem, state in states.items():
            actions[elem] = self.select_action_eps_greedy(neighbor_name=elem, state=state)
        return actions



    def select_action_eps_greedy(self, neighbor_name, state):
        """action  selection epsilon greedy算法"""
        self.__check_state_exist(neighbor_name, state)
        eps = self.action_selection_model['paras']['epsilon']
        return epsilon_greedy(epsilon=eps, state=state, q_table=self.q_table[neighbor_name], all_actions=self.action_names)

    def get_q_value_by(self, neighbor_name, state, action):
        """根据state和action读取Q值"""
        self.__check_state_exist(neighbor_name, state)
        return self.q_table[neighbor_name].loc[state, action]

    def get_action_selection_model(self):
        """获得该Agent的动作选择模型"""
        return self.action_selection_model['model']

    def get_learning_model_type(self):
        """get learning model type, QL_single, QL_neighbors, QL_neighbors_NetGame, SARSA, etc"""
        return self.learning_model['model']

    def __update_q_table_by(self,neighbor_name, state, action, q):
        """ update q table with state,action,q"""
        self.q_table[neighbor_name].loc[state, action] = q

    def __check_state_exist(self, neighbor_name, state):
        if state in self.q_table[neighbor_name].index:
            pass
        else:
            self.q_table[neighbor_name] = self.q_table[neighbor_name].append(
                pd.Series(
                    [0] * self.action_num,
                    index=self.q_table[neighbor_name].columns,
                    name=state
                )
            )

    def update_q_table_ql_single(self,neighbor_name, pre_state, action, post_state, reward):
        """更新Q表，只考虑本地信息"""
        self.__check_state_exist(neighbor_name, pre_state)
        self.__check_state_exist(neighbor_name, post_state)

        # 获取参数
        alpha = self.learning_model['paras']['alpha']
        gamma = self.learning_model['paras']['gamma']
        pre_q = self.q_table[neighbor_name].loc[pre_state, action]
        q_max_for_post_state = self.q_table[neighbor_name].loc[post_state, :].max()
        #
        q_new = q_learning_local_only(alpha=alpha,
                                      gamma=gamma,
                                      reward=reward,
                                      pre_q=pre_q,
                                      q_max_for_post_state=q_max_for_post_state)
        #
        self.__update_q_table_by(neighbor_name=neighbor_name, state=pre_state, action=action, q=q_new)



    def update_q_table_ql_with_neighbors(self, neighbor_name, pre_state, action, post_state, reward, neighbors_q):
        """ update q table """
        self.__check_state_exist( neighbor_name,pre_state)
        self.__check_state_exist( neighbor_name,post_state)

        alpha = self.learning_model['paras']['alpha']
        gamma = self.learning_model['paras']['gamma']
        pre_q = self.q_table[neighbor_name].loc[pre_state, action]
        q_max_for_post_state = self.q_table[neighbor_name].loc[post_state, :].max()
        #
        q_new = q_learning_with_neighbors(alpha=alpha,
                                          gamma=gamma,
                                          reward=reward,
                                          pre_q=pre_q,
                                          q_max_for_post_state=q_max_for_post_state,
                                          neighbors_q=neighbors_q)
        #
        self.__update_q_table_by( neighbor_name=neighbor_name,state=pre_state, action=action, q=q_new)


