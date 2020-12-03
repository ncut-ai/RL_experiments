from reinforcement_learning import ReinforcementLearning

class IntersectionAgent:
    """

    """

    def __init__(self, agent_setting, rl_setting):
        """Initialization"""
        print('Agent初始化……')
        self.agent_id = agent_setting['cross_id']  # agent_id denoted as cross id
        self.cross_id = self.agent_id
        self.state_config = agent_setting['states']  # basic info about states of the agent
        self.action_config = agent_setting['actions']  # action config
        self.reward_config = agent_setting['rewards']  # reward config
        self.neighbors = agent_setting['neighbors']  # neighbor agents' names
        #
        self.reinforcement_learning = ReinforcementLearning(rl_setting=rl_setting,
                                                            state_names=self.state_config['names'],
                                                            action_names=self.action_config['names'])

    def get_state_config(self):
        """返回“状态”相关信息"""
        return self.state_config

    def get_action_config(self):
        """返回“动作”相关信息"""
        return self.action_config

    def get_reward_config(self):
        """返回“奖励”相关信息"""
        return self.reward_config

    def get_q_value_by(self,state,action):
        return self.reinforcement_learning.get_q_value_by(state,action)

    def select_action(self, state):
        """action selection"""
        return self.reinforcement_learning.select_action(state)

    def update_q_table(self, pre_state,action,post_state,reward,neighbors_q):
        """ update q table """
        self.reinforcement_learning.update_q_table(pre_state=pre_state,
                                                   action=action,
                                                   post_state=post_state,
                                                   reward=reward,
                                                   neighbors_q=neighbors_q)
