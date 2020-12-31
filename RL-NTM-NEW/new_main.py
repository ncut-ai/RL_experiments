from new_static_utilities import *
from new_NTM import NTM

#初始化NTM和agent
env_setting, agent_settings = get_settings_from_yaml(yaml_file='_new_config.yaml')
traffic_environment = NTM(NTM_setting=env_setting)
zone_agents = initialize_agents_by(agent_settings=agent_settings)
#step = 0
#开始执行循环三万步
##循环内部
##1.读取agent状态
##2.动作选择
##3.在NTM里执行动作
##4.在NTM里获得奖励
##5.获得新状态
##6.获得当前状态的Q值
##更新Q表

for t in range(10000):
    ##读取agent状态
    all_agents_states_t = get_all_agents_states_by(environment=traffic_environment,
                                                   agents_list=zone_agents)
    all_agents_current_states = all_agents_states_t
    #print(all_agents_current_states)

    all_agents_current_actions = get_all_agents_actions_by(agents_states=all_agents_current_states,
                                                           agents_list=zone_agents)
    print(all_agents_current_actions)

    # execute_actions_in_environment(environment=traffic_environment,
    #                                actions_list=all_agents_current_actions,
    #                                agents_list=zone_agents)



    # all_agents_current_rewards = get_all_agents_rewards_by(environment=traffic_environment,
    #                                                        agents_list=zone_agents)

    ##获取新状态

    ##更新Q表

