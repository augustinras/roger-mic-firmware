#ifndef SQUIRE_WAKE_FEEDBACK_H
#define SQUIRE_WAKE_FEEDBACK_H
#include <stdbool.h>
#include <stdint.h>

/* Solid green for six seconds, including while on the charger.
 * Unsigned elapsed time stays correct across the 32-bit uptime wrap. */
static inline int squire_wake_phase(uint32_t now, uint32_t started, bool connected, bool off)
{
    uint32_t elapsed = now - started;
    if (!connected || off || elapsed >= 6000U) {
        return -1;
    }
    return 1;
}
void squire_wake_feedback_start(void);
#endif
