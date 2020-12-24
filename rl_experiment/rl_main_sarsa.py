"""
SARSA算法流程：
    #获取当前状态
    #agent返回动作
    #执行仿真
    #获取新的状态
    #agent选择动作
    #获取奖励
    #计算Q值
"""
import time

from static_utilities import *
from static_utilities_actions import *
from static_utilities_q import *
from static_utilities_rewards import *
from static_utilities_states import *
from static_utilities_updata_q_sarsa import *
from traffic_environment import TrafficEnvironment

'''
    初始化
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
# get current selected actions
all_agents_current_actions_t = get_all_agents_actions_by(agents_states=all_agents_states_t,
                                                         agents_list=intersection_agents)
while step <= env_setting['simulation_time']:
    time_start = time.time()  # 计时
    # observe current states of all agents
    all_agents_current_states = all_agents_states_t
    # action selection for every agent
    all_agents_current_actions = all_agents_current_actions_t
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
    # get new selected actions
    all_agents_new_actions = get_all_agents_actions_by(agents_states=all_agents_new_states,
                                                       agents_list=intersection_agents)
    # update q_table
    update_q_tables_sarsa(prev_states=all_agents_current_states,
                          prev_actions=all_agents_current_actions,
                          next_states=all_agents_new_states,
                          next_actions=all_agents_new_actions,
                          rewards=all_agents_current_rewards,
                          agents_list=intersection_agents)
    # 计时结束
    time_end = time.time()
    print('time cost: ', time_end - time_start, 's')
    # 选择数据（用于存储）
    # retrieve all agents' q
    all_agents_q_with_current_state = get_all_agents_q_by(pre_states=all_agents_new_states,
                                                          actions=all_agents_new_actions,
                                                          agents_list=intersection_agents)
    data_collection(step, runtime_data,
                    states=all_agents_current_states,
                    actions=all_agents_current_actions,
                    rewards=all_agents_current_rewards,
                    q_vals=all_agents_q_with_current_state)
    #
    # 预备下一次循环
    #
    all_agents_states_t = all_agents_new_states
    all_agents_current_actions_t = all_agents_new_actions
    # 清空变量
    # clear_all_variables(all_agents_new_states,
    #                     all_agents_current_states,
    #                     all_agents_current_actions,
    #                     all_agents_current_rewards,
    #                     all_agents_q_with_current_state.clear())

# 存储数据到文件
save_data_h5py('to_pickle', data=runtime_data, file_path=env_setting['data_save_filepath'])
