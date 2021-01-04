##new_NTM就是environment
import numpy as np
from numpy import random


class NTM:

    def __init__(self, NTM_setting):
        self.model = NTM_setting['model']
        self.canshu = NTM_setting['canshu']
        self.current_transmit_flow = {} #用来记录
        self.zones_2_neighbors_transmit_flow = {}
        self.after_actions_accumulated_vehicles = {}


    # def create_transmit_flow(self, max_flow, expected_flow):
    #     transmit_flow = random.poisson(lam=expected_flow)
    #     if transmit_flow > max_flow:
    #         transmit_flow = max_flow
    #     elif transmit_flow < expected_flow:
    #         transmit_flow = expected_flow
    #     return transmit_flow

    def create_transmit_flow(self):
        transmit_flow = random.randint(0,1000)
        return transmit_flow

    def get_selected_zone_flow(self, id, zone_paras):

        expected_flow = zone_paras['expected_flow']
        max_flow = zone_paras['max_flow']
        neighbors= zone_paras['neighbors']

        zone_2_neighbors_transmit_flow = {}
        for elem in neighbors:
            transmit_flow = self.create_transmit_flow()
            # transmit_flow = self.create_transmit_flow(max_flow, expected_flow)
            # zone_2_neighbors_transmit_flow = zone_2_neighbors_transmit_flow + (transmit_flow,)
            # zone_2_neighbors_transmit_flow.append(transmit_flow)
            zone_2_neighbors_transmit_flow[elem] = transmit_flow

        self.current_transmit_flow[id] = zone_2_neighbors_transmit_flow


    def get_actions_zone_2_neighbors_flow(self, id, zone_paras):
        expected_flow = zone_paras['expected_flow']
        max_flow = zone_paras['max_flow']
        first_flow = zone_paras['first_flow']
        whole_outflow = zone_paras['whole_outflow']
        whole_inflow = zone_paras['whole_inflow']
        neighbors = zone_paras['neighbors']
        accumulated_vehicles = zone_paras['accumulated_vehicles']
        old_accumulated_vehicles = zone_paras['old_accumulated_vehicles']
        critical_accumulated_vehicles = zone_paras['critical_accumulated_vehicles']
        neighbors_accumulated_vehicles = zone_paras['neighbors_accumulated_vehicles']
        neighbors_old_accumulated_vehicles = zone_paras['neighbors_old_accumulated_vehicles']

        zone_2_neighbors_transmit_flow = {}
        after_actions_accumulated_vehicles = []
        for elem, x, y in zip(neighbors ,neighbors_accumulated_vehicles, neighbors_old_accumulated_vehicles):

            if x > y * 0.9 and x < y:
                transmit_factor = 0.1
                zone_2_neighbors_transmit_flow[elem] = transmit_factor * self.create_transmit_flow(max_flow, expected_flow) #生成传输流
                x = y + zone_2_neighbors_transmit_flow[elem] #对于elem(某邻居)，累计车辆数 = 旧的累计车辆数 + 流入
                accumulated_vehicles = old_accumulated_vehicles + self.create_transmit_flow(max_flow, expected_flow)- zone_2_neighbors_transmit_flow[elem]  # 流出小区 ，累计车辆数 = 旧的 +新的- 流出
                old_accumulated_vehicles = accumulated_vehicles
            elif x > y * 0.5 and x < old_accumulated_vehicles * 0.9:
                transmit_factor = 0.5
                zone_2_neighbors_transmit_flow[elem] = transmit_factor * self.create_transmit_flow(max_flow, expected_flow)
                x = y + zone_2_neighbors_transmit_flow[elem]  # 对于elem(某邻居)，累计车辆数 = 旧的累计车辆数 + 流入
                accumulated_vehicles = old_accumulated_vehicles + self.create_transmit_flow(max_flow, expected_flow)- zone_2_neighbors_transmit_flow[elem]  # 流出小区 ，累计车辆数 = 旧的 +新的- 流出
                old_accumulated_vehicles = accumulated_vehicles
            elif x < y * 0.5:
                transmit_factor = 0.7
                zone_2_neighbors_transmit_flow[elem] = transmit_factor * self.create_transmit_flow(max_flow, expected_flow)
                x = y + zone_2_neighbors_transmit_flow[elem]  # 对于elem(某邻居)，累计车辆数 = 旧的累计车辆数 + 流入
                accumulated_vehicles = old_accumulated_vehicles + self.create_transmit_flow(max_flow, expected_flow)- zone_2_neighbors_transmit_flow[elem]  # 流出小区 ，累计车辆数 = 旧的 +新的- 流出
                old_accumulated_vehicles = accumulated_vehicles
        self.after_actions_accumulated_vehicles[id] = after_actions_accumulated_vehicles.append(old_accumulated_vehicles)
        self.neighbors_current_transmit_flow[id] = zone_2_neighbors_transmit_flow

    def execute_action_by(self, id, action, action_config):
        if action_config['types'][action] == '选择低等流量':
            self.__execute_action_transmit_low_flow(id=id)
        elif action_config['types'][action] == '选择中等流量':
            self.__execute_action_transmit_normal_flow(id=id)
        elif action_config['types'][action] == '选择高等流量':
            self.__execute_action_transmit_high_flow(id=id)
        else:
            raise Exception('there is no such action')

    # def __execute_action_transmit_low_flow(self, id, zone_paras):
    #     accumulated_vehicles = zone_paras['accumulated_vehicles']
    #     old_accumulated_vehicles = zone_paras['old_accumulated_vehicles']
    #     critical_accumulated_vehicles = zone_paras['critical_accumulated_vehicles']
    #     neighbors = zone_paras['neighbors']
    #
    #     zone_2_neighbors_transmit_flow = {}
    #     after_actions_accumulated_vehicles = []
    #     for elem, x, y in zip(neighbors, neighbors_accumulated_vehicles, neighbors_old_accumulated_vehicles):
    #         if x > y * 0.9 and x < y:
    #             transmit_factor = 0.1
    #             zone_2_neighbors_transmit_flow[elem] = transmit_factor * self.create_transmit_flow(max_flow, expected_flow)  # 生成传输流
    #             x = y + zone_2_neighbors_transmit_flow[elem]  # 对于elem(某邻居)，累计车辆数 = 旧的累计车辆数 + 流入
    #             accumulated_vehicles = old_accumulated_vehicles + self.create_transmit_flow(max_flow, expected_flow) - zone_2_neighbors_transmit_flow[elem]  # 流出小区 ，累计车辆数 = 旧的 +新的- 流出
    #             old_accumulated_vehicles = accumulated_vehicles
    #         elif x > y * 0.5 and x < old_accumulated_vehicles * 0.9:
    #             transmit_factor = 0.5
    #             zone_2_neighbors_transmit_flow[elem] = transmit_factor * self.create_transmit_flow(max_flow, expected_flow)
    #             x = y + zone_2_neighbors_transmit_flow[elem]  # 对于elem(某邻居)，累计车辆数 = 旧的累计车辆数 + 流入
    #             accumulated_vehicles = old_accumulated_vehicles + self.create_transmit_flow(max_flow, expected_flow) - zone_2_neighbors_transmit_flow[elem]  # 流出小区 ，累计车辆数 = 旧的 +新的- 流出
    #             old_accumulated_vehicles = accumulated_vehicles
    #         elif x < y * 0.5:
    #             transmit_factor = 0.7
    #             zone_2_neighbors_transmit_flow[elem] = transmit_factor * self.create_transmit_flow(max_flow, expected_flow)
    #             x = y + zone_2_neighbors_transmit_flow[elem]  # 对于elem(某邻居)，累计车辆数 = 旧的累计车辆数 + 流入
    #             accumulated_vehicles = old_accumulated_vehicles + self.create_transmit_flow(max_flow, expected_flow) - zone_2_neighbors_transmit_flow[elem]  # 流出小区 ，累计车辆数 = 旧的 +新的- 流出
    #             old_accumulated_vehicles = accumulated_vehicles
    #     self.after_actions_accumulated_vehicles[id] = after_actions_accumulated_vehicles.append(
    #         old_accumulated_vehicles)
    #     self.neighbors_current_transmit_flow[id] = zone_2_neighbors_transmit_flow

    def __execute_action_transmit_low_flow(self, id):
        transmit_influence_factor = 0.1
        # neighbors = zone_paras['neighbors']
        # neighbors_current_accumulated_vehicles = zone_paras['neighbors_current_accumulated_vehicles']
        # neighbors_critical_accumulated_vehicles = zone_paras['neighbors_critical_accumulated_vehicles']

        # get_zone_2_neighbors_transmit_flow = {}
        A = self.create_transmit_flow()
        transmit_flow = transmit_influence_factor * A
        # for elem in (neighbors, neighbors_current_accumulated_vehicles):
        #
        #     get_zone_2_neighbors_transmit_flow[elem] = transmit_influence_factor * self.create_transmit_flow(max_flow, expected_flow)  # 生成传输流

        # self.zone_2_neighbors_transmit_flow[id] = get_zone_2_neighbors_transmit_flow
        # print(get_zone_2_neighbors_transmit_flow)

        # return self.zone_2_neighbors_transmit_flow
        return transmit_flow




        # self.neighbors.current_accumulated_vehicles = self.neighbors.current_accumulated_vehicles + transmit_flow
        # self.current_accumulated_vehicles = self.current_accumulated_vehicles - transmit_flow

        # self.zone_2_neighbors_transmit_flow[id] = get_zone_2_neighbors_transmit_flow

    # def __execute_action_transmit_normal_flow(self, id):
    #     transmit_influence_factor = 0.5
    #     # neighbors = zone_paras['neighbors']
    #     # neighbors_current_accumulated_vehicles = zone_paras['neighbors_current_accumulated_vehicles']
    #     # neighbors_critical_accumulated_vehicles = zone_paras['neighbors_critical_accumulated_vehicles']
    #
    #     get_zone_2_neighbors_transmit_flow = {}
    #
    #     for elem, current_accumulated_vehicles in zip(neighbors, neighbors_current_accumulated_vehicles):
    #         get_zone_2_neighbors_transmit_flow[elem] = transmit_influence_factor * self.create_transmit_flow(max_flow, expected_flow)  # 生成传输流
    #
    #     self.zone_2_neighbors_transmit_flow[id] = get_zone_2_neighbors_transmit_flow
    #     print(get_zone_2_neighbors_transmit_flow)
    #     return self.zone_2_neighbors_transmit_flow
    #
    # def __execute_action_transmit_high_flow(self, id):
    #     transmit_influence_factor = 0.7
    #     # neighbors = zone_paras['neighbors']
    #     # neighbors_current_accumulated_vehicles = zone_paras['neighbors_current_accumulated_vehicles']
    #     # neighbors_critical_accumulated_vehicles = zone_paras['neighbors_critical_accumulated_vehicles']
    #
    #     get_zone_2_neighbors_transmit_flow = {}
    #
    #     for elem, current_accumulated_vehicles in zip(neighbors, neighbors_current_accumulated_vehicles):
    #         get_zone_2_neighbors_transmit_flow[elem] = transmit_influence_factor * self.create_transmit_flow(max_flow,
    #                                                                                                          expected_flow)  # 生成传输流
    #
    #     self.zone_2_neighbors_transmit_flow[id] = get_zone_2_neighbors_transmit_flow
    #     print(get_zone_2_neighbors_transmit_flow)
    #     return self.zone_2_neighbors_transmit_flow

    def __execute_action_transmit_normal_flow(self, id):
        transmit_influence_factor = 0.5
        A = self.create_transmit_flow()
        transmit_flow = transmit_influence_factor * A
        return transmit_flow


    def __execute_action_transmit_high_flow(self, id):
        transmit_influence_factor = 0.7
        A = self.create_transmit_flow()
        transmit_flow = transmit_influence_factor * A
        return transmit_flow

    def get_zone_2_neighbors_transmit_flow_by(self, agent_id, neighbor_id):
        transmit_influence_factor = 0.1
        A = self.create_transmit_flow()
        transmit_flow = transmit_influence_factor * A
      

        # print(dic_1)
