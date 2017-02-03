#include <avr/io.h>
#include <util/delay.h>

struct RGB_set {
    unsigned char r;
    unsigned char g;
    unsigned char b;
} RGB_set;

struct HSV_set {
    signed int h;
    unsigned char s;
    unsigned char v;
} HSV_set;

void init_avr(void) {
    _delay_ms(1000);	// wait a little before starting setup

    DDRA = 0xff;		// pin for driving blinking led (to see if device freezes or sth)
    PORTA = 0x00;

    DDRB = 0xff;		// set all portb to output
    PORTB = 0x00;
}

void set_red(uint16_t val) {
    TC1H = val >> 8;
    OCR1D = val & 0x0FF;
}

void set_green(uint16_t val) {
    TC1H = val >> 8;
    OCR1A = val & 0x0FF;
}

void set_blue(uint16_t val) {
    TC1H = val >> 8;
    OCR1B = val & 0x0FF;
}

void init_pwm(void) {

    // Set low speed mode and start the PLL
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

    // Clear the LEDs
    set_green(0);
    set_blue(0);
    set_red(0);
}

void init_timer(void) {
    // - - - TSM PSR0 CS02 CS01 CS00
    TCCR0B = _BV(CS01) | _BV(CS00);

    TCNT0H = 0x00;
    TCNT0L = 0x00;
}

void HSV2RGB(struct HSV_set HSV, struct RGB_set *RGB){
    int i;
    float f, p, q, t, h, s, v;

    h=(float)HSV.h;
    s=(float)HSV.s;
    v=(float)HSV.v;

    s /=255;

    if( s == 0 ) { // achromatic (grey)
        RGB->r = RGB->g = RGB->b = v;
        return;
    }

    h /= 60;            // sector 0 to 5
    i = floor( h );
    f = h - i;            // factorial part of h
    p = (unsigned char)(v * ( 1 - s ));
    q = (unsigned char)(v * ( 1 - s * f ));
    t = (unsigned char)(v * ( 1 - s * ( 1 - f ) ));

    switch( i ) {
        case 0:
            RGB->r = v;
            RGB->g = t;
            RGB->b = p;
            break;
        case 1:
            RGB->r = q;
            RGB->g = v;
            RGB->b = p;
            break;
        case 2:
            RGB->r = p;
            RGB->g = v;
            RGB->b = t;
            break;
        case 3:
            RGB->r = p;
            RGB->g = q;
            RGB->b = v;
            break;
        case 4:
            RGB->r = t;
            RGB->g = p;
            RGB->b = v;
            break;
        default:        // case 5:
            RGB->r = v;
            RGB->g = p;
            RGB->b = q;
            break;
    }
}

void main(void) {
    struct RGB_set RGB;
    struct HSV_set HSV;

    HSV.h = 0;
    HSV.s = 255;
    HSV.v = 255;

    init_avr();
    init_pwm();
    init_timer();

#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Wmissing-noreturn"
    while (1) {
/*
        green = (green+1)%1024;
        blue = (blue+1)%1024;
        red = (red+1)%1024;
*/
        _delay_ms(10);

        HSV.h = (HSV.h+1)%360;
        HSV2RGB(HSV, &RGB);

        set_green(RGB.g);
        set_blue(RGB.b);
        set_red(RGB.r);

        _delay_ms(10);
    }
#pragma clang diagnostic pop
}
