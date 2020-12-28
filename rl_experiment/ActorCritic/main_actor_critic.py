"""
Actor Critic 算法
Li et al. [2009]
"""
import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import time

from utilities.static_utilities import *
from utilities.static_utilities_actions import *
from utilities.static_utilities_q import *
from utilities.static_utilities_rewards import *
from utilities.static_utilities_states import *
from utilities.static_utilities_update_q_actor_critic import *
from traffic_environment import TrafficEnvironment


def main_actor_critic(**kwargs):
    # 获取参数
    yaml_file = kwargs['yaml_file']
    '''
        初始化
    '''
    # 1.# to read settings info
    env_setting, net_game_setting, agent_settings, runtime_data = get_settings_from_yaml(yaml_file=yaml_file)
    # 2.# traffic environment
    traffic_environment = TrafficEnvironment(env_setting=env_setting)
    # all agents:in a dict: [key is an agent's name] : [val is the Agent object from IntersectionAgent Class]
    intersection_agents = initialize_agents_by(agent_settings=agent_settings)
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
        # update q_table
        update_q_tables_actor_critic(prev_states=all_agents_current_states,
                                     prev_actions=all_agents_current_actions,
                                     next_states=all_agents_new_states,
                                     rewards=all_agents_current_rewards,
                                     agents_list=intersection_agents)
        # 计时结束
        time_end = time.time()
        print('time cost: ', time_end - time_start, 's')
        # 选择数据（用于存储）
        # retrieve all agents' q
        all_agents_q_with_current_state = get_all_agents_q_by(pre_states=all_agents_current_states,
                                                              actions=all_agents_current_actions,
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
        # 清空变量
        # clear_all_variables(all_agents_new_states,
        #                     all_agents_current_states,
        #                     all_agents_current_actions,
        #                     all_agents_current_rewards,
        #                     all_agents_q_with_current_state.clear())

    # 存储数据到文件
    save_data_pickle('to_pickle', data=runtime_data, file_path=env_setting['data_save_filepath'])
