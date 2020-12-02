import yaml

"""
0
"""
constant_file = open("constant.yaml", 'r')
constant_content = (yaml.load(constant_file, Loader=yaml.FullLoader))
STEP = constant_content['step']
PRESTEP = constant_content['prestep']
NUMCROSS = constant_content['numcross']
NUMSTATE = constant_content['numstate']
NUMACTION = constant_content['numaction']


"""
1
"""
SUMO_file = open("SUMO.yaml", 'r')
SUMO_CONTENT = yaml.load(SUMO_file, Loader=yaml.FullLoader)
adress = SUMO_CONTENT['adress']
all_edge_list = SUMO_CONTENT['all_edge_list']
id_list = SUMO_CONTENT['id_list']
all_neighbor_list = SUMO_CONTENT['all_neighbor_list']
all_neighber_number_list = SUMO_CONTENT['all_neighber_number_list']


"""
2
"""
agent_file = open("agent.yaml", 'rb')
agent_content = yaml.load(agent_file, Loader=yaml.FullLoader)
state_list = []
for i in range(1):
    state_list.append(agent_content['state'][0])
for j in state_list:
    state_function_list = list(j)
    npos = state_function_list.index(')')
    state_function_list.insert(npos, 'i')
    str_state_function = "".join(state_function_list)     #获得函数方法的写法，自变量为Agent中所示的循环中的i，代表一条边的id，使用时前面加上eval

action_list = []
for i in range(1):
    action_list.append(agent_content['action'][0])
for j in action_list:
    action_function_list = list(j)
    npos = action_function_list.index(')')
    action_function_list.insert(npos, 'self.cross_id, action')    #需要按action的改动修改变量action，应该是一个改变相位的时间
    str_action_function = "".join(action_function_list)


"""
3
"""
qtable_file = open("qtable.yaml", 'rb')
qtable_content = yaml.load(qtable_file, Loader=yaml.FullLoader)
qtableparameter = qtable_content['r_learning']['qtableparameter']
ALPHA = qtableparameter[0]
GAMMA = qtableparameter[1]
EPSILON = qtableparameter[2]


"""
4
"""
boyi_file = open("boyi.yaml", 'rb')
boyi_content = yaml.load(boyi_file, Loader=yaml.FullLoader)
Agent_id_list = boyi_content['game']['agent_id_list']
node_list = boyi_content['game']['agent_id_list']         #这个地方有疑问，明天问师姐
edge_list = boyi_content['game']['agent_edge_list']
Amat = boyi_content['game']['Amat']


#
# def read_yaml():
#     """ A function to read YAML file"""
#     with open('agent.yaml', 'rb') as f:
#         config = list(yaml.safe_load_all(f))
#
#     return config


# f=open("agent.yaml","r")
# a=yaml.load(f,Loader=yaml.FullLoader)
# eval(a["action"][1])
#
# def input(size):
#     state=[]
#     for i in range(size):
#         state.append(a["action"][i])
#

# str_1='wo shi yi zhi da da niu/n'
# str_list=list(str_1)
# nPos=str_list.index('/')
# str_list.insert(nPos,',')
# str_2="".join(str_list)
# print(str_2)
