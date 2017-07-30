/**
 * Test Code to drive an ATTiny861a
 *
 * http://www.atmel.com/Images/doc8197.pdf
 *
 * - Drives an RGB LED Strip via PWM
 *
 */

#include <avr/io.h>
#include <util/delay.h>
#include "main.h"

#define STEP 0.0005

volatile int state = 0;
volatile int direction = 1;

void init_avr() {
    // wait a little before starting setup
    _delay_ms(1000);

    // Set all of port A to input
    DDRA = 0x00;

    // set all of port B to output
    DDRB = 0xFF;
    PORTB = 0x00;
}

void init_pwm(void) {

    // Set low speed mode (LSM) and start the PLL (PLLE)
    PLLCSR = _BV(LSM) | _BV(PLLE);

    while (!(PLLCSR & 1<<PLOCK));

    // Enable PCKE (set all rather than set bit via |= to save space)
    PLLCSR = _BV(LSM) | _BV(PCKE) | _BV(PLLE);

    // COM1A1 COM1A0 COM1B1 COM1B0 FOC1A FOC1B PWM1A PWM1B
    TCCR1A = _BV(COM1A1) | _BV(COM1B1) | _BV(PWM1A) | _BV(PWM1B);

    // prescaler at 64
    TCCR1B = _BV(CS12) | _BV(CS11) | _BV(CS10);

    // COM1A1S COM1A0S COM1B1S COM1B0S COM1D1 COM1D0 FOC1D PWM1D
    TCCR1C = _BV(COM1A1S) | _BV(COM1B1S) | _BV(COM1D1) | _BV(PWM1D);

    // FPIE1 FPEN1 FPNC1 FPES1 FPAC1 FPF1 WGM11 WGM10
    TCCR1D = _BV(WGM10);

    // Clear the compare counter
    TC1H = 0x00;
    TCNT1 = 0x00;

    // Set the top value of the compare count to 1023
    TC1H = 0x03;
    OCR1C = 0xFF;

    // Timer/Counter0 Control Register B: CS01 & CS00 == clock divided by 64
    TCCR0B = _BV(CS01) | _BV(CS00);

    TCNT0H = 0x00;
    TCNT0L = 0x00;

    // Clear the LEDs
    set_green(0);
    set_blue(0);
    set_red(0);
}

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

void set_blue(uint16_t val) {
    TC1H = val >> 8;
    OCR1D = val & 0x0FF;
}

void set_red(uint16_t val) {
    TC1H = val >> 8;
    OCR1A = val & 0x0FF;
}

void set_green(uint16_t val) {
    TC1H = val >> 8;
    OCR1B = val & 0x0FF;
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
    in->h += 0.01;
    in->v = 1.0;

    if (in->h > 360.0) {
        in->h = 0.0;
    }
}

int main(void) {
    init_avr();
    init_pwm();

    hsv currentHSV;
    rgb currentRGB;

    currentHSV.h = 0.0;
    currentHSV.s = 1.0;
    currentHSV.v = 1.0;

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
        set_red((uint16_t) 1024*currentRGB.r);
        set_green((uint16_t) 1024*currentRGB.g);
        set_blue((uint16_t) 1024*currentRGB.b);
    }
}
