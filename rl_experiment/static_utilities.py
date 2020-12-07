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
    agent_settings = yaml_data['agent_settings']  # 路口Agents初始化参数

    return env_settings, net_game_settings, agent_settings


def initialize_agents_by(agent_settings):
    """Initialize all intersection agents according to agent settings"""
    intersection_agents = {}
    for key, val in agent_settings.items():
        intersection_agents[key] = IntersectionAgent(agent_setting=val)
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


def get_all_agents_learning_type(agents_list):
    """get all agents' learning model type"""
    all_agents_learning_type = {}
    for name, agent in agents_list.items():
        all_agents_learning_type[name] = agent.get_learning_model_type()
    return all_agents_learning_type


def get_agent_neighbors_q_values(neighbors_names, q_values):
    """获得agent的所有邻居的Q值"""
    neighbors_q_values = []
    for neighbor in neighbors_names:
        neighbors_q_values.append(q_values[neighbor])
    return neighbors_q_values


def get_all_agents_q_by(pre_states, actions, agents_list):
    """ 依据state和action得到每个Agent的Q值"""
    all_agents_q = {}
    for name, agent in agents_list.items():
        all_agents_q[name] = agent.get_q_value_by(state=pre_states[name], action=actions[name])
    return all_agents_q


def clear_all_variables(*args):
    """清空所有变量"""
    for arg in args:
        arg.clear()


def get_all_agents_actions_by(agents_states, agents_list):
    """获取指定状态下agents选择的动作"""
    all_agent_selected_actions = {}
    for name, agent in agents_list.items():
        action_selection_model = agent.get_action_selection_model() #获得该Agent的动作类型
        if action_selection_model == 'eps-greedy':
            action = agent.select_action_eps_greedy(agents_states[name]) #参数：状态
        elif action_selection_model == 'UCB':  # to be
            action = agent.select_action_ucb(agents_states[name])
        else:
            raise Exception('there is no such a selection model')
        all_agent_selected_actions[name] = action
    return all_agent_selected_actions


def update_q_tables(**kwargs):
    """更新Q表"""
    # 获取参数
    learning_types = kwargs['learning_types']
    agents_list = kwargs['agents_list']
    # 获取others参数
    pre_states = kwargs['pre_states']
    actions = kwargs['actions']
    post_states = kwargs['post_states']
    rewards = kwargs['rewards']
    q_values = kwargs['q_values']

    #
    for name_id, agent in agents_list.items():
        learning_model_type = learning_types[name_id]  # 获取当前Agent的学习类型，针对不同的学习类型，获得不同的参数

        if learning_model_type == 'QL':  # q_learning local only
            #
            agent.update_q_table_ql_single(pre_state=pre_states[name_id],
                                           action=actions[name_id],
                                           post_state=post_states[name_id],
                                           reward=rewards[name_id])
        elif learning_model_type == 'QL_with_neighbors':
            # 获得邻居q值
            neighbors_q_values = get_agent_neighbors_q_values(neighbors_names=agent.neighbors, q_values=q_values)
            # 更新Q值
            agent.update_q_table_ql_with_neighbors(pre_state=pre_states[name_id],
                                                   action=actions[name_id],
                                                   post_state=post_states[name_id],
                                                   reward=rewards[name_id],
                                                   neighbors_q=neighbors_q_values)
        elif learning_model_type == 'QL_NetGame':
            pass
        elif learning_model_type == 'SARSA':
            pass
        else:
            raise ValueError('No such a Learning Model')
