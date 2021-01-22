from reinforcement_learning import ReinforcementLearning


class IntersectionAgent:
    """

    """

    def __init__(self, agent_setting):
        """Initialization"""
        print('Agent初始化……')
        self.agent_id = agent_setting['cross_id']  # agent_id denoted as cross id
        self.cross_id = self.agent_id
        self.tls_id = agent_setting['tls_id']  # 信号灯id
        self.state_config = agent_setting['states']  # basic info about states of the agent
        self.action_config = agent_setting['actions']  # action config
        self.reward_config = agent_setting['rewards']  # reward config
        self.neighbors = agent_setting['neighbors']  # neighbor agents' names
        #
        rl_setting = agent_setting['rl_settings']  # 强化学习模型
        self.reinforcement_learning = ReinforcementLearning(rl_setting=rl_setting,
                                                            state_names=self.state_config['names'],
                                                            action_names=self.action_config['names'])

    def get_tls_id(self):
        """返回信号灯ID"""
        return self.tls_id

    def get_state_config(self):
        """返回“状态”相关信息"""
        return self.state_config

    def get_action_config(self):
        """返回“动作”相关信息"""
        return self.action_config

    def get_reward_config(self):
        """返回“奖励”相关信息"""
        return self.reward_config

    def get_q_value_by(self, state, action):
        return self.reinforcement_learning.get_q_value_by(state, action)

    def get_learning_model_type(self):
        """get learning model type, QL_single, QL_neighbors, QL_neighbors_NetGame, SARSA, etc"""
        return self.reinforcement_learning.get_learning_model_type()

    def get_action_selection_model(self):
        """获取动作选择模型"""
        return self.reinforcement_learning.get_action_selection_model()

    def select_action_eps_greedy(self, state):
        """action selection"""
        return self.reinforcement_learning.select_action_eps_greedy(state=state)

    def select_action_ucb(self, state):
        """UCB算法，动作选择"""
        return self.reinforcement_learning.select_action_ucb(state=state)

    def select_action_boltzmann(self, state):
        """Boltzmann 或 Softmax 方法"""
        return self.reinforcement_learning.select_action_boltzmann(state=state)

    def update_q_table_ql_single(self, pre_state, action, post_state, reward):
        """更新Q表，只考虑本地信息"""
        self.reinforcement_learning.update_q_table_ql_single(pre_state=pre_state,
                                                             action=action,
                                                             post_state=post_state,
                                                             reward=reward)

    def update_q_table_ql_with_neighbors(self, pre_state, action, post_state, reward, neighbors_q):
        """ update q table 考虑邻居的影响"""
        self.reinforcement_learning.update_q_table_ql_with_neighbors(pre_state=pre_state,
                                                                     action=action,
                                                                     post_state=post_state,
                                                                     reward=reward,
                                                                     neighbors_q=neighbors_q)

    def update_q_table_sarsa(self, prev_state, prev_action, next_state, next_action, reward):
        """ update q table 根据SARSA算法计算Q值"""
        self.reinforcement_learning.update_q_table_sarsa(prev_state=prev_state,
                                                         prev_action=prev_action,
                                                         next_state=next_state,
                                                         next_action=next_action,
                                                         reward=reward)

    def update_q_table_actor_critic(self, prev_state, prev_action, next_state, reward):
        """ update q table 根据SARSA算法计算Q值"""
        self.reinforcement_learning.update_q_table_actor_critic(prev_state=prev_state,
                                                                prev_action=prev_action,
                                                                next_state=next_state,
                                                                reward=reward)
