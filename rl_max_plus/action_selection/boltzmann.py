import numpy as np


def boltzmann(**kwargs):
    """Boltzmann or Softmax equation"""
    state = kwargs['state']
    q_table = kwargs['q_table']
    temperature = kwargs['temperature']
    #
    q_state_action = q_table.loc[state, :]  # loc是获取一列的值:取q_table的observation行，所有列
    e_q_state_action = np.exp(q_state_action / temperature)  #
    e_q_state_action_sum = np.sum(e_q_state_action)
    #
    probability_actions = np.true_divide(e_q_state_action, e_q_state_action_sum)
    #
    action_selected = np.random.choice(
        q_state_action[(q_state_action == np.random.choice(q_state_action, p=probability_actions))].index)
    return action_selected
