//
// Created by Garth Webb on 6/25/17.
//
#include <stdio.h>

#define STEP 0.01

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

typedef int uint16_t;

volatile int state = 0;
volatile int direction = 1;

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

rgb hsv2rgb(hsv *in) {
    double      hh, p, q, t, ff;
    long        i;
    rgb         out;

    if (in->s <= 0.0) {       // < is bogus, just shuts up warnings
        out.r = in->v;
        out.g = in->v;
        out.b = in->v;
        return out;
    }
    hh = in->h;
    if (hh >= 360.0) hh = 0.0;
    hh /= 60.0;
    i = (long) hh;
    ff = hh - i;
    p = in->v * (1.0 - in->s);
    q = in->v * (1.0 - (in->s * ff));
    t = in->v * (1.0 - (in->s * (1.0 - ff)));

    switch (i) {
        case 0:
            out.r = in->v;
            out.g = t;
            out.b = p;
            break;
        case 1:
            out.r = q;
            out.g = in->v;
            out.b = p;
            break;
        case 2:
            out.r = p;
            out.g = in->v;
            out.b = t;
            break;

        case 3:
            out.r = p;
            out.g = q;
            out.b = in->v;
            break;
        case 4:
            out.r = t;
            out.g = p;
            out.b = in->v;
            break;
        case 5:
        default:
            out.r = in->v;
            out.g = p;
            out.b = q;
            break;
    }
    return out;
}

void phase_red(hsv *in) {
    in->h = 0.0;
    phase_color(in);
}

void phase_green(hsv *in) {
    in->h = 120.0;
    phase_color(in);
}

void phase_blue(hsv *in) {
    in->h = 240.0;
    phase_color(in);
}

void phase_color(hsv *in) {
    in->v += STEP * direction;

    if (in->v > 1.0) {
        in->v = 1.0;
        direction = -1;
    }

    if (in->v < 0.0) {
        in->v = 0.0;
        direction = 1;
        state = (state + 1) % 4;
    }
}

void rotate_full(hsv *in) {
    in->h += 1;
    in->v = 1.0;

    if (in->h > 360.0) {
        in->h -= 360.0;
    }
}

int main(void) {
    hsv currentHSV;
    rgb currentRGB;

    currentHSV.h = 0.0;
    currentHSV.s = 1.0;
    currentHSV.v = 0.0;

    while (1) {
        switch (state) {
            case 0:
                phase_red(&currentHSV);
                break;
            case 1:
                phase_green(&currentHSV);
                break;
            case 2:
                phase_blue(&currentHSV);
                break;
            default:
                rotate_full(&currentHSV);
                break;
        }

        currentRGB = hsv2rgb(&currentHSV);
        printf("RED: %f\n", 1024*currentRGB.r);
        printf("GREEN: %f\n", 1024*currentRGB.g);
        printf("BLUE: %f\n", 1024*currentRGB.b);
    }
}