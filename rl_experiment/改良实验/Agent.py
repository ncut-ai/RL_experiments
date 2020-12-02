import traci
import readyaml


class GetInformation:
    def __init__(self, cross_id, edge_id):
        self.cross_id = cross_id
        self.edge_id = edge_id

    def __get_current_state(self):
        """获取一个路口每条边的排队长度，所有边的排队长度之和为路口排队长度作为返回值"""
        cross_queque_count = 0
        for i in self.edge_id:
            one_road_queque_count = eval(readyaml.str_state_function)
            cross_queque_count += one_road_queque_count
        return cross_queque_count

    def get_current_state(self):
        """调用私有函数，获得一个路口的排队长度总数"""
        return self.__get_current_state()

    def __get_execaction(self, action):
        """选择动作，当action==0时，动作为切换相位"""
        if action == 0:
            eval(readyaml.str_action_function)
            print("Yes")
        else:
            print("None")

    def do_action(self, action):
        """调用选择动作的函数"""
        return self.__get_execaction(action)

    def __get_waiting_time(self):
        """获得路口四车道的等待时间之和"""
        waitting_time = 0.00
        for i in self.edge_id:
            one_road_waitting_time = traci.edge.getWaitingTime(i)
            waitting_time += one_road_waitting_time
        return waitting_time

    def get_waiting_time(self):
        """调用获得路口等待时间的函数"""
        return self.__get_waiting_time()

    # 计算奖励
    def __caculate_delayed_reward(self):
        """根据等待时间计算奖励"""
        wait_time = self.get_waiting_time()
        WAITTIME = 10
        if wait_time > 2 * WAITTIME:
            delay_reward = 0
        elif wait_time < WAITTIME:
            delay_reward = 2
        else:
            delay_reward = 1
        return delay_reward

    def caculate_reward(self):
        """调用计算等待时间的函数"""
        return self.__caculate_delayed_reward()
