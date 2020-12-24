"""
Q-Learning算法流程：
    #获取当前状态
    #agent返回动作
    #执行仿真
    #获取奖励
    #更新Q表
"""
import time

from static_utilities import *
from static_utilities_states import *
from static_utilities_actions import *
from static_utilities_rewards import *
from static_utilities_q import *
from static_utilities_update_q_ql import *

from traffic_environment import TrafficEnvironment

'''
# Initialization
# 1. read config info from file
# 2. initialize the traffic simulation environment and all agents with info about reinforcement learning
# 3. initialize the network game model (to be)
'''
# 1.
env_setting, net_game_setting, agent_settings, runtime_data = get_settings_from_yaml(
    yaml_file='_config_multi_rewards_test_and_UCB.yaml')  # to read settings info
# 2.
traffic_environment = TrafficEnvironment(env_setting=env_setting)  # traffic environment
intersection_agents = initialize_agents_by(
    agent_settings=agent_settings)  # all agents:in a dict: [key is an agent's name] : [val is the Agent object from IntersectionAgent Class]
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
    all_agents_q_with_current_state = get_all_agents_q_by(pre_states=all_agents_current_states,
                                                          actions=all_agents_current_actions,
                                                          agents_list=intersection_agents)
    # retrieve all agents' learning model type
    all_agents_learning_type = get_all_agents_learning_type(agents_list=intersection_agents)
    # update q_table
    update_q_tables(pre_states=all_agents_current_states,
                    actions=all_agents_current_actions,
                    post_states=all_agents_new_states,
                    rewards=all_agents_current_rewards,
                    q_values=all_agents_q_with_current_state,
                    learning_types=all_agents_learning_type,
                    agents_list=intersection_agents)
    time_end = time.time()  # 计时结束
    print('time cost: ', time_end - time_start, 's')
    # 选择数据（用于存储）
    data_collection(step, runtime_data,
                    states=all_agents_current_states,
                    actions=all_agents_current_actions,
                    rewards=all_agents_current_rewards,
                    q_vals=all_agents_q_with_current_state)
    # 清空变量
    # clear_all_variables(all_agents_new_states,
    #                     all_agents_current_states,
    #                     all_agents_current_actions,
    #                     all_agents_current_rewards,
    #                     all_agents_q_with_current_state.clear())

# 存储数据到文件
save_data_h5py('to_pickle', data=runtime_data, file_path=env_setting['data_save_filepath'])
