#include "queMed.h"
#include <stdlib.h>

void initQue(queque *q, size_t arraySize){

q->size = arraySize;  
q->array = malloc(sizeof(int) * q->size);
q->head = 0;
q->tail = 2;
q->med = 0;
q->value = 0;

}

int sorttingArray(int *pA, size_t arraySize){

int i = 0;

for(i = 0; i<arraySize; i++){

    if(pA[0] < pA[i]){

        pA[0] = pA[i];

    }
}

if(pA[1] < pA[2]){
    return pA[1];
}

else {
    return pA[2];
}

return;

}

int enQue(queque *q, int data1, int data2){

    q->value = (data1 + data2) / 2;

    if(q->size == 3){
        q->head = 0;
        q->med = sorttingArray(q->array,q->size);

        q->array[q->head] = q->array[1];
        q->array[1] = q->array[q->tail];
        q->array[q->tail] = q->value;

        return q->med;
    }

    q->array[q->head++] = q->value;
    q->head = (q->head +1 ) % q->size;
    return q->med;

}
