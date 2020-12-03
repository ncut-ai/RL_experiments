"""
 static_utilities.py
 12/2/2020, created by
 We use lots of utilities independent from other modulers in this experiment, like reading essential config information
 for initialization, some miscellanceous tasks, etc.

"""

import yaml
from intersection_agent import IntersectionAgent


def read_yaml(yaml_file):
    """to read a yaml file"""
    with open(yaml_file, 'rb') as f:
        all_data = list(yaml.safe_load_all(f))
    return all_data


def get_settings_from_yaml(yaml_file):
    """Read config information from yaml file"""
    yaml_data = read_yaml(yaml_file)[0]
    env_settings = yaml_data['environment_settings']  # 仿真环境配置参数
    net_game_settings = yaml_data['net_game_settings']  # 网络博弈模型参数
    rl_settings = yaml_data['rl_settings']  # 强化学习模型参数
    agent_settings = yaml_data['agent_settings']  # 路口Agents初始化参数

    return env_settings, net_game_settings, rl_settings, agent_settings


def initialize_agents_by(agent_settings, rl_setting):
    """Initialize all intersection agents according to agent settings"""
    intersection_agents = {}
    for key, val in agent_settings.items():
        intersection_agents[key] = IntersectionAgent(agent_setting=val, rl_setting=rl_setting)
    return intersection_agents


def get_all_agents_states_by(environment, agents_list):
    """读取所有Agent的状态"""
    all_agents_current_states = {}
    for name, agent in agents_list.items():
        state_config = agent.get_state_config()
        state_val = ()
        for state_name in state_config['names']:
            state_val_t = environment.retrieve_state_by(state_type=state_config['types'][state_name],
                                                        paras=state_config['retrieve_para'][state_name])
            state_val = state_val + (state_val_t,)
        all_agents_current_states[name] = state_val
    return all_agents_current_states


def get_al_agents_actions_by(agents_states, agents_list):
    """获取指定状态下agents选择的动作"""
    all_agent_selected_actions = {}
    for name, agent in agents_list.items():
        action = agent.select_action(agents_states[name])
        all_agent_selected_actions[name] = action
    return all_agent_selected_actions


def execute_actions_in_environment(environment, actions_list, agents_list):
    """在环境中执行动作"""
    for agent_id, action_name in actions_list.items():
        environment.execute_action_by(cross_id=agent_id, action=action_name,
                                      action_config=agents_list[agent_id].get_action_config())


def get_all_agents_rewards_by(environment, agents_list):
    """从环境中获取奖励"""
    all_agents_rewards = {}
    for agent_id, agent in agents_list.items():
        reward_config = agent.get_reward_config()
        reward_val = {}
        for reward_name in reward_config['names']:
            reward_val_t = environment.retrieve_reward_by(reward_type=reward_config['types'][reward_name],
                                                          paras=reward_config['retrieve_para'][reward_name])
            reward_val[reward_name] = reward_val_t
        all_agents_rewards[agent_id] = reward_val
    return all_agents_rewards

def update_q_tables(pre_states, actions, post_states, rewards, agents_list):
    """更新Q表"""
    for name_id, agent in agents_list.items():
        neighbors_q_values = get_agent_neighbors_q_values(agent_name=name_id,
                                                          pre_states=pre_states,
                                                          actions=actions,
                                                          agents_list=agents_list)
        agent.update_q_table(pre_state=pre_states[name_id],
                             action=actions[name_id],
                             post_state=post_states[name_id],
                             reward=rewards[name_id],
                             neighbors_q=neighbors_q_values)

def get_agent_neighbors_q_values(agent_name,pre_states,actions,agents_list):
    """获得agent_name的所有邻居的Q值"""
    neighbors_q_values = []
    agent = agents_list[agent_name]
    for neighbor in agent.neighbors:
        neighbor_agent = agents_list[neighbor]
        neighbor_state = pre_states[neighbor]
        neighbor_action = actions[neighbor]
        neighbors_q_values.append(neighbor_agent.get_q_value_by(neighbor_state,neighbor_action))
    return neighbors_q_values