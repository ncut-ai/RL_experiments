import yaml

# yaml_file = open("items.yaml", 'r')
# yaml_content = yaml.load(yaml_file, Loader=yaml.FullLoader)


# qtable_file = open("qtable.yaml", 'r')
# qtable_content = yaml.load(qtable_file, Loader=yaml.FullLoader)
# qtableparameter = qtable_content['r_learning']['qtableparameter']
# ALPHA = qtableparameter[0]
# GAMMA = qtableparameter[1]
# EPSILON = qtableparameter[2]
# print(ALPHA,GAMMA,EPSILON)


# with open('agent.yaml', 'r') as f:
#     config = list(yaml.safe_load_all(f))
# my_config = config
# my_quiz = my_config[0]

# agent_file = open("agent.yaml", 'rb')
# agent_content = yaml.load(agent_file, Loader=yaml.FullLoader)

# agent_file = open("agent.yaml", 'r')
# agent_content = yaml.load(agent_file, Loader=yaml.FullLoader)
# state_list = []
# state_list.append(agent_content['state']['0'])
# state_function_list = list(0)
# npos = state_function_list.index(')')
# state_function_list.insert(npos, 'i')
# str_state_function = "".join(state_function_list)     #获得函数方法的写法，自变量为Agent中所示的循环中的i，代表一条边的id，使用时前面加上eval
#
# action_list = []
# for i in range(1):
#     action_list.append(agent_content['action']['0'])
# for j in action_list:
#     action_function_list = list(0)
#     npos = action_function_list.index(')')
#     action_function_list.insert(npos, 'self.cross_id, action')    #需要按action的改动修改变量action，应该是一个改变相位的时间
#     str_action_function = "".join(action_function_list)

SUMO_file = open("SUMO.yaml", 'rb')
SUMO_CONTENT = yaml.load(SUMO_file, Loader=yaml.FullLoader)
adress = SUMO_CONTENT['adress']
all_edge_list = SUMO_CONTENT['all_edge_list']
id_list = SUMO_CONTENT['id_list']
all_neighbor_list = SUMO_CONTENT['all_neighbor_list']
all_neighber_number_list = SUMO_CONTENT['all_neighber_number_list']


