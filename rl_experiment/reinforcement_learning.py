import pandas as pd

from action_selection.UCB import upper_confidence_bounds
from action_selection.epsilon_greedy import epsilon_greedy
from QL.q_learning_single_local import q_learning_local_only
from QL.q_learning_with_neighbors import q_learning_with_neighbors
from SARSA.sarsa import sarsa_func
from ActorCritic.actor_critic import actor_critic


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
        #
        self.state_action_count_table = self.__init_state_action_count_table_from_states_and_actions(state_names,
                                                                                                     action_names)  # 状态，动作）对，被访问次数统计表

    def __init_q_table_from_states_and_actions(self, state_name_list, action_name_list):
        """create q-table 仅完成初始化，通过添加index使空间动态增长"""
        arrays = [[0] * 1] * self.state_num  # looks like ep. arrays1 = [[0], [0], [0], [0]]
        idx = pd.MultiIndex.from_arrays(arrays, names=state_name_list)
        q_table = pd.DataFrame(0, index=idx, columns=action_name_list)
        return q_table

    def __init_state_action_count_table_from_states_and_actions(self, state_name_list, action_name_list):
        """创建状态动作访问次数统计表，用于统计状态动作对出现的次数"""
        arrays = [[0] * 1] * self.state_num  # looks like ep. arrays1 = [[0], [0], [0], [0]]
        idx = pd.MultiIndex.from_arrays(arrays, names=state_name_list)
        state_action_count_table = pd.DataFrame(1, index=idx, columns=action_name_list)  # 初始化值为 1
        return state_action_count_table

    #
    def select_action_eps_greedy(self, state):
        """action  selection epsilon greedy算法"""
        self.__check_state_exist(state)
        eps = self.action_selection_model['paras']['epsilon']
        return epsilon_greedy(epsilon=eps, state=state, q_table=self.q_table, all_actions=self.action_names)

    def select_action_ucb(self, state):
        """UCB算法，动作选择"""
        # check state in q table
        self.__check_state_exist(state)
        self.__check_state_exist_in_count_table(state)
        # 调用计算函数
        action_selected = upper_confidence_bounds(state=state,
                                                  q_table=self.q_table,
                                                  state_action_count_table=self.state_action_count_table)
        # 增加计数
        self.__add_to_state_action_count_table_by(state=state, action=action_selected)
        # 返回
        return action_selected

    def get_q_value_by(self, state, action):
        """根据state和action读取Q值"""
        self.__check_state_exist(state)
        return self.q_table.loc[state, action]

    def get_q_max_by(self, state):
        """获取state对应的最大Q值"""
        return self.q_table.loc[state, :].max()

    def get_action_selection_model(self):
        """获得该Agent的动作选择模型"""
        return self.action_selection_model['model']

    def get_learning_model_type(self):
        """get learning model type, QL_single, QL_neighbors, QL_neighbors_NetGame, SARSA, etc"""
        return self.learning_model['model']

    def __update_q_table_by(self, state, action, q):
        """ update q table with state,action,q"""
        self.q_table.loc[state, action] = q

    def __check_state_exist(self, state):
        """检查state是否存在q table中"""
        q_table_idx = self.q_table.index
        if q_table_idx.isin([state]).any():
            pass
        else:
            idx = pd.MultiIndex.from_tuples([state], names=self.state_names)
            df = pd.DataFrame(0, index=idx, columns=self.action_names)
            self.q_table = pd.concat([self.q_table, df])  # 将df合并

    def __check_state_exist_in_count_table(self, state):
        """在统计表中检查状态是否存在"""
        q_table_idx = self.state_action_count_table.index
        if q_table_idx.isin([state]).any():
            pass
        else:
            idx = pd.MultiIndex.from_tuples([state], names=self.state_names)
            df = pd.DataFrame(1, index=idx, columns=self.action_names)  # 初始化为1次
            self.state_action_count_table = pd.concat([self.state_action_count_table, df])  # 将df合并

    def __add_to_state_action_count_table_by(self, state, action):
        """在状态动作计数表中对应位置+1"""
        self.state_action_count_table.loc[state, action] += 1

    def update_q_table_ql_single(self, pre_state, action, post_state, reward):
        """更新Q表，只考虑本地信息"""
        self.__check_state_exist(pre_state)
        self.__check_state_exist(post_state)
        # 获取参数
        alpha = self.learning_model['paras']['alpha']
        gamma = self.learning_model['paras']['gamma']

        pre_q = self.q_table.loc[pre_state, action]
        q_max_for_post_state = self.q_table.loc[post_state, :].max()
        #
        q_new = q_learning_local_only(alpha=alpha,
                                      gamma=gamma,
                                      reward=reward,
                                      pre_q=pre_q,
                                      q_max_for_post_state=q_max_for_post_state)
        #
        self.__update_q_table_by(state=pre_state, action=action, q=q_new)

    def update_q_table_ql_with_neighbors(self, pre_state, action, post_state, reward, neighbors_q):
        """ update q table """
        self.__check_state_exist(pre_state)
        self.__check_state_exist(post_state)

        alpha = self.learning_model['paras']['alpha']
        gamma = self.learning_model['paras']['gamma']

        pre_q = self.get_q_value_by(pre_state, action)
        q_max_for_post_state = self.get_q_max_by(post_state)
        #
        q_new = q_learning_with_neighbors(alpha=alpha,
                                          gamma=gamma,
                                          reward=reward,
                                          pre_q=pre_q,
                                          q_max_for_post_state=q_max_for_post_state,
                                          neighbors_q=neighbors_q)
        #
        self.__update_q_table_by(state=pre_state, action=action, q=q_new)


    def update_q_table_sarsa(self, prev_state, prev_action, next_state, next_action, reward):
        """ update q table 根据SARSA算法计算Q值"""
        self.__check_state_exist(prev_state)
        self.__check_state_exist(next_state)
        #
        alpha = self.learning_model['paras']['alpha']
        gamma = self.learning_model['paras']['gamma']
        #
        #
        prev_q = self.get_q_value_by(prev_state, prev_action)
        next_q = self.get_q_value_by(next_state, next_action)
        #
        q_new = sarsa_func(prev_q=prev_q, next_q=next_q, reward=reward, alpha=alpha, gamma=gamma)
        #
        self.__update_q_table_by(state=prev_state, action=prev_action, q=q_new)

    def update_q_table_actor_critic(self, prev_state, prev_action, next_state, reward):
        """ update q table 根据SARSA算法计算Q值"""
        self.__check_state_exist(prev_state)
        self.__check_state_exist(next_state)
        #
        alpha = self.learning_model['paras']['alpha']
        #
        #
        prev_q = self.get_q_value_by(prev_state, prev_action)
        prev_q_max = self.get_q_max_by(prev_state)
        next_q_max = self.get_q_max_by(next_state)
        #
        q_new = actor_critic(prev_q=prev_q, prev_q_max=prev_q_max, next_q_max=next_q_max, reward=reward, alpha=alpha)
        #
        self.__update_q_table_by(state=prev_state, action=prev_action, q=q_new)