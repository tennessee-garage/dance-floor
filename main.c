#include <avr/io.h>
#include <util/delay.h>

/*
struct RGB_set {
    unsigned int r;
    unsigned int g;
    unsigned int b;
} RGB_set;

struct HSV_set {
    unsigned int h;
    unsigned int s;
    unsigned int v;
} HSV_set;
*/
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

// OCR1C Sets the top compare value used to clear the ORC1A/B/D registers
void set_top_compare(int val) {
    TC1H = val >> 8;
    OCR1C = val & 0x0FF;
}

void set_red(int val) {
    TC1H = val >> 8;
    OCR1D = val & 0x0FF;
}

void set_green(int val) {
    TC1H = val >> 8;
    OCR1A = val & 0x0FF;
}

void set_blue(int val) {
    TC1H = val >> 8;
    OCR1B = val & 0x0FF;
}

void init_pwm(void) {

    PLLCSR =  0x82;      // LSM for PLL & enable PLL
    while (!(PLLCSR & 1<<PLOCK));
    PLLCSR = 0x86;         // LSM for PLL, PLL enable PCKE

    //TCCR1A
    // COM1A1 COM1A0 COM1B1 COM1B0 FOC1A FOC1B PWM1A PWM1B
    //TCCR1A = 0b00100001;	// enable PWM1B
    TCCR1A = 0b10100011;

    //TCCR1C
    // COM1A1S COM1A0S COM1B1S COM1B0S COM1D1 COM1D0 FOC1D PWM1D
    TCCR1C = 0b10101001;	// enable PWM1D

    //TCCR1D
    // FPIE1 FPEN1 FPNC1 FPES1 FPAC1 FPF1 WGM11 WGM10
    TCCR1D = 0b00000001;

    TC1H = 0x00;
    TCNT1 = 0x00;

    set_green(0);
    set_blue(0);
    set_red(0);

    set_top_compare(1023);

    //DT1=0x00;
    TCCR1B |= (1 << CS12) | (1 << CS11) | (1 << CS10);	// prescaler 64
}

void init_timer(void) {

    // init timer
    // prescaler 64

    //TCCR0A
    // TCW0 ICEN0 ICNC0 ICES0 ACIC0 â€“ â€“ CTC0

    //TCCR0B
    // â€“ â€“ â€“ TSM PSR0 CS02 CS01 CS01
    TCCR0B = 0b00000011;

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
}
