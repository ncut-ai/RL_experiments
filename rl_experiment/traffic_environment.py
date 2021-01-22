"""
# traffic_environment.py
# 12/2/2020 created by 
#
# Here the TrafficEnvironment Class defined with which a traffic simulation model is described, highly correlating to
# SUMO the platform.
"""

import traci


class TrafficEnvironment:
    def __init__(self, env_setting):
        print('初始化仿真环境……')
        traci.start(env_setting['sumo_start_config'])  # initialize traci

    def simulation_step(self):
        """# 执行一步仿真"""
        traci.simulationStep()

    def retrieve_state_by(self, state_type, paras):
        """# retrieve state value"""
        if state_type == 'queue_count' or state_type == 'queue_count_edge':  # 边 上的排队长度
            return self.__retrieve_queue_count_on_edge(edge_id=paras)
        elif state_type == 'remaining_phase_duration':  # 当前相位的剩余时长
            return self.__retrieve_remaining_phase_duration_on_edge_by(tls_id=paras)
        elif state_type == 'phase_id':  # 当前相位的序号
            return self.__retrieve_current_phase_id_by(tls_id=paras)
        elif state_type == 'vehicle_number_edge':  # 边 上的车辆数
            return self.__retrieve_vehicle_number_on_edge_by(edge_id=paras)
        elif state_type == 'mean_speed_edge':  # 边 上的平均速度
            return self.__retrieve_mean_speed_on_edge_by(edge_id=paras)
        elif state_type == 'occupancy_edge':  # 边 上的占有率
            return self.__retrieve_occupancy_on_edge_by(edge_id=paras)
        elif state_type == 'waiting_time_edge':  # 边 上的等待时间
            return self.__retrieve_waiting_time_on_edge_by(edge_id=paras)
        elif state_type == 'travel_time_edge':  # 边 上的旅行时间
            return self.__retrieve_travel_time_on_edge_by(edge_id=paras)
        elif state_type == 'ave_length_edge':  # 边 上的平均车辆长度
            return self.__retrieve_ave_length_on_edge_by(edge_id=paras)
        elif state_type == 'vehicle_number_lane':  # 车道上的车辆数
            return self.__retrieve_vehicle_number_on_lane_by(lane_id=paras)
        elif state_type == 'queue_count_lane':  # 车道上排队长度
            return self.__retrieve_queue_count_on_lane_by(lane_id=paras)
        elif state_type == 'mean_speed_lane':  # 车道上平均速度
            return self.__retrieve_mean_speed_on_lane_by(lane_id=paras)
        elif state_type == 'occupancy_lane':  # 车道上占有率
            return self.__retrieve_occupancy_on_lane_by(lane_id=paras)
        elif state_type == 'waiting_time_lane':  # 车道上等待时间
            return self.__retrieve_waiting_time_on_lane_by(lane_id=paras)
        elif state_type == 'travel_time_lane':  # 车道上旅行时间
            return self.__retrieve_travel_time_on_lane_by(lane_id=paras)
        elif state_type == 'ave_length_lane':  # 车道上平均车辆长度
            return self.__retrieve_ave_length_on_lane_by(lane_id=paras)
        else:
            raise Exception('there is no such bizarre state type')

    def execute_action_by(self, tls_id, action, action_config):
        """execute action"""
        if action_config['types'][action] == 'keep':  # 什么也不做
            pass
        elif action_config['types'][action] == 'switch':  # 切换到下一相位，不改变相序
            self.__execute_action_switch_to_next_phase(tls_id=tls_id)
        elif action_config['types'][action] == 'switch_to_phase':  # 切换到指定的相位
            self.__execute_action_switch_to_given_phase(tlsID=tls_id, para=action_config['para'][action])
        elif action_config['types'][action] == 'set_max_speed_edge':  # 设置道路上的最大速度
            self.__execute_action_set_max_speed_on_edge(para=action_config['para'][action])
        elif action_config['types'][action] == 'set_max_speed_lane':  # 设置车道上的最大速度
            self.__execute_action_set_max_speed_on_lane(para=action_config['para'][action])
        elif action_config['types'][action] == 'add_phase_duration':  # 增加当前相位的时长
            self.__execute_action_add_current_phase_duration(tlsID=tls_id, para=action_config['para'][action])
        else:
            raise Exception('there is no such action')

    def retrieve_reward_by(self, reward_type, paras):
        """# retrieve reward value"""
        if reward_type == 'sum_waiting_time':
            return self.__retrieve_sum_waiting_time_on_edges(edge_ids=paras)
        elif reward_type == 'sum_queue_count':  # '路口总排队长度': 'sum_queue_count',
            return self.__retrieve_sum_queue_count_on_edges(edge_ids=paras)
        elif reward_type == 'sum_travel_time':  # '路口总旅行时间': 'sum_travel_time',
            return self.__retrieve_sum_travel_time_on_edges(edge_ids=paras)
        elif reward_type == 'sum_occupancy':  # '路口占有率': 'sum_occupancy',
            return self.__retrieve_sum_occupancy_on_edges(edge_ids=paras)
        elif reward_type == 'ave_mean_speed':  # '平均速度': 'ave_mean_speed',
            return self.__retrieve_ave_mean_speed_on_edges(edge_ids=paras)
        elif reward_type == 'ave_length':  # '平均车辆长度': 'ave_length',
            return self.__retrieve_ave_length_on_edges(edge_ids=paras)
        else:
            raise Exception('there is no such reward type')

    def __retrieve_sum_waiting_time_on_edges(self, edge_ids):
        """retrieve waiting time sum on edges"""
        sum_waiting_time = 0
        for edge_id in edge_ids:
            sum_waiting_time = sum_waiting_time + traci.edge.getWaitingTime(edge_id)
        return sum_waiting_time

    def __retrieve_sum_queue_count_on_edges(self, edge_ids):
        """获取所有给定道路上的排队长度之和"""
        sum_queue_count = 0
        for edge_id in edge_ids:
            sum_queue_count += traci.edge.getLastStepHaltingNumber(edgeID=edge_id)
        return sum_queue_count

    def __retrieve_sum_travel_time_on_edges(self, edge_ids):
        """获取所有给定道路上的旅行时间之和"""
        sum_travel_time = 0
        for edge_id in edge_ids:
            sum_travel_time += traci.edge.getTraveltime(edgeID=edge_id)
        return sum_travel_time

    def __retrieve_sum_occupancy_on_edges(self, edge_ids):
        """获取所有给定道路上的占有率之和"""
        sum_occupancy = 0
        for edge_id in edge_ids:
            sum_occupancy += traci.edge.getLastStepOccupancy(edgeID=edge_id)
        return sum_occupancy

    def __retrieve_ave_mean_speed_on_edges(self, edge_ids):
        """获取所有给定道路上的平均速度"""
        ave_mean_speed = 0.0
        for edge_id in edge_ids:
            ave_mean_speed += traci.edge.getLastStepMeanSpeed(edgeID=edge_id)
        return ave_mean_speed / len(edge_ids)

    def __retrieve_ave_length_on_edges(self, edge_ids):
        """获取所有给定道路上的平均车辆长度"""
        ave_length = 0.0
        for edge_id in edge_ids:
            ave_length += traci.edge.getLastStepLength(edgeID=edge_id)
        return ave_length / len(edge_ids)

    def __execute_action_switch_to_given_phase(self, tlsID, para):
        """切换到指定相位"""
        index = int(para)
        traci.trafficlight.setPhase(tlsID=tlsID, index=index)

    def __execute_action_set_max_speed_on_edge(self, para):
        """设置道路上最大速度"""
        traci.edge.setMaxSpeed(edgeID=para[0], speed=para[1])

    def __execute_action_set_max_speed_on_lane(self, para):
        """设置车道的最大速度"""
        traci.lane.setMaxSpeed(laneID=para[0], speed=para[1])

    def __execute_action_add_current_phase_duration(self, tlsID, para):
        """增加当前相位的时长"""
        current_phase_duration = traci.trafficlight.getPhaseDuration(tlsID=tlsID)
        traci.trafficlight.setPhaseDuration(tlsID=tlsID, phaseDuration=current_phase_duration + para)

    def __execute_action_switch_to_next_phase(self, tls_id):
        """切换到下一个相位"""
        traci.trafficlight.setPhaseDuration(tlsID=tls_id, phaseDuration=0)

    def pre_run_simulation_to_prepare(self, pre_steps):
        """ pre run simulation with doing nothing"""
        traci.simulationStep(pre_steps)

    def __retrieve_queue_count_on_edge(self, edge_id):
        """retrieve queue count on edge"""
        return traci.edge.getLastStepHaltingNumber(edgeID=edge_id)

    def __retrieve_remaining_phase_duration_on_edge_by(self, tls_id):
        """获取当前相位剩余绿灯时间"""
        return traci.trafficlight.getNextSwitch(tlsID=tls_id) - traci.simulation.getTime()

    def __retrieve_current_phase_id_by(self, tls_id):
        """获取当前相位ID，序号"""
        return traci.trafficlight.getPhase(tlsID=tls_id)

    def __retrieve_vehicle_number_on_edge_by(self, edge_id):
        """获取 边 上的车辆数"""
        return traci.edge.getLastStepVehicleNumber(edgeID=edge_id)

    def __retrieve_mean_speed_on_edge_by(self, edge_id):
        """获取 边 上的平均速度"""
        return traci.edge.getLastStepMeanSpeed(edgeID=edge_id)

    def __retrieve_occupancy_on_edge_by(self, edge_id):
        """获取 边 上的占有率"""
        return traci.edge.getLastStepOccupancy(edgeID=edge_id)

    def __retrieve_waiting_time_on_edge_by(self, edge_id):
        """获取 边 上的等待时间"""
        return traci.edge.getWaitingTime(edgeID=edge_id)

    def __retrieve_travel_time_on_edge_by(self, edge_id):
        """获取 道路 上的旅行时间"""
        return traci.edge.getTraveltime(edgeID=edge_id)

    def __retrieve_ave_length_on_edge_by(self, edge_id):
        """获取 道路 上的平均车辆长度"""
        return traci.edge.getLastStepLength(edgeID=edge_id)

    def __retrieve_vehicle_number_on_lane_by(self, lane_id):
        """获取 道路 上的车辆数"""
        return traci.lane.getLastStepVehicleNumber(laneID=lane_id)

    def __retrieve_queue_count_on_lane_by(self, lane_id):
        """获取车道上的排队长度"""
        return traci.lane.getLastStepHaltingNumber(laneID=lane_id)

    def __retrieve_mean_speed_on_lane_by(self, lane_id):
        """获取车道上的平均速度"""
        return traci.lane.getLastStepMeanSpeed(laneID=lane_id)

    def __retrieve_occupancy_on_lane_by(self, lane_id):
        """获取车道上的占有率"""
        return traci.lane.getLastStepOccupancy(laneID=lane_id)

    def __retrieve_waiting_time_on_lane_by(self, lane_id):
        """获取车道上的等待时间"""
        return traci.lane.getWaitingTime(laneID=lane_id)

    def __retrieve_travel_time_on_lane_by(self, lane_id):
        """获取车道上的旅行时间"""
        return traci.lane.getTraveltime(laneID=lane_id)

    def __retrieve_ave_length_on_lane_by(self, lane_id):
        """获取车道上的平均车辆长度"""
        return traci.lane.getLastStepLength(laneID=lane_id)
