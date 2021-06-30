from utilities.static_utilities import *
from traffic_environment import TrafficEnvironment


if __name__ == "__main__":
    # to read settings info
    env_setting, dqn_settings = get_settings_from_yaml(yaml_file='_config.yaml')
    # to initialize SUMO
    sumo_environment = TrafficEnvironment(env_setting=env_setting)  # traffic environment
    
    sumo_environment.simulation_step()
    
    sumo_environment.pre_run_simulation_to_prepare(10000)