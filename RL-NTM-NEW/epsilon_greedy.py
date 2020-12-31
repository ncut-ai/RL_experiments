import numpy as np


# def epsilon_greedy(epsilon, state, q_table, all_actions):
#     """epsilon greedy"""
#     state_action = q_table.loc[state, :]
#     if np.random.uniform() < epsilon:  # 选择Q_value 最高的action
#         # choose best action
#           # loc是获取一列的值:取q_table的observation行，所有列
#         # some actions may have the same value, randomly choose on in these actions
#
#         action = np.random.choice(all_actions)
#
#         # action = np.random.choice(state_action[state_action == np.max(state_action)].index)  # np.max（）：取行方向的最大值
#         # print(action)
#     else:
#         # choose random action
#         action = np.random.choice(all_actions)
#
#         # print(action)
#
#
#
#     return action

def epsilon_greedy(epsilon, state, q_table, all_actions):
    """epsilon greedy"""
    if np.random.uniform() < epsilon:  # 选择Q_value 最高的action
        # choose best action
        state_action = q_table.loc[state, :]  # loc是获取一列的值:取q_table的observation行，所有列
        # some actions may have the same value, randomly choose on in these actions
        action = np.random.choice(state_action[state_action == np.max(state_action)].index)  # np.max（）：取行方向的最大值
        if isinstance(action,int):
            print('action没有正确进行结果输出，原因：Q表中存在重复项，即index出现了相同值，导致state_action为2*3')
    else:
        # choose random action
        action = np.random.choice(all_actions)
    return action

