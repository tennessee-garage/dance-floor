#ifndef _MAIN_H
#define _MAIN_H

typedef struct {
    double r;       // a fraction between 0 and 1
    double g;       // a fraction between 0 and 1
    double b;       // a fraction between 0 and 1
} rgb;

typedef struct {
    double h;       // angle in degrees
    double s;       // a fraction between 0 and 1
    double v;       // a fraction between 0 and 1
} hsv;

void init_avr(void);
void init_pwm(void);

rgb hsv2rgb(hsv *in);

void set_red(uint16_t val);
void set_green(uint16_t val);
void set_blue(uint16_t val);

void phase_red(hsv *in);
void phase_green(hsv *in);
void phase_blue(hsv *in);
void phase_color(hsv *in);
void rotate_full(hsv *in);

int main(void);

#endif
