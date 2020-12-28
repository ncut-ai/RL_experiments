def update_q_tables_actor_critic(**kwargs):
    """根据SARSA算法计算Q值，更新Q表"""
    prev_states = kwargs['prev_states']
    prev_actions = kwargs['prev_actions']
    next_states = kwargs['next_states']
    rewards = kwargs['rewards']
    agents_list = kwargs['agents_list']

    #
    for name_id, agent in agents_list.items():
        agent.update_q_table_actor_critic(prev_state=prev_states[name_id],
                                          prev_action=prev_actions[name_id],
                                          next_state=next_states[name_id],
                                          reward=rewards[name_id])
