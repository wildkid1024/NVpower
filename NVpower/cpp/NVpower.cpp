#include "NVpower.h"

NVpower::NVpower()
{
    this->flag = 0;

    this->device_id = 0;
    this->sample_interval = 1000.0;
    this->threshold_power = 0.0;
}

NVpower::NVpower(int device_id, float sample_interval, float threshold_power)
{
    NVpower();
    
    this->device_id = device_id;
    this->sample_interval = sample_interval;
    this->threshold_power = threshold_power;
}

NVpower::~NVpower()
{
    // shutdown_nvml();
}

void NVpower::start_monitoring()
{
    this->flag = 0;
    
    this->init_profiling();
}

void NVpower::end_monitoring() 
{
    this->flag = 1;

    this->stop_profiling();
}

void NVpower::end_monitoring(int sig) 
{
    this->flag = 1;

    this->stop_profiling();
}

void NVpower::monitor_power(nvmlDevice_t device, std::vector<float> *powerArray)
{
    nvmlReturn_t result;

    nvmlPstates_t pstates;
    result = nvmlDeviceGetPerformanceState(this->device, &pstates);
    if (NVML_ERROR_NOT_SUPPORTED == result) 
        printf("This does not support performance state query\n");
    else if (NVML_SUCCESS != result){
        printf("Failed to get the performance state for device %i: %s\n", this->device_id, nvmlErrorString(result));
        exit(1);
    }

    unsigned int power;

    result = nvmlDeviceGetPowerUsage(this->device, &power);

    if (NVML_ERROR_NOT_SUPPORTED == result)
        printf("This does not support power measurement\n");
    else if (NVML_SUCCESS != result)
    {
        printf("Failed to get power for device %i: %s\n", 0, nvmlErrorString(result));
        exit(1);
    }

    printf("Performance state: %d, Power: %d mw\n", pstates, power); /* For Debugging */

    if(flag == 0 && pstates == 2){
        (*powerArray).push_back(power/1000);  // power(W)
    }

}

pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

void* run_monitor(void* arg){
    pthread_mutex_lock(&mutex);
    NVpower* that;
    that = (NVpower *)arg;
    std::vector<float> powerArray;
    while(that->flag==0){
        that->monitor_power(that->device, &powerArray);
        usleep(that->sample_interval * 1000);
    }
    int size = powerArray.size();
    float sum = std::accumulate(powerArray.begin(), powerArray.end(), 0);
	
    float result = (that->sample_interval * sum * 0.001); // time(S) * power(W) = Energy(J)
    float power_result = sum/size;

    float threshold_energy = (that->threshold_power * size) * 0.001 * that->sample_interval;

    printf("==================================\n");
    // printf("debug size: %d\n", size);
    printf("Average Power: %f W\n", power_result - that->threshold_power);
    printf("Energy: %f J\n", result - threshold_energy);
    pthread_mutex_unlock(&mutex);
    return 0;
}

void NVpower::init_profiling(){
    nvmlReturn_t result;

    result = nvmlInit();
    if (NVML_SUCCESS != result)
    { 
        printf("Failed to initialize NVML: %s\n", nvmlErrorString(result));
        printf("Press ENTER to continue...\n");
        getchar();
        exit(1);
    }

    result = nvmlDeviceGetHandleByIndex(this->device_id, &this->device);
    if (NVML_SUCCESS != result)
    { 
        printf("INIT: Failed to get handle for device %i: %s\n", 0, nvmlErrorString(result));
        exit(1);
    }

    // signal(SIGINT, end_monitoring);


    //Start NMVL
    if(pthread_create(&this->thread_id, NULL, run_monitor, (void*)this)){
        printf("Thread Init Error\n");
    }

    printf("Thread id: %u  | start sampling...\n", (unsigned int)this->thread_id);
}

void NVpower::shutdown_nvml()
{
    nvmlReturn_t result;
    result = nvmlShutdown();
    if (NVML_SUCCESS != result)
        printf("Failed to shutdown NVML: %s\n", nvmlErrorString(result));
}

void NVpower::stop_profiling(){
    if(this->flag == 1){
    	// cudaDeviceSynchronize();

    	pthread_join(this->thread_id, NULL);
    	shutdown_nvml();

        printf("Thread id: %u | End sampling...\n", (unsigned int)this->thread_id);
    }
}
