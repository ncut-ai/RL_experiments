import yaml
from new_agent import Agent

def read_yaml(yaml_file):
    with open(yaml_file, 'rb') as f:
        all_data = list(yaml.safe_load_all(f))
    return all_data

def get_settings_from_yaml(yaml_file):
    yaml_data = read_yaml(yaml_file)[0]
    env_settings = yaml_data['ntm_setting']  # 仿真环境配置参数
    agent_settings = yaml_data['agent_settings']  # 路口Agents初始化参数

    return env_settings, agent_settings

def initialize_agents_by(agent_settings):
    zone_agents = {}
    for key, val in agent_settings.items():
        zone_agents[key] = Agent(agent_setting=val)
    return zone_agents

def get_all_agents_states_by(environment, agents_list):
    """读取所有Agent的状态"""
    for name, agent in agents_list.items():
        environment.get_selected_zone_flow(id=agent.id, zone_paras=agent.parameters)
    return environment.current_transmit_flow

def get_all_agents_2_neighbors_transmit_flow_by(environment, agents_list):
    for name, agent in agents_list.items():
        environment.get_actions_zone_2_neighbors_flow(id=agent.id, zone_paras=agent.parameters)
    return environment.neighbors_current_transmit_flow, environment.after_actions_accumulated_vehicles

def get_all_agents_actions_by(agents_states, agents_list):
    all_agents_selected_actions = {}
    for name, agent in agents_list.items():
        action_selection_model = agent.get_action_selection_model()
        if action_selection_model == 'eps-greedy':
            action = agent.select_action_eps_greedy(agents_states[name])
        else:
            raise Exception('there is no such a selection model')
        all_agents_selected_actions[name] = action
    return all_agents_selected_actions

def execute_actions_in_environment(environment, actions_list, agents_list):
    """在环境中执行动作"""
    for agent_id, actions_name in actions_list.items():
        # print(agent_id, actions_name)
        for neighbor_id, action_name in actions_name.items():
            #print(agent_id, neighbor_id, action_name)
            environment.get_zone_2_neighbors_transmit_flow_by(agent_id=agent_id, neighbor_id =neighbor_id)
            environment.execute_action_by(id=neighbor_id,
                                          action=action_name,
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










