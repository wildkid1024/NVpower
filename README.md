# NVpower 

**NVpower** is a tool to measure the  energy consumption of NVIDIA GPUs.

**NVpower** uses [NVML SDK (Nvidia Management Library)](https://developer.nvidia.com/nvidia-management-library-nvml) to perform a sequence of power measurements sampling on the specified NVIDIA GPU devices during the execution of a given process.  

The measured energy consumption can be calculated by the following formula:

```
Energy_measure = (Power_sampled - Power_static) * Duration 
```

## Installation

Make sure that you use the python3 environment. In some linux machine, python usually means python2 but not python3, and also pip.

In order to avoid unnecessary errors, it is better to install the ```nvidia-ml-py3``` package.

requirement:
- python3
- nvidia-ml-py3

Find the python release whleel [https://github.com/wildkid1024/NVpower/releases/tag/0.0.1](https://github.com/wildkid1024/NVpower/releases/tag/0.0.1), then 

```bash
> pip install NVpower-0.0.1-py3-none-any.whl
``` 

## Usage

#### CLI

```bash
> NVpower --job /path/to/job --gpu_id device_id --interval 1
```
example:

```bash
# run "./GPU_bin argv1 argv2" program with device 0 
> CUDA_VISIBLE_DEVICES=0 NVpower -j "./atm 24 1024" -d 0
```

#### Python package

#### CPP lib

## ToDo

- [x] Add sampling interval
- [ ] Add output file
- [ ] Add threshold power
- [ ] Add all deveice power moniter

## Related Works

1. Collange, Sylvain, David Defour, and Arnaud Tisserand. "Power consumption of GPUs from a software perspective." International Conference on Computational Science. Springer, Berlin, Heidelberg, 2009. 
2. Mittal, Sparsh, and Jeffrey S. Vetter. "A survey of methods for analyzing and improving GPU energy efficiency." ACM Computing Surveys (CSUR) 47.2 (2014): 1-23.

## Update logs

- Version 0.0.1 2020-12-03
  - release the new built package


