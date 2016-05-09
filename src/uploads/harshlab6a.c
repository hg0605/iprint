#include<stdio.h>
#include<string.h>
#include<pthread.h>
#include<stdlib.h>
#include<unistd.h>
#include<semaphore.h>
#define size 10

int buf[10];
pthread_mutex_t block;
sem_t filled;
sem_t empty;
int pos=0;


void* producerFunc(void *args)
{
	int item;
	while(1)
	{
		item=30;
		
		sem_wait(&empty);
		pthread_mutex_lock(&block);
		if(pos<size)
		{
			buf[pos]=item;
			pos++;
		}
		pthread_mutex_unlock(&block);
		sem_post(&filled);
		sleep(1);
	}
}

void* consumerFunc(void *args)
{
	int item;
	while(1)
	{
		sem_wait(&filled);
		pthread_mutex_lock(&block);
		if(pos>0)
		{
			pos--;
			item=buf[pos];
			disp(item);
		}
		pthread_mutex_unlock(&block);
		sem_post(&empty);
		sleep(1);
	}
	return 0;
}


void main(int argc,void* argv[])
{
	int i=0;
	pthread_t producer;
	pthread_t consumer[4];
	
	pthread_mutex_init(&block,NULL);
	sem_init(&full,0,0);
	sem_init(&empty,0,size);

	pthread_create(&producer,NULL,producerFunc,NULL);
	pthread_create(&consumer[0],NULL,consumerFunc,NULL);
	pthread_create(&consumer[1],NULL,consumerFunc,NULL);
pthread_create(&consumer[2],NULL,consumerFunc,NULL);
pthread_create(&consumer[3],NULL,consumerFunc,NULL);
	
	pthread_exit(NULL);

}



