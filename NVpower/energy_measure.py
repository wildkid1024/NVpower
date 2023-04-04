import time
import threading
import logging
from threading import Thread

from pynvml import *

logging.basicConfig(level=logging.DEBUG)

class MonitorResult():
    def __init__(self, result=None, powers=None):
        self.result = result
        self.powers = powers
        
    
    def __str__(self):
        help_info = "please use attr result and powers to get the function result and run powers"
        
    
class MonitorThread(Thread):
    def __init__(self, target=None, args=(), kwargs=None):
        super(MonitorThread, self).__init__()
        if kwargs is None:
            kwargs = {}
        self.func = target
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.result = self.func(*self.args, **self.kwargs)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None
        
# 每秒采样一次 require pynvml(only linux)
def get_gpu_power(gpu_id, sample_interval):
    nvmlInit()
    logging.info("Driver: ", nvmlSystemGetDriverVersion())  #显示驱动信息
    handle = nvmlDeviceGetHandleByIndex(gpu_id)
    energy, cnt = 0, 0
#     run_cnt = 0
    sampled_power = []
    while True:
        info = nvmlDeviceGetMemoryInfo(handle)
        # print("Memory Total: ",info.total)
        # print("Memory Free: ",info.free)
        # print("Memory Used: ",info.used)
        powerstate = nvmlDeviceGetPowerState(handle)
        power = nvmlDeviceGetPowerUsage(handle)
        logging.debug("Power ststus:{}, useage:{}".format(powerstate, power))
        if powerstate == 2:
#             energy += power
#             run_cnt += 1
            sampled_power.append(power)
        elif powerstate == 8:
            if cnt >= 5: break
            else: cnt += 1
                
        time.sleep(sample_interval * 0.001)
    nvmlShutdown()
    
    return sampled_power

def run_energy_mj(gpu_id=0, sample_interval=1000, threshold_power=0.0):
    def run_gpu_energy_mj(func):
        def call_fun(*args, **kwargs):
            main_thread = MonitorThread(target=func , args=args, kwargs=kwargs)
            power_thread = MonitorThread(target=get_gpu_power, args=(gpu_id, sample_interval))
            power_thread.start()
            main_thread.start()
            power_thread.join()
            main_thread.join()
            
            fun_result = main_thread.get_result()
            sampled_power = power_thread.get_result()
            run_energy, run_cnt = sum(sampled_power), len(sampled_power)
            run_time = run_cnt * sample_interval
            threshold_energy = threshold_power * run_time * 0.001
            logging.debug('%s() | run time: %s ms | run energy: %s J | run power: %s W' % (func.__name__, run_time, run_energy * sample_interval * 0.001 - threshold_energy, run_energy / run_cnt - threshold_power))
            
            result = MonitorResult(fun_result, run_energy / run_cnt - threshold_power)
            return result
        return call_fun
    return run_gpu_energy_mj
