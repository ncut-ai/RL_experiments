from reinforcement_learning import ReinforcementLearning


class Agent:

    def __init__(self, agent_setting):
        self.parameters = agent_setting['parameters']
        self.state_config = agent_setting['states']  # action config
        self.action_config = agent_setting['actions']
        self.id = agent_setting['id']





        rl_setting = agent_setting['rl_settings']
        self.reinforcement_learning = ReinforcementLearning(rl_setting=rl_setting,
                                                            neighbors=self.state_config['neighbors'],
                                                            action_names=self.action_config['names'])

    def get_action_config(self):
        """返回“动作”相关信息"""
        return self.action_config

    def get_reward_config(self):
        """返回“奖励”相关信息"""
        return self.reward_config

    def get_actions_zone_2_neighbors_flow(self, id, zone_paras):
        expected_flow = zone_paras['expected_flow']
        max_flow = zone_paras['max_flow']
        first_flow = zone_paras['first_flow']
        whole_outflow = zone_paras['whole_outflow']
        whole_inflow = zone_paras['whole_inflow']
        neighbors = zone_paras['neighbors']
        accumulated_vehicles = zone_paras['accumulated_vehicles']
        old_accumulated_vehicles = zone_paras['old_accumulated_vehicles']
        critical_accumulated_vehicles = zone_paras['critical_accumulated_vehicles']

        zone_2_neighbors_transmit_flow = {}
        for elem in neighbors:

            if accumulated_vehicles > old_accumulated_vehicles * 0.9 and accumulated_vehicles < old_accumulated_vehicles:
                transmit_factor = 0.1
                zone_2_neighbors_transmit_flow[elem] = transmit_factor * self.create_transmit_flow(max_flow, expected_flow)
                accumulated_vehicles = old_accumulated_vehicles - zone_2_neighbors_transmit_flow[elem]
                self.accumulated_vehicles = self.old_accumulated_vehicles + zone_2_neighbors_transmit_flow
            elif accumulated_vehicles > old_accumulated_vehicles * 0.5 and accumulated_vehicles < old_accumulated_vehicles * 0.9:
                transmit_factor = 0.5
                zone_2_neighbors_transmit_flow[elem] = transmit_factor * self.create_transmit_flow(max_flow, expected_flow)
                accumulated_vehicles = old_accumulated_vehicles + zone_2_neighbors_transmit_flow[elem]

            elif accumulated_vehicles < old_accumulated_vehicles * 0.5:
                transmit_factor = 0.7
                zone_2_neighbors_transmit_flow[elem] = transmit_factor * self.create_transmit_flow(max_flow, expected_flow)
                accumulated_vehicles = old_accumulated_vehicles + zone_2_neighbors_transmit_flow[elem]

        self.neighbors_current_transmit_factor[id] = zone_2_neighbors_transmit_flow


    def get_action_selection_model(self):
        """获取动作选择模型"""
        return self.reinforcement_learning.get_action_selection_model()


    def select_action_eps_greedy(self, state):
        """action selection"""
        return self.reinforcement_learning.select_action_eps_greedy_neighbors(states=state)

    def after_action_zone_current_accumulated_vehicles(self, id, zone_paras, transmit_flow):

        neighbors = zone_paras['neighbors']
        neighbors_current_accumulated_vehicles = zone_paras['neighbors_current_accumulated_vehicles']
        neighbors_critical_accumulated_vehicles = zone_paras['neighbors_critical_accumulated_vehicles']

        self.neighbors.current_accumulated_vehicles = self.neighbors.current_accumulated_vehicles + transmit_flow

        self.current_accumulated_vehicles = self.current_accumulated_vehicles - transmit_flow

        return self.current_accumulated_vehicles
