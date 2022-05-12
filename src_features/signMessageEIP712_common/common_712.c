#include "shared_context.h"
#include "common_712.h"

bool    handle_sign_712_common_apdu_parse(uint8_t **apdu_buf,
                                          uint8_t *data_length)
{
    if (*data_length < 1)
    {
        PRINTF("Invalid data\n");
        return false;
    }
    tmpCtx.messageSigningContext712.pathLength = (*apdu_buf)[0];
    if ((tmpCtx.messageSigningContext712.pathLength < 0x01) ||
        (tmpCtx.messageSigningContext712.pathLength > MAX_BIP32_PATH))
    {
        PRINTF("Invalid path\n");
        return false;
    }
    *apdu_buf += 1;
    *data_length -= 1;
    for (uint8_t i = 0; i < tmpCtx.messageSigningContext712.pathLength; ++i)
    {
        if (*data_length < sizeof(uint32_t))
        {
            PRINTF("Invalid data\n");
            return false;
        }
        tmpCtx.messageSigningContext712.bip32Path[i] = U4BE(*apdu_buf, 0);
        *apdu_buf += sizeof(uint32_t);
        *data_length -= sizeof(uint32_t);
    }
    return true;
}
