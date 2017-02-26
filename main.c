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
#include "usiTwiSlave.h"
#include "main.h"

#ifndef SLAVE_ADDRESS
#define SLAVE_ADDRESS 0x26
#endif

#define COMMAND_SET_LED 0x10
#define COMMAND_REQUEST_WEIGHT 0x11
#define COMMAND_LAST 0x12

#define ADC_CONVERSION_DONE() !(ADCSRA & _BV(ADSC))
#define START_ADC_CONVERSION() ADCSRA |= _BV(ADSC)

uint8_t adc_value;
uint8_t last_i2c_command;

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

void init_adc(void) {
    // Enable the ADC and set the prescalar to 128 (divide the 16Mhz system clock to a reasonable
    // value for the ADC
    ADCSRA = _BV(ADEN) | _BV(ADPS2) | _BV(ADPS1) | _BV(ADPS0);

    // Set bipolar input mode
    ADCSRB = _BV(BIN) | _BV(GSEL);

    // PA5: positive, PA6: negative, 20x gain
    ADMUX = _BV(ADLAR) | _BV(MUX4) | _BV(MUX2);

    // Set the "start conversion" bit
    ADCSRA |= _BV(ADSC);
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

void handle_i2c_command_last(void) {
    usiTwiTransmitByte(last_i2c_command);
}

void handle_i2c_command_request_weight(void) {
    usiTwiTransmitByte(adc_value);
}

void handle_i2c_command_set_led(void) {
    uint8_t red = usiTwiReceiveByte();
    uint8_t green = usiTwiReceiveByte();
    uint8_t blue = usiTwiReceiveByte();

    set_red(red);
    set_green(green);
    set_blue(blue);
}

void handle_i2c_command(void) {
    uint8_t command;

    command = usiTwiReceiveByte();

    switch(command) {
        case COMMAND_REQUEST_WEIGHT:
            handle_i2c_command_request_weight();
            break;
        case COMMAND_SET_LED:
            handle_i2c_command_set_led();
            break;
        case COMMAND_LAST:
            handle_i2c_command_last();
            break;
        default:
            break;
    }
    last_i2c_command = command;
}

void main(void) {
    init_avr();
    init_pwm();
    init_timer();
    init_adc();

    sei();

    usiTwiSlaveInit(SLAVE_ADDRESS);

    while (1) {
        if (ADC_CONVERSION_DONE()) {
            adc_value = ADCH;

            START_ADC_CONVERSION();
        }

        if (usiTwiDataInReceiveBuffer()) {
            handle_i2c_command();
        }
    }
}
