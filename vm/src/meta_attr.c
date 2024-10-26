#include "meta_attr.h"

char *meta_attr_read(FILE *f)
{
    uint16_t len;

    char buf[1024];
    for (len = 0;; len++)
    {
        int c = fgetc(f);
        buf[len] = c;
        if (c == '\0') break;
        if (c == EOF || len == sizeof(buf)) return NULL;
    }

    char *str = malloc(len);
    if (str == NULL) return NULL;
    for (uint16_t i = 0; i < len; i++) *(str+i) = buf[i];
    return str;
}

int meta_attr_parse(FILE *f, struct meta_attr *attr)
{
    attr->key = meta_attr_read(f);
    attr->val = meta_attr_read(f);
    if (attr->key == NULL) return 0;
    if (attr->val == NULL) return 0;
    return 1;
}
