########################################################################################################################
#
#
#
#
#
#
########################################################################################################################
from reinforcement_learning import ReinforcementLearning


class IntersectionAgent:
    def __init__(self, agent_setting, rl_setting):
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
    # 返回“状态”相关信息
    def get_state_config(self):
        return self.state_config
    # 返回“状态”相关信息
    def get_action_config(self):
        return self.action_config
    # action selection
    def select_action(self,state):
        return self.reinforcement_learning.select_action(state)