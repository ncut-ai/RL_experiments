def get_all_agents_rewards_by(environment, agents_list):
    """从环境中获取奖励"""
    all_agents_rewards = {}
    for agent_id, agent in agents_list.items():
        reward_config = agent.get_reward_config()
        reward_compute_type = reward_config['compute_type']
        if reward_compute_type == 'single':  # 单一返回值
            all_agents_rewards[agent_id] = get_reward_single(environment=environment, reward_config=reward_config)
        elif reward_compute_type == 'single_qualitative':  # 定性评价，等级划分
            all_agents_rewards[agent_id] = get_reward_single_qualitative(environment=environment,
                                                                         reward_config=reward_config)
        elif reward_compute_type == 'weighted':
            all_agents_rewards[agent_id] = get_reward_weighted(environment=environment,
                                                               reward_config=reward_config)
        elif reward_compute_type == 'compound':
            all_agents_rewards[agent_id] = get_reward_compound(environment=environment,
                                                               reward_config=reward_config)
        else:
            raise ValueError('reward type ERROR')

    return all_agents_rewards


def get_reward_single(environment, reward_config):
    """single类型的reward值"""
    reward_name = reward_config['names']
    return environment.retrieve_reward_by(reward_type=reward_config['types'][reward_name],
                                          paras=reward_config['retrieve_para'][reward_name])


def get_reward_single_qualitative(environment, reward_config):
    """single类型，返回定性评价值"""
    return -99


def get_reward_weighted(environment, reward_config):
    """weighted类型，返回加权reward值"""
    return -99


def get_reward_compound(environment, reward_config):
    """weighted类型，返回加权reward值"""
    return -99
