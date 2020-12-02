import traci
import copy
from functions import net_work, inital_agent_qtable, take_state_action_zx, get_nbr_q_i_reward, do_one_action, append_in_the_list, save_csv
import Constant
import readyaml


"""#获取复杂网络"""
the_NET = net_work(readyaml.node_list, readyaml.edge_list)
"""#初始化包含每个路口的Agent和Qtable列表，以及Real_Q_table列表和Node_States列表"""
Real_Q_table_list, Node_States_list, get_cross_information_list, Net_Q_table_list = inital_agent_qtable(the_NET)
all_Real_Q_table_list = Constant.all_Real_Q_table_list


# 仿真模型
sumoCmd = readyaml.adress
"""--------------------------初始化仿真 traci -----------------------------"""

traci.start(sumoCmd)
step = readyaml.STEP  # 设置步长计数
"""------------------------------  开始进行仿真  ------------------------------------------"""
# Run a simulation until all vehicles have arrived
for step in range(readyaml.PRESTEP):
    traci.simulationStep()


while step < 900:
    newNStates = copy.deepcopy(Node_States_list)
    state_list_t, agent_action_chosen_list_t, zx_list_t = [], [], []
    w = 0
    for i in the_NET.nodes():
        """ 真实路网的state：排队长度;博弈节点根据强化学习选动作;计算节点i的动作对应的向量"""
        if w < 6:
            state, agent_action_chosen, zx = take_state_action_zx(i, newNStates, get_cross_information_list, Real_Q_table_list)
            append_in_the_list(state_list_t, agent_action_chosen_list_t, zx_list_t, state, agent_action_chosen, zx)
            w += 1
        else:
            break
    step += 1
    """进行一步仿真"""
    traci.simulationStep()
    v = 0
    for i in the_NET.nodes():
        """获得邻居的Q值并计算在这一节点i的奖励值"""
        if v < 6:
            nbr_Q_list = Constant.nbr_Q_list
            reward = 0
            for j in the_NET.adj[i]:
                input_reward = reward
                input_nbr_Q_list = nbr_Q_list
                nbr_Q_list, reward = get_nbr_q_i_reward(Net_Q_table_list, get_cross_information_list, Real_Q_table_list, zx_list_t[i], newNStates, j, input_reward, input_nbr_Q_list)
            """路口根据强化学习做出选择的动作"""
            cross_action_chosen = do_one_action(Real_Q_table_list, agent_action_chosen_list_t[i], get_cross_information_list, i)
            """进行一步仿真后计算排队长度、奖励值，然后更新Q表"""
            next_step_state = get_cross_information_list[i].get_current_state()
            next_step_reward = get_cross_information_list[i].caculate_reward()
            q_rl = Real_Q_table_list[i].update_qtable(state_list_t[i], cross_action_chosen, next_step_reward, next_step_state, nbr_Q_list, readyaml.ALPHA, readyaml.GAMMA)
            """计算博弈节点下一步的状态"""
            Node_States_list[i] = agent_action_chosen_list_t[i]
            """更新博弈q表"""
            q_ng = Net_Q_table_list[i].update_qtable(newNStates[i], agent_action_chosen_list_t[i], reward, Node_States_list[i], nbr_Q_list, readyaml.ALPHA, readyaml.GAMMA)
            all_Real_Q_table_list[i].append([state_list_t[i], agent_action_chosen_list_t[i], next_step_reward, q_rl, q_ng])
            v += 1
        else:
            break

traci.close()

save_csv(readyaml.NUMCROSS, all_Real_Q_table_list)


