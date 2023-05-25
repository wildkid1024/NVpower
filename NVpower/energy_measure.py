import time
import threading
import logging
from threading import Thread
from typing import List, Dict, DefaultDict
from collections import defaultdict
from pynvml import *

logging.basicConfig(level=logging.DEBUG)


def get_average(data:List)->Dict:
    return [sum(data) / len(data), min(data), max(data)]


class MonitorResult():
    def __init__(self, result=None, samples:dict=None):
        self.result = result
        self.samples = samples
        self.device_info = defaultdict(tuple)

        self.compute()

    def compute(self, ) -> dict:
        for kw, value in self.samples.items():
            self.device_info[kw] = get_average(value)
        return self.device_info

    def __len__(self, ):
        return len(self.samples["power"])
   
    def __str__(self):
        help_info = "please use attr result and device_info to get the function result and device_info"
        return help_info
        
    
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
def get_gpu_power(gpu_id:int=0, sample_interval:int=1000)->DefaultDict:
    try:
        nvmlInit()
    except Exception as e:
        print(e)
        logging.error("No GPU was found!")
        return
    
    driver_info = nvmlSystemGetDriverVersion()
    driver_info = ''.join(driver_info)
    logging.info("Driver: " + driver_info)  #显示驱动信息
    handle = nvmlDeviceGetHandleByIndex(gpu_id)
    cnt = 0
    samples_info = defaultdict(list)
    while cnt < 5:
        gpu_mem_info = nvmlDeviceGetMemoryInfo(handle)
        gpu_temperature_info = nvmlDeviceGetTemperature(handle, NVML_TEMPERATURE_GPU)
        gpu_fan_info = nvmlDeviceGetFanSpeed_v2(handle, NVML_FAN_NORMAL)
        power_state = nvmlDeviceGetPowerState(handle)
        power_info = nvmlDeviceGetPowerUsage(handle)
        gpu_util_rate_info = nvmlDeviceGetUtilizationRates(handle)

        # print("Memory Total: ",info.total)
        # print("Memory Free: ",info.free)
        logging.debug("GPU Memory total: {} |GPU Memory used: {} |GPU Memory free: {}"\
                      .format(gpu_mem_info.total, gpu_mem_info.used, gpu_mem_info.free))
        logging.debug("GPU temperature: {}".format(gpu_temperature_info))
        logging.debug("GPU fan speed: {}".format(gpu_fan_info))
        logging.debug("GPU util rate:{} | memory rate".format(gpu_util_rate_info.gpu, gpu_util_rate_info.memory))
        logging.debug("GPU Power ststus:{}, useage:{}".format(power_state, power_info))
        
        samples_info["memory"].append(gpu_mem_info.used)
        samples_info["temperature"].append(gpu_temperature_info)
        samples_info["fan"].append(gpu_fan_info)
        samples_info["util"].append(gpu_util_rate_info.gpu)
        if power_state == 2:
            samples_info["power"].append(power_info)
        elif power_state == 8:
            cnt += 1

        time.sleep(sample_interval * 0.001)
    nvmlShutdown()
    
    return samples_info

def get_device_samples(gpu_id:int=0, sample_interval:int=1000, threshold_power:float=0.0):
    def device_info_func(func:callable):
        def call_func(*args, **kwargs):
            main_thread = MonitorThread(target=func , args=args, kwargs=kwargs)
            sample_thread = MonitorThread(target=get_gpu_power, args=(gpu_id, sample_interval))
            sample_thread.start()
            main_thread.start()
            sample_thread.join()
            main_thread.join()
            fun_result = main_thread.get_result()
            samples_info = sample_thread.get_result()

            print(samples_info)

            result = MonitorResult(fun_result, samples_info)
            result.device_info["power"][0] -= threshold_power

            run_time = sample_interval * len(samples_info)
            run_energy = 0.001 * run_time * result.device_info["power"][0]
            logging.debug('%s() | run time: %s ms | run energy: %s J | run power: %s W' % (func.__name__, run_time, run_energy, result.device_info["power"][0]))
            
            return result
        return call_func
    return device_info_func
