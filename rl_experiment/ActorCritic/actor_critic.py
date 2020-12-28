def actor_critic(**kwargs):
    """Actor-Critic 算法的Q值更新公式"""
    #
    prev_q = kwargs['prev_q']
    prev_q_max = kwargs['prev_q_max']
    next_q_max = kwargs['next_q_max']
    reward = kwargs['reward']
    alpha = kwargs['alpha']

    #
    q_new = prev_q + alpha * (reward + next_q_max - prev_q_max)
    #
    return q_new