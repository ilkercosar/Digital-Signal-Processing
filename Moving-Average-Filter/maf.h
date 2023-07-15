#ifndef Filter__
#define Filter__

#ifdef __cplusplus
extern "C" {
#endif

#include <stdlib.h>

typedef struct maf{
    int *filter, size, oldValue;
}maf;

void filter_init(void);
int filter_update(void);
void filter_reset(void);

#ifdef __cplusplus
}
#endif
#endif