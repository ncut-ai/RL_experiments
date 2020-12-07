import pandas as pd

from epsilon_greedy import epsilon_greedy
from q_learning_single_local import q_learning_local_only
from q_learning_with_neighbors import q_learning_with_neighbors


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
    def select_action_eps_greedy(self, state):
        """action  selection epsilon greedy算法"""
        self.__check_state_exist(state)
        eps = self.action_selection_model['paras']['epsilon']
        return epsilon_greedy(epsilon=eps, state=state, q_table=self.q_table, all_actions=self.action_names)

    def select_action_ucb(self, state):
        """UCB算法，动作选择"""
        # check state in q table
        self.__check_state_exist(state)
        # 获取参数

        # 调用计算函数，并返回
        return 0

    def get_q_value_by(self, state, action):
        """根据state和action读取Q值"""
        self.__check_state_exist(state)
        return self.q_table.loc[state, action]

    def get_action_selection_model(self):
        """获得该Agent的动作选择模型"""
        return self.action_selection_model['model']

    def get_learning_model_type(self):
        """get learning model type, QL_single, QL_neighbors, QL_neighbors_NetGame, SARSA, etc"""
        return self.learning_model['model']

    def __update_q_table_by(self, state, action, q):
        """ update q table with state,action,q"""
        self.q_table.loc[state, action] = q

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

    def update_q_table_ql_single(self, pre_state, action, post_state, reward):
        """更新Q表，只考虑本地信息"""
        self.__check_state_exist(pre_state)
        self.__check_state_exist(post_state)
        if self.__check_reward_num(reward) == 'single_reward':
            # 获取参数
            alpha = self.learning_model['paras']['alpha']
            gamma = self.learning_model['paras']['gamma']
            reward = list(reward.values())[0]
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
        else:
            raise ValueError('reward value or type ERROR')

    def update_q_table_ql_with_neighbors(self, pre_state, action, post_state, reward, neighbors_q):
        """ update q table """
        self.__check_state_exist(pre_state)
        self.__check_state_exist(post_state)
        if self.__check_reward_num(reward) == 'single_reward':
            alpha = self.learning_model['paras']['alpha']
            gamma = self.learning_model['paras']['gamma']
            reward = list(reward.values())[0]
            pre_q = self.q_table.loc[pre_state, action]
            q_max_for_post_state = self.q_table.loc[post_state, :].max()
            #
            q_new = q_learning_with_neighbors(alpha=alpha,
                                              gamma=gamma,
                                              reward=reward,
                                              pre_q=pre_q,
                                              q_max_for_post_state=q_max_for_post_state,
                                              neighbors_q=neighbors_q)
            #
            self.__update_q_table_by(state=pre_state, action=action, q=q_new)
        else:
            raise ValueError('reward value or type ERROR')
