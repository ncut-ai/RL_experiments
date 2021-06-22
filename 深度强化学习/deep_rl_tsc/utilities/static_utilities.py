import yaml



def read_yaml(yaml_file):
    """to read a yaml file"""
    with open(yaml_file, 'rb') as f:
        all_data = list(yaml.safe_load_all(f))
    return all_data


def get_settings_from_yaml(yaml_file):
    """Read config information from yaml file"""
    yaml_data = read_yaml(yaml_file)[0]
    env_settings = yaml_data['env_settings']  # 仿真环境配置参数
    dqn_settings = yaml_data['dqn_settings']  # 网络博弈模型参数

    return env_settings, dqn_settings