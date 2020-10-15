import sys
import os
import traci
import traci.constants as tc
#
from RLAgent import RLAgent #Agent类
##--------------------------------------------------------------------------------
##--------------------------- 基本配置数据&信息 -----------------------------------------------------
#仿真模型
#sumoCmd = ["sumo", "-c", "4RL-test/simple6nodes.sumocfg"]
sumoCmd = ["sumo-gui", "-c", "4RL-test/simple6nodes.sumocfg", '--start']
##--------------------------初始化仿真 traci -----------------------------
traci.start(sumoCmd)

##---------------------------------- 基本变量初始化 ----------------------------------------------
junctionList = traci.trafficlight.getIDList()
#所有路口
allJunctions = []
for xj in junctionList:
   theJunction = RLAgent(xj)
   theJunction.setPhaseNum(len(traci.trafficlight.getCompleteRedYellowGreenDefinition(xj)[0].phases))#相位数
   for index, thePhase in enumerate(traci.trafficlight.getCompleteRedYellowGreenDefinition(xj)[0].phases):#获取一个相位，和索引
      if thePhase.duration > 10: #找到有效的相位，不重要的相位不考虑
         theJunction.addPhase(str(index)) #将相位编号加入
   allJunctions.append(theJunction)
##--------------------------
#
##------------------------- 初始化计数变量 --------------------------------
step = 0 #设置步长计数
## ------------------------------  开始进行仿真  ------------------------------------------
#Run a simulation until all vehicles have arrived
while traci.simulation.getMinExpectedNumber() > 0:
   print("step", step)
   step+=1
   traci.simulationStep()
   #----------------获取每个路口的交通状态评价
   print(traci.junction.getContextSubscriptionResults('J1'))


traci.close()