"""
 static_utilities.py
 12/2/2020, created by
 We use lots of utilities independent from other modulers in this experiment, like reading essential config information
 for initialization, some miscellanceous tasks, etc.

"""

import pickle

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
    rl_setting = yaml_data['rl_settings']

    runtime_data = {}  # 用于存储运行过程中的数据

    return env_settings, net_game_settings, agent_settings, rl_setting, runtime_data


def initialize_agents_by(agent_settings, rl_setting):
    """Initialize all intersection agents according to agent settings"""
    intersection_agents = {}
    for key, val in agent_settings.items():
        intersection_agents[key] = IntersectionAgent(agent_setting=val, rl_setting=rl_setting)
    return intersection_agents


def clear_all_variables(*args):
    """清空所有变量"""
    for arg in args:
        arg.clear()


def data_collection(*args, **kwargs):  # 未完成
    """用于运行数据存储"""
    args[1][args[0]] = {}  # 嵌套词典存储
    args[1][args[0]]['states'] = kwargs['states']
    args[1][args[0]]['actions'] = kwargs['actions']
    args[1][args[0]]['rewards'] = kwargs['rewards']
    args[1][args[0]]['q_vals'] = kwargs['q_vals']


def save_data_pickle(*args, **kwargs):
    """保存数据到文件"""
    print(args[0])
    file_name = kwargs['file_path']
    data = kwargs['data']
    hf_object = open(file_name, 'wb')
    pickle.dump(data, hf_object)
    hf_object.close()
