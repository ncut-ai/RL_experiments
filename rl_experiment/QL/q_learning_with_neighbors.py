def q_learning_with_neighbors(**kwargs):
    """
    Q_Learning algorithm using neighbors' q value
    """
    alpha = kwargs['alpha']
    gamma = kwargs['gamma']
    reward = kwargs['reward']
    pre_q = kwargs['pre_q']
    q_max_for_post_state = kwargs['q_max_for_post_state']
    neighbors_q_list = kwargs['neighbors_q']

    neighbors_q_sum = sum(neighbors_q_list)

    q_new = pre_q * (1 - alpha) + alpha * (reward + gamma * (q_max_for_post_state + neighbors_q_sum))

    return q_new
