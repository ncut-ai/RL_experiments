########################################################################################################################
#
#
#
#
#
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