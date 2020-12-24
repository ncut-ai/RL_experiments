def get_all_agents_learning_type(agents_list):
    """get all agents' learning model type"""
    all_agents_learning_type = {}
    for name, agent in agents_list.items():
        all_agents_learning_type[name] = agent.get_learning_model_type()
    return all_agents_learning_type


def get_agent_neighbors_q_values(neighbors_names, q_values):
    """获得agent的所有邻居的Q值"""
    neighbors_q_values = []
    for neighbor in neighbors_names:
        neighbors_q_values.append(q_values[neighbor])
    return neighbors_q_values


def get_all_agents_q_by(pre_states, actions, agents_list):
    """ 依据state和action得到每个Agent的Q值"""
    all_agents_q = {}
    for name, agent in agents_list.items():
        all_agents_q[name] = agent.get_q_value_by(state=pre_states[name], action=actions[name])
    return all_agents_q


def update_q_tables(**kwargs):
    """更新Q表"""
    # 获取参数
    learning_types = kwargs['learning_types']
    agents_list = kwargs['agents_list']
    # 获取others参数
    pre_states = kwargs['pre_states']
    actions = kwargs['actions']
    post_states = kwargs['post_states']
    rewards = kwargs['rewards']
    q_values = kwargs['q_values']

    #
    for name_id, agent in agents_list.items():
        learning_model_type = learning_types[name_id]  # 获取当前Agent的学习类型，针对不同的学习类型，获得不同的参数

        if learning_model_type == 'QL':  # q_learning local only
            #
            agent.update_q_table_ql_single(pre_state=pre_states[name_id],
                                           action=actions[name_id],
                                           post_state=post_states[name_id],
                                           reward=rewards[name_id])
        elif learning_model_type == 'QL_with_neighbors':
            # 获得邻居q值
            neighbors_q_values = get_agent_neighbors_q_values(neighbors_names=agent.neighbors, q_values=q_values)
            # 更新Q值
            agent.update_q_table_ql_with_neighbors(pre_state=pre_states[name_id],
                                                   action=actions[name_id],
                                                   post_state=post_states[name_id],
                                                   reward=rewards[name_id],
                                                   neighbors_q=neighbors_q_values)
        elif learning_model_type == 'QL_NetGame':
            pass
        elif learning_model_type == 'SARSA':
            pass
        else:
            raise ValueError('No such a Learning Model')
