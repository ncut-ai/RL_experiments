"""
# traffic_environment.py
# 12/2/2020 created by 
#
# Here the TrafficEnvironment Class defined with which a traffic simulation model is described, highly correlating to
# SUMO the platform.
"""

import traci


class TrafficEnvironment:
    def __init__(self, env_setting):
        print('初始化仿真环境……')
        traci.start(env_setting['sumo_start_config'])  # initialize traci

    def simulation_step(self):
        """# 执行一步仿真"""
        traci.simulationStep()

    def retrieve_state_by(self, state_type, paras):
        """# retrieve state value"""
        if state_type == 'queue_count':
            return self.__retrieve_queue_count_on_edge(edge_id=paras)
        else:
            raise Exception('there is no such bizarre state type')

    def retrieve_reward_by(self, reward_type, paras):
        """# retrieve reward value"""
        if reward_type == 'sum_waiting_time':
            return self.__retrieve_sum_waiting_time_on_edges(edge_ids=paras)
        else:
            raise Exception('there is no such reward type')

    def __retrieve_queue_count_on_edge(self, edge_id):
        """retrieve queue count on edge"""
        return traci.edge.getLastStepHaltingNumber(edgeID=edge_id)

    def __retrieve_sum_waiting_time_on_edges(self, edge_ids):
        """retrieve waiting time sum on edges"""
        sum_waiting_time = 0
        for edge_id in edge_ids:
            sum_waiting_time = sum_waiting_time + traci.edge.getWaitingTime(edge_id)
        return sum_waiting_time

    def execute_action_by(self, cross_id, action, action_config):
        """execute action"""
        if action_config['types'][action] == 'keep':
            pass
        elif action_config['types'][action] == 'switch':
            self.__execute_action_switch_to_next_phase(cross_id=cross_id)
        else:
            raise Exception('there is no such action')

    def __execute_action_switch_to_next_phase(self, cross_id):
        """切换到下一个相位"""
        traci.trafficlight.setPhaseDuration(cross_id, 0)

    def pre_run_simulation_to_prepare(self, pre_steps):
        """ pre run simulation with doing nothing"""
        traci.simulationStep(pre_steps)
