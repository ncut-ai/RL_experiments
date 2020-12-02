########################################################################################################################
# static_utilities.py
# 12/2/2020, created by
# We use lots of utilities independent from other modulers in this experiment, like reading essential config information
# for initialization, some miscellanceous tasks, etc.
#
#
########################################################################################################################
import yaml
from intersection_agent import IntersectionAgent
from traffic_environment import TrafficEnvironment

########################################################################################################################
# Read essential config and setting information from a yaml file
########################################################################################################################
def read_yaml(yaml_file):
    """to read a yaml file"""
    with open(yaml_file,'rb') as f:
        all_data = list(yaml.safe_load_all(f))
    return all_data
def get_settings_from_yaml(yaml_file):
    yaml_data = read_yaml(yaml_file)[0]
    env_settings = yaml_data['environment_settings'] # 仿真环境配置参数
    net_game_settings = yaml_data['net_game_settings'] # 网络博弈模型参数
    rl_settings = yaml_data['rl_settings'] # 强化学习模型参数
    agent_settings = yaml_data['agent_settings'] # 路口Agents初始化参数

    return env_settings, net_game_settings, rl_settings, agent_settings
########################################################################################################################
# Initialize all intersection agents according to agent settings
########################################################################################################################
def initialize_agents_by(agent_settings,rl_setting):
    intersection_agents = {}
    for key, val in agent_settings.items():
        intersection_agents[key] = IntersectionAgent(agent_setting=val,rl_setting=rl_setting)
    return intersection_agents

########################################################################################################################
# 读取所有Agent的状态
########################################################################################################################
def get_all_agents_states_by(environment, agents_list):
    all_agents_current_states = {}
    for name, agent in agents_list.items():
        agent_config = agent.get_state_config()
        state_val = ()
        for state_name in agent_config['names']:
            state_val_t = environment.retrieve_state_by(state_type=agent_config['types'][state_name],
                                                  paras=agent_config['retrieve_para'][state_name])
            state_val = state_val + (state_val_t,)
        all_agents_current_states[name] = state_val
    return all_agents_current_states
########################################################################################################################
# 获取指定状态下agents选择的动作
########################################################################################################################
def get_al_agents_actions_by(agents_states,agents_list):
    all_agent_selected_actions = {}
    for name,agent in agents_list.items():
        action = agent.select_action(agents_states[name])
        all_agent_selected_actions[name] = action
    return all_agent_selected_actions
########################################################################################################################
# 在环境中执行动作
########################################################################################################################
def execute_actions_in_environment(environment, actions_list, agents_list):
    for agent_id, action_name in actions_list.items():
        environment.execute_action_by(cross_id=agent_id,action=action_name,action_config=agents_list[agent_id].get_action_config())