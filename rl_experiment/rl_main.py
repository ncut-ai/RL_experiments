import intersection_agent
import rl_learning
import traffic_environment

'''
初始化
1、读取配置文件
2、实例化环境和Agents
'''

traffic_environment = TrafficEnvironment()
for key,val in agent_settings.items():
    intersection_agents[key] = IntersectionAgent(val)

'''
开始仿真
'''
while step <= 3600
    #获取当前状态
    for key, agent in intersection_agents.items():
        traffic_environment.get_current_state_by(state_types, state_retrieve_paras)
    # action selection
    #agent返回动作
    traffic_environment.take_action()
    #执行仿真
    traffic_environment.simulation_step()
    #获取奖励

    #更新Q表