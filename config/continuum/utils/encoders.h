/*
 * Shared helper macros for matrices that expose:
 * - JS0..JS4  : 5-way joystick directions + center
 * - LEC       : encoder click key position
 *
 * Override any *_BINDING macro before including this file when you need
 * different behavior per keyboard/keymap.
 */

/* Joystick + encoder-click default key bindings. */
#ifndef JS0_BINDING
#define JS0_BINDING &kp UP
#endif

#ifndef JS1_BINDING
#define JS1_BINDING &kp LEFT
#endif

#ifndef JS2_BINDING
#define JS2_BINDING &kp ENTER
#endif

#ifndef JS3_BINDING
#define JS3_BINDING &kp RIGHT
#endif

#ifndef JS4_BINDING
#define JS4_BINDING &kp DOWN
#endif

/*
 * Key binding helper for encoder click positions.
 * Example: LEC_BINDING(C_MUTE) &kp C_MUTE
 */
#define LEC_BINDING(binding) binding

/*
 * Key binding helper for encoder click positions.
 * Example: REC_BINDING(SPACE) &kp SPACE
 */
#define REC_BINDING(binding) binding

/*
 * Sensor helper for ZMK_LAYER(..., sensors) payload.
 * Example: sensor-bindings = <SENSOR_BINDING(C_VOL_UP, C_VOL_DN)>;
 */
#define SENSOR_BINDING(clockwise, counter_clockwise) \
    &inc_dec_kp clockwise counter_clockwise

/* Common presets for convenience. */
#define SENSOR_VOLUME_BINDING SENSOR_BINDING(C_VOL_UP, C_VOL_DN)
#define SENSOR_PAGE_BINDING SENSOR_BINDING(PG_UP, PG_DN)
#define SENSOR_SCROLL_BINDING SENSOR_BINDING(C_AC_SCROLL_UP, C_AC_SCROLL_DOWN)
#define SENSOR_FR_BINDING SENSOR_BINDING(C_FAST_FORWARD, C_REWIND)
#define SENSOR_NP_BINDING SENSOR_BINDING(C_NEXT, C_PREV)