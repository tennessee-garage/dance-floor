/**
 * Code to drive an ATTiny861a
 *
 * http://www.atmel.com/Images/doc8197.pdf
 *
 * - Drives an RGB LED Strip via PWM
 * - Reads 4 load sensors in a wheatstone bridge configuration via differential ADC
 * - Communicates to a master controller via i2c
 *
 */

#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>
//#include "i2cCommands.h"
#include "spiCommands.h"
#include "main.h"

#define ADC_CONVERSION_DONE() !(ADCSRA & _BV(ADSC))
#define START_ADC_CONVERSION() ADCSRA |= _BV(ADSC)

#define NUM_MEASUREMENTS 10
int8_t measurements[NUM_MEASUREMENTS];

// Store the last value of the ADC/weight sensor value
int8_t adc_value;

// Store the lowest value seen to use as a calibration
int8_t base_adc_value;

uint8_t adc_conversions;

void init_avr() {
    // wait a little before starting setup
    _delay_ms(1000);

    // Set all of port A to input
    DDRA = 0x00;

    // set all of port B to output
    DDRB = 0xFF;
    PORTB = 0x00;

    base_adc_value = 127;
    adc_conversions = 0;
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
    // Timer/Counter0 Control Register B: CS01 & CS00 == clock divided by 64
    TCCR0B = _BV(CS01) | _BV(CS00);

    TCNT0H = 0x00;
    TCNT0L = 0x00;
}

void init_adc(void) {
    // Enable the ADC (ADEN) and set the prescalar (ADPSX) to 128 which will divide the 16Mhz system
    // clock to a reasonable value for the ADC
    ADCSRA = _BV(ADEN) | _BV(ADPS2) | _BV(ADPS1) | _BV(ADPS0);

    // Set bipolar input mode (BIN), 32x gain (GSEL), see below for MUX5 info
    ADCSRB = _BV(BIN) | _BV(GSEL) | _BV(MUX5);

    // 1.1v reference voltage (REFS1), left shift 10bit result (ADLAR),
    // PA5: positive, PA6: negative (MUX5, MUX3, MUX2, see table 15-5 in datasheet)
    ADMUX = _BV(REFS1) | _BV(ADLAR) | _BV(MUX3) | _BV(MUX2);

    // Initialize measurements to zero
    for (int i = 0; i < NUM_MEASUREMENTS; i++) {
        measurements[i] = 0;
    }

    START_ADC_CONVERSION();
}

void add_measurement(int8_t val) {
    int8_t highest = 127;
    int8_t lowest = -127;
    int16_t sum = 0;

    for (int i = NUM_MEASUREMENTS - 1; i > 0; i--) {
        measurements[i] = measurements[i-1];
        if (measurements[i] > highest) {
            highest = measurements[1];
        }
        if (measurements[i] < lowest) {
            lowest = measurements[1];
        }
        sum += measurements[i];
    }

    measurements[0] = val;
    sum += val;
    sum -= highest + lowest;

    adc_value = (int8_t) (sum/8.0);
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

int8_t toSignedInt(uint8_t val) {
    if (0x80 & val) {
        return -1*(adc_value & 0x80) + (adc_value & ~0x80);
    } else {
        return val;
    }
}

int main(void) {
    init_avr();
    //init_pwm();
    //init_timer();
    init_adc();
    init_spi();
    //init_i2c();

    sei();

    while (1) {
        if (ADC_CONVERSION_DONE()) {

            adc_value = toSignedInt(ADCH);

            //add_measurement(toSignedInt(ADCH));

            //if (base_adc_value > adc_value) {
            //    base_adc_value = adc_value;
            //}
            //adc_value -= base_adc_value;

            // Unweighted value is tricky.  The unloaded weight on the test square seems to
            // creep up slowly, so I can't just look for the lowest adc_value as the base
            // value.  I need to find a way to guess when the square is unloaded, some sort
            // of local low.


            //_delay_ms(10);
            START_ADC_CONVERSION();

        }

        handle_spi();
        // handle_i2c();
    }
}
