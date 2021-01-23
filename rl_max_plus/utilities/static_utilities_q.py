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

