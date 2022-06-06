#ifndef INT256_H_
#define INT256_H_

#include <stdbool.h>
#include <stdint.h>
#include "uint256.h"

bool tostring256_s(const uint256_t *const number,
                   uint32_t base,
                   char *const out,
                   uint32_t out_length);

#endif  // INT256_H_
