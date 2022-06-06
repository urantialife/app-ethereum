#include <string.h>
#include "int256.h"
#include "uint_common.h"

/**
 * Format a uint256_t into a string as a signed integer
 *
 * @param[in] number the number to format
 * @param[in] base the radix used in formatting
 * @param[out] out the output buffer
 * @param[in] out_length the length of the output buffer
 * @return whether the formatting was successful or not
 */
bool tostring256_s(const uint256_t *const number,
                   uint32_t base,
                   char *const out,
                   uint32_t out_length) {
    uint256_t max_unsigned_val;
    uint256_t max_signed_val;
    uint256_t one_val;
    uint256_t two_val;
    uint256_t tmp;

    // showing negative numbers only really makes sense in base 10
    if (base == 10) {
        explicit_bzero(&one_val, sizeof(one_val));
        LOWER(LOWER(one_val)) = 1;
        explicit_bzero(&two_val, sizeof(two_val));
        LOWER(LOWER(two_val)) = 2;

        memset(&max_unsigned_val, 0xFF, sizeof(max_unsigned_val));
        divmod256(&max_unsigned_val, &two_val, &max_signed_val, &tmp);
        if (gt256(number, &max_signed_val))  // negative value
        {
            sub256(&max_unsigned_val, number, &tmp);
            add256(&tmp, &one_val, &tmp);
            out[0] = '-';
            return tostring256(&tmp, base, out + 1, out_length - 1);
        }
    }
    return tostring256(number, base, out, out_length);  // positive value
}
