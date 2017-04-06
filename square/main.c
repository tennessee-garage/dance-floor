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
#include "main.h"

#define ADC_CONVERSION_DONE() !(ADCSRA & _BV(ADSC))
#define START_ADC_CONVERSION() ADCSRA |= _BV(ADSC)

// Clear the overflow flag after reading data from an SPI transfer
#define CLEAR_OVERFLOW() USISR |= _BV(USIOIF)

// Test whether the overflow condition has happened
#define IN_OVERFLOW() (USISR & _BV(USIOIF))
#define NOT_IN_OVERFLOW() !IN_OVERFLOW()

// Read the value off the chip select
#define CHIP_SELECT() (PINA & _BV(PINA3))
#define IS_CHIP_SELECTED() (CHIP_SELECT() == 0)

// Pull 10-bit values
#define DECODE_RED(byte1, byte2) (((byte1 & 0x3F) << 4) | (byte2 >> 4))
#define DECODE_GREEN(byte1, byte2) (((byte1 & 0x0F) << 6) | (byte2 >> 2))
#define DECODE_BLUE(byte1, byte2) (((byte1 & 0x03) << 8) | byte2)

// Each packet transmitted has 4 bytes.  The dance floor has 64 squares so will need
// to have 64 packets sent to set LED values.  Using 96 to give some extra room
#define DATA_BYTES 4
#define MAX_PACKETS 96

// Hold the data being piped through the squares
uint8_t buffer[DATA_BYTES * MAX_PACKETS];
// Keep track of where we're at in the buffer
uint8_t head;

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

void init_adc(void) {
    // Enable the ADC (ADEN) and set the prescalar (ADPSX) to 128 which will divide the 16Mhz system
    // clock to a reasonable value for the ADC
    ADCSRA = _BV(ADEN) | _BV(ADPS2) | _BV(ADPS1) | _BV(ADPS0);

    // Set bipolar input mode (BIN), 32x gain (GSEL), see below for MUX5 info
    ADCSRB = _BV(BIN) | _BV(GSEL) | _BV(MUX5);

    // 1.1v reference voltage (REFS1),
    // PA5: positive, PA6: negative (MUX5, MUX3, MUX2, see table 15-5 in datasheet)
    ADMUX = _BV(REFS1) | _BV(MUX3) | _BV(MUX2);

    START_ADC_CONVERSION();
}

void init_spi(void) {
    // USIWM0 sets 3 wire mode, USICS1 sets an external clock source
    USICR = _BV(USIWM0) | _BV(USICS1);

    // Set alternate SPI pins on PORTA (PA0=DI, PA1=DO, PA2=USCK)
    USIPP = _BV(USIPOS);

    // Set PA0 to be an output for the DO SPI function
    DDRA |= _BV(DDA1);

    for (int i = 0; i < DATA_BYTES * MAX_PACKETS; i++) {
        buffer[i] = 0x00;
    }
    head = 0;

    // Clear the overflow flag
    CLEAR_OVERFLOW();
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

void handle_spi(void) {
    uint8_t transferred = 0;

    // If we're selected
    while (IS_CHIP_SELECTED()) {
        transferred = 1;

        // Wait for bytes to be read in, at which point overflow will trigger
        while (NOT_IN_OVERFLOW() && IS_CHIP_SELECTED());

        // Write the value we got to the head of the fifo, and read the tail to sent forward
        buffer[head] = USIDR;
        USIDR = buffer[head-3];

        head++;

        CLEAR_OVERFLOW();
    }

    // If we didn't just transfer some bytes, don't decode and set LEDs
    if (!transferred) {
        return;
    }

    // The value of head is incremented after the last byte is written, and then incremented again when
    // chip select goes high (not selected) for this reason the last byte written is at head - 2
    uint16_t red = DECODE_RED(buffer[head-5], buffer[head-4]);
    uint16_t green = DECODE_GREEN(buffer[head-4], buffer[head-3]);
    uint16_t blue = DECODE_BLUE(buffer[head-3], buffer[head-2]);

    set_red(red);
    set_green(green);
    set_blue(blue);

    // Keep the head at 4 so we don't start overwriting the weight with color
    // values when there's no ADC conversion ready
    head = 4;
}

void handle_adc(void) {

    if (ADC_CONVERSION_DONE()) {
        // These MUST be read in this order, ADCL then ADCH "to ensure that the
        // content of the data registers belongs to the same conversion"
        buffer[1] = ADCL;
        buffer[0] = ADCH;

        buffer[2] = 0;
        buffer[3] = 0;

        // Ready the first byte for the next transfer
        USIDR = buffer[0];
        head = 4;

        START_ADC_CONVERSION();
    }
}

int main(void) {
    init_avr();
    init_pwm();
    init_adc();
    init_spi();

    while (1) {
        handle_adc();
        handle_spi();
    }
}
