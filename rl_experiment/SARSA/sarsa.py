def sarsa_func(**kwargs):
    """SARSA算法的Q值更新公式"""
    #
    prev_q = kwargs['prev_q']
    next_q = kwargs['next_q']
    reward = kwargs['reward']
    alpha = kwargs['alpha']
    gamma = kwargs['gamma']
    #
    q_new = (1 - alpha) * prev_q + alpha * (reward + gamma * next_q)
    #
    return q_new
