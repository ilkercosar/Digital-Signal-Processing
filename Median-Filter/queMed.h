#ifndef __queMed__
#define __queMed__

typedef struct{

int *array; 
int size,head,tail,med,value;

}queque;

void initQue(queque *q, size_t arraySize);
int sorttingArray(int *pA, size_t arraySize);
int enQue(queque *q, int data1, int data2);

#endif
