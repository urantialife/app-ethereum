#ifndef COMMON_EIP712_H_
#define COMMON_EIP712_H_

#include <stdint.h>
#include <stdbool.h>
#include "ux.h"

bool    handle_sign_712_common_apdu_parse(uint8_t **apdu_buf,
                                          uint8_t *data_length);
unsigned int ui_712_approve_cb(const bagl_element_t *e);
unsigned int ui_712_reject_cb(const bagl_element_t *e);

#endif // COMMON_EIP712_H_
