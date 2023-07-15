#include "maf.h"
#include <stdio.h>

int signal(void){
    return rand()%100;
}

void delay(void){
	int i = 0;
    for (i = 0; i < 500000000; i++)
    {

    }
}

int main(){

    filter_init();
    while(1){
        if(signal()%5 == 0){
            printf("Filtered Value: %d\n",filter_update());
        }
        else{
            printf("Unfiltered Value: %d\n",signal());
        }
        delay();
    }
}
