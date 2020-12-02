########################################################################################################################
#
#
#
#
#
#
########################################################################################################################
import yaml
from intersection_agent import IntersectionAgent

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