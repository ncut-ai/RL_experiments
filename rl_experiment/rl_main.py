"""
开始仿真

while step <= 3600
    #获取当前状态
    #agent返回动作
    #执行仿真
    #获取奖励
    #更新Q表
"""

from static_utilities import *
from traffic_environment import TrafficEnvironment

'''
# Initialization
# 1. read config info from file
# 2. initialize the traffic simulation environment and all agents with info about reinforcement learning
# 3. initialize the network game model (to be)
'''
# 1.
env_setting, net_game_setting, rl_setting, agent_settings = get_settings_from_yaml(
    yaml_file='rl_experiment_config.yaml')  # to read settings info
# 2.
traffic_environment = TrafficEnvironment(env_setting=env_setting)  # traffic environment
intersection_agents = initialize_agents_by(agent_settings=agent_settings,
                                           rl_setting=rl_setting)  # all agents:in a dict: [key is an agent's name] : [val is the Agent object from IntersectionAgent Class]
# 3.


'''begin'''
step = 0  #
traffic_environment.pre_run_simulation_to_prepare(100)  # pre run simulation with doing nothing
# get current states
all_agents_states_t = get_all_agents_states_by(environment=traffic_environment,
                                               agents_list=intersection_agents)
while step <= 3600:
    # observe current states of all agents
    all_agents_current_states = all_agents_states_t
    # action selection for every agent
    all_agents_current_actions = get_al_agents_actions_by(agents_states=all_agents_current_states,
                                                          agents_list=intersection_agents)
    # take action in
    execute_actions_in_environment(environment=traffic_environment,
                                   actions_list=all_agents_current_actions,
                                   agents_list=intersection_agents)
    # simulation step
    step += 1
    traffic_environment.simulation_step()
    # get rewards
    all_agents_current_rewards = get_all_agents_rewards_by(environment=traffic_environment,
                                                           agents_list=intersection_agents)
    # get new states
    all_agents_new_states = get_all_agents_states_by(environment=traffic_environment,
                                                     agents_list=intersection_agents)
    all_agents_states_t = all_agents_new_states
    # update q_table
    update_q_tables(pre_states=all_agents_current_states,
                    actions=all_agents_current_actions,
                    post_states=all_agents_new_states,
                    rewards=all_agents_current_rewards,
                    agents_list=intersection_agents)
