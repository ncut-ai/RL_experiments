def get_all_agents_rewards_by(environment, agents_list):
    """从环境中获取奖励"""
    all_agents_rewards = {}
    for agent_id, agent in agents_list.items():
        reward_config = agent.get_reward_config()
        reward_val = {}
        reward_compute_type = reward_config['compute_type']
        if reward_compute_type == 'single':  # 单一返回值
            for reward_name in reward_config['names']:
                reward_val_t = environment.retrieve_reward_by(reward_type=reward_config['types'][reward_name],
                                                              paras=reward_config['retrieve_para'][reward_name])
                reward_val[reward_name] = reward_val_t
            all_agents_rewards[agent_id] = reward_val
        elif reward_compute_type == 'single_qualitative':  # 定性评价，等级划分
            pass
        elif reward_compute_type == 'weighted':
            pass
        elif reward_compute_type == 'compound':
            pass
        else:
            raise ValueError('reward type ERROR')

    return all_agents_rewards
