#ifndef _META_ATTR_H_
#define _META_ATTR_H_

#include <stdio.h>
#include <stdlib.h>

#include "def.h"

struct meta_attr
{
    char *key;
    char *val;
};

char *meta_attr_read(FILE *f);
int meta_attr_parse(FILE *f, struct meta_attr *attr);

#endif//_META_ATTR_H_
