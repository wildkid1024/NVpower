#include <bits/stdc++.h>
#include "NVpower.h"
using namespace std;

void fun(long long num)
{
    for (int i=0;i<num;i++);
}


void* foo(void * arg)
{
    int flag = *(unsigned int *)arg;
    printf("flag = %u\n", flag);
}
int main2()
{
    int i = 0;
    pthread_t tid[10];
    // pthread_t tid;
    for (i=0; i<10;i++)
    {
    pthread_create(&tid[i], NULL, foo, (void *)&tid);
    pthread_join(tid[i], NULL);
    }
    return 0;
}

int main()
{
    const long long  num = 1e9;
    NVpower* p = new NVpower(0, 200.0, 0.0);
    p->start_monitoring();
    fun(num);
    p->end_monitoring();
}