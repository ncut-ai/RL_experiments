def q_learning_local_only(**kwargs):
    """
    Q_Learning algorithm using neighbors' q value
    """
    alpha = kwargs['alpha']
    gamma = kwargs['gamma']
    reward = kwargs['reward']
    pre_q = kwargs['pre_q']
    q_max_for_post_state = kwargs['q_max_for_post_state']

    q_new = pre_q * (1 - alpha) + alpha * (reward + gamma * (q_max_for_post_state))

    return q_new