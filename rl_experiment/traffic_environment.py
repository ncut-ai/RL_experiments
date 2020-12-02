########################################################################################################################
# traffic_environment.py
# 12/2/2020 created by 
#
# Here the TrafficEnvironment Class defined with which a traffic simulation model is described, highly correlating to
# SUMO the platform.
#
########################################################################################################################
import traci





class TrafficEnvironment:
    def __init__(self, env_setting):
        print('初始化仿真环境……')
        traci.start(env_setting['sumo_start_config']) # initialize traci

    # 执行一步仿真
    def simulation_step(self):
        traci.simulationStep()

    # retrieve state value
    def retrieve_state_by(self,state_type,paras):
        if state_type=='queue_count':
            return self.__retrieve_queue_count_on_edge(edge_id=paras)
        else:
            raise Exception('there is no such bizarre type')
    # retrieve queue count on edge
    def __retrieve_queue_count_on_edge(self,edge_id):
        return traci.edge.getLastStepHaltingNumber(edgeID=edge_id)

    # execute action
    def execute_action_by(self,cross_id,action,action_config):
        if action_config['types'][action] == 'keep':
            pass
        elif action_config['types'][action] == 'switch':
            self.__execute_action_switch_to_next_phase(cross_id=cross_id)
        else:
            raise Exception('there is no such action')
    # 切换到下一个相位
    def __execute_action_switch_to_next_phase(self,cross_id):
        traci.trafficlight.setPhaseDuration(cross_id,0)