def get_all_agents_states_by(environment, agents_list):
    """读取所有Agent的状态"""
    all_agents_current_states = {}
    for name, agent in agents_list.items():
        state_config = agent.get_state_config()
        state_val = ()
        for state_name in state_config['names']:
            state_val_t = environment.retrieve_state_by(state_type=state_config['types'][state_name],
                                                        paras=state_config['retrieve_para'][state_name])
            state_val = state_val + (state_val_t,)
        all_agents_current_states[name] = state_val
    return all_agents_current_states
