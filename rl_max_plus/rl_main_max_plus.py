import time

from utilities.static_utilities import *
from utilities.static_utilities_states import *
from utilities.static_utilities_actions import *
from utilities.static_utilities_rewards import *


from traffic_environment import TrafficEnvironment

'''
 Max-plus算法
'''
# 读取配置文件
env_setting, net_game_setting, agent_settings, rl_setting, runtime_data = get_settings_from_yaml(yaml_file='yaml_configs/_config.yaml')  # to read settings info

# 环境初始化
traffic_environment = TrafficEnvironment(env_setting=env_setting)  # traffic environment

# Agents 初始化
intersection_agents = initialize_agents_by(agent_settings=agent_settings, rl_setting=rl_setting)
# 3.


'''begin'''
step = 0  #
traffic_environment.pre_run_simulation_to_prepare(env_setting['pre_steps'])  # pre run simulation with doing nothing
# get current states
all_agents_states_t = get_all_agents_states_by(environment=traffic_environment,
                                               agents_list=intersection_agents)
while step <= env_setting['simulation_time']:
    time_start = time.time()  # 计时
    # observe current states of all agents
    all_agents_current_states = all_agents_states_t
    # action selection for every agent
    all_agents_current_actions = get_all_agents_actions_by(agents_states=all_agents_current_states,
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
    # retrieve all agents' q

    # retrieve all agents' learning model type

    # update q_table

    # 选择数据（用于存储）

    # 清空变量
    # clear_all_variables(all_agents_new_states,
    #                     all_agents_current_states,
    #                     all_agents_current_actions,
    #                     all_agents_current_rewards,
    #                     all_agents_q_with_current_state.clear())

# 存储数据到文件
save_data_pickle('to_pickle', data=runtime_data, file_path=env_setting['data_save_filepath'])
