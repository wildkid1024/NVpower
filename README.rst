# NVpower 

NVpower is a tool for measure the NVIDIA GPU computing power.

## Installation

requirement:
- pip
- nvidia-ml-py3

find the python release whleel, then 

```bash
> pip install NVpower-0.0.1-py3-none-any.whl
``` 

## Usage

```bash
> NVpower --job /path/to/job --gpu_id device_id --interval 1
```
example:

```bash
# run "./GPU_bin argv1 argv2" program with device 0 
> CUDA_VISIBLE_DEVICES=0 NVpower -j "./atm 24 1024" -d 0
```

## ToDo

- [x] Add sampling interval
- [ ]  Add output file
- [ ] Add threshold power