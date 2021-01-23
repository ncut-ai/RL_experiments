import numpy as np


def upper_confidence_bounds(state, q_table, state_action_count_table):
    """UCB算法实现"""
    q_state_action = q_table.loc[state, :]  # loc是获取一列的值:取q_table的observation行，所有列
    state_action_count = state_action_count_table.loc[state, :]  # 对应的计数表的state行，所有列
    # 根据公式进行计算
    equation_2nd_part = np.sqrt(np.log(np.sum(state_action_count)) / state_action_count)
    equation_final_result = equation_2nd_part - q_state_action
    #
    action_selected = np.random.choice(equation_final_result[equation_final_result == np.max(equation_final_result)].index)  # np.max（）：取行方向的最大值
    return action_selected
