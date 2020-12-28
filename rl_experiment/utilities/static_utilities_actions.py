def get_all_agents_actions_by(agents_states, agents_list):
    """获取指定状态下agents选择的动作"""
    all_agent_selected_actions = {}
    for name, agent in agents_list.items():
        action_selection_model = agent.get_action_selection_model()  # 获得该Agent的动作类型
        #
        if action_selection_model == 'eps-greedy':
            action = agent.select_action_eps_greedy(state=agents_states[name])  # 参数：状态
        #
        elif action_selection_model == 'UCB':  #
            action = agent.select_action_ucb(state=agents_states[name])
        #
        elif action_selection_model == 'Boltzmann': # Softmax方法
            action = agent.select_action_boltzmann(state=agents_states[name])
        else:
            raise Exception('there is no such a selection model')
        #
        all_agent_selected_actions[name] = action

    return all_agent_selected_actions  # 返回


def execute_actions_in_environment(environment, actions_list, agents_list):
    """在环境中执行动作"""
    for agent_id, action_name in actions_list.items():
        environment.execute_action_by(cross_id=agent_id, action=action_name,
                                      action_config=agents_list[agent_id].get_action_config())
