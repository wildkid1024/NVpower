CUDA_DIR = /usr/local/cuda-10.2
CUDA_INC = $(CUDA_DIR)/include
CUDA_GDK = $(CUDA_DIR)/gdk
CUDA_LIB = $(CUDA_DIR)/lib64

NVCC = nvcc
NVCFLAGS = -ccbin g++ -shared -m64 --compiler-options '-fPIC'
GENCODE = -gencode arch=compute_30,code=sm_30 -gencode arch=compute_35,code=sm_35 -gencode arch=compute_37,code=sm_37 -gencode arch=compute_50,code=sm_50 -gencode arch=compute_52,code=sm_52 -gencode arch=compute_60,code=sm_60 -gencode arch=compute_61,code=sm_61 -gencode arch=compute_70,code=sm_70 -gencode arch=compute_75,code=sm_75 -gencode arch=compute_75,code=compute_75
CUDALIBS = -L$(CUDA_DIR)/lib64i -L$(NVML_LIB) -L$(CUDA_DIR)/extras/CUPTI/lib64 -lcuda -lcudart -lnvidia-ml -lstdc++ -lm  -ldl -I$(NVML_INC) -I$(CUDA_DIR)/extras/CUPTI/include


CC = g++
CFLAGS = -Wall -g -std=c++11 -fPIC -shared 
SPECIALFLAGS = -lnvidia-ml -lpthread 

SRC = NVpower.cpp
OBJECT = libnvpower.o
TARGET = libnvpower.so

all: $(TARGET)

$(TARGET): $(OBJECT)
	$(CC)  $(CFLAGS) -I $(CUDA_INC) -I $(CUDA_GDK) -L $(CUDA_LIB) -o $(TARGET) $(OBJECT) $(SPECIALFLAGS) -lcudart -lcuda
	# $(NVCC) $(NVCFLAGS) $(GENCODE) $(CUDALIBS) -o $(TARGET) $(OBJECT)

$(OBJECT): $(SRC) 
	$(CC) $(CFLAGS) -I$(CUDA_INC) -I$(CUDA_GDK) -L$(CUDA_LIB) -ldl -o $(OBJECT) -c $(SRC)
	# $(NVCC) $(NVCFLAGS) $(GENCODE) $(CUDALIBS) -ldl -o $(OBJECT) -c $(SRC)

gdb:
	gdb ./$(TARGET)
clean:
	rm -f *.o *.so
