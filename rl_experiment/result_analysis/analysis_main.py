import pickle
import numpy as np
import pandas as pd
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

'''
'''

'''
'''


def proc_states(state_data):
    print('处理状态数据')
    # for key, val in state_data.items():
    #     print('路口:', key)


'''
'''


def proc_actions(action_data):
    print('处理动作数据')
    # for key, val in action_data.items():
    #     print('路口:', key)


'''
'''


def proc_rewards(reward_data, df):
    print('处理奖励数据')
    new = pd.DataFrame(columns={"J1": 0, "J2": 0, "J3": 0, "J4": 0, "J5": 0, "J6": 0}, index=[0])
    new.loc[0, 'J1'] = reward_data['J1']
    new.loc[0, 'J2'] = reward_data['J2']
    new.loc[0, 'J3'] = reward_data['J3']
    new.loc[0, 'J4'] = reward_data['J4']
    new.loc[0, 'J5'] = reward_data['J5']
    new.loc[0, 'J6'] = reward_data['J6']
    df = df.append(new, ignore_index=True)  # ignore_index=True,表示不按原来的索引，从0开始自动递增
    return df


'''
'''


def proc_q_vals(q_data, df):
    print('处理Q值数据')
    new = pd.DataFrame(columns={"J1": 0, "J2": 0, "J3": 0, "J4": 0, "J5": 0, "J6": 0}, index=[0])
    new.loc[0, 'J1'] = q_data['J1']
    new.loc[0, 'J2'] = q_data['J2']
    new.loc[0, 'J3'] = q_data['J3']
    new.loc[0, 'J4'] = q_data['J4']
    new.loc[0, 'J5'] = q_data['J5']
    new.loc[0, 'J6'] = q_data['J6']
    df = df.append(new, ignore_index=True)  # ignore_index=True,表示不按原来的索引，从0开始自动递增
    return df


'''
'''
if __name__ == '__main__':
    # 创建奖励变量
    df_reward = pd.DataFrame()
    df_q = pd.DataFrame()
    # # 读取
    with open('test_data.pickle', 'rb') as f:
        data = pickle.load(f)

    '''
    '''
    for key, val in data.items():
        for s_key, s_val in val.items():
            if s_key == 'states':
                proc_states(state_data=s_val)
            elif s_key == 'actions':
                proc_actions(action_data=s_val)
            elif s_key == 'rewards':
                df_reward = proc_rewards(reward_data=s_val, df=df_reward)
            elif s_key == 'q_vals':
                df_q = proc_q_vals(q_data=s_val, df=df_q)
            else:
                raise Exception("Wrong Values")

    f.close()
    '''
    '''
    print(df_reward)

    # Plot the responses for different events and regions
    x = df_reward.index.to_list()
    y = df_reward.loc[:, 'J3'].to_list()

    print(x)
    print(y)

    #two_arrays = np.array(x,y)
    ddd = [x, y]
    print(ddd)

    #fig = px.line(df_reward, title='Life expectancy in Canada')
    #fig = px.scatter(x=x, y=y)
    #fig = px.scatter(df_reward,  y="J4")
    #fig = go.Figure(data=go.Scatter(x=x,  y=y, mode='markers'))
    fig = px.histogram(df_q, x="J2")
    
    fig.show()
