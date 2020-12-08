#include <dlfcn.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <cuda_profiler_api.h>
#include <cuda_runtime.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <nvml.h>
#include <signal.h>
#include <pthread.h>
#include <iostream>
#include <algorithm>
#include <vector>
#include <functional>
#include <numeric>
#include <cuda.h>
#include <stdio.h>
#include <cuda_runtime_api.h>
#include <cassert>
#include <map>
#include <list>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/types.h>
#include <unistd.h>


#include <unistd.h>
#include <pthread.h>


class NVpower
{
private:
    volatile sig_atomic_t flag;
    unsigned int device_id;
    nvmlDevice_t device;
    float sample_interval;
    float threshold_power;
    /* -----some variable must be used-------  */
    pthread_t thread_id;
private:
    void init_profiling();
    friend void* run_monitor(void *);
    void monitor_power(nvmlDevice_t device, std::vector<float> *powerArray);
    void shutdown_nvml();
    void stop_profiling();
public:
    NVpower();
    NVpower(int device_id, float sample_interval, float threshold_power);
    ~NVpower();
    void start_monitoring();
    void end_monitoring();
    void end_monitoring(int sig);
};