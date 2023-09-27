/**
*  Multithreading example in C
*  This example can be compiled only on a Linux machine
*  or alternatively on Windows Subsystem Linux (WSL)
*  Author: Jacopo Abramo, 26.09.2023
*/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>
#define NUM_THREADS 2
 
void *worker(void *maxCount)
{
    int count = *(int*)maxCount;
    int counter = 0;

    printf("Starting new thread (count = %d)...\n", count);
    while(count > 0)
    {
        count--;
    }

    printf("Thread terminated! Counter reached %d\n", count);
    return NULL;
}
 
int main(void)
{
    int maxCount = 100000000 / NUM_THREADS;

    pthread_t threads[NUM_THREADS];

    for(int i = 0; i < NUM_THREADS; i++)
    {
        pthread_create(&threads[i], NULL, worker, &maxCount);
    }

    for(int i = 0; i < NUM_THREADS; i++)
    {
        pthread_join(threads[i], NULL);
    }

    printf("Exiting from main program\n");
    return 0;
}