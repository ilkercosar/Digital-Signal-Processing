#include "maf.h"

static maf filter;

void filter_init(void){
    filter.size = 1;
    filter.filter = malloc(sizeof(int) * filter.size);
    filter.oldValue = 0;
    filter.filter[filter.size-1] = 0;
}

int filter_update(void){
    filter.filter[filter.size-1] = filter.oldValue + (signal() / filter.size); 
    filter.oldValue = filter.filter[filter.size - 1];
    filter.size++;
    filter.filter = realloc(filter.filter, sizeof(int) * (filter.size));
    return (filter.filter[filter.size - 2]);
}

void filter_reset(void){
    filter.size = 0;    
    filter.oldValue = 0;
    free(filter.filter);
}