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
#include <avr/interrupt.h>
#include <util/delay.h>
#include "main.h"

#define ADC_CONVERSION_DONE() !(ADCSRA & _BV(ADSC))
#define START_ADC_CONVERSION() ADCSRA |= _BV(ADSC)

// Clear the overflow flag after reading data from an SPI transfer
#define CLEAR_OVERFLOW() USISR |= _BV(USIOIF)

// Clear the USI counter to make sure we are ready for the next transfer (e.g. and don't have extra bits in the buffer)
#define RESET_USI_COUNTER() USISR &= ~_BV(USICNT0) & ~_BV(USICNT1) & ~_BV(USICNT2) & ~_BV(USICNT3)

// Test whether the overflow condition has happened
#define IN_OVERFLOW() (USISR & _BV(USIOIF))
#define NOT_IN_OVERFLOW() !IN_OVERFLOW()

#define CHIP_SELECT_PIN    PINA3
#define CHIP_SELECT_PORTIN PINA
#define CHIP_SELECT_MASK   _BV(CHIP_SELECT_PIN)

// Read the value off the chip select
#define CHIP_SELECT() (CHIP_SELECT_PORTIN & CHIP_SELECT_MASK)
#define IS_CHIP_SELECTED() (CHIP_SELECT() == 0)
#define IS_CHIP_UNSELECTED() (CHIP_SELECT() == 1)

// Pull 10-bit values
#define DECODE_RED(byte1, byte2) ((((byte1) & 0x3F) << 4) | ((byte2) >> 4))
#define DECODE_GREEN(byte1, byte2) ((((byte1) & 0x0F) << 6) | ((byte2) >> 2))
#define DECODE_BLUE(byte1, byte2) ((((byte1) & 0x03) << 8) | (byte2))

// Each packet transmitted has 4 bytes.  The dance floor has 64 squares so will need
// to have 64 packets sent to set LED values.  Using 96 to give some extra room
#define DATA_BYTES 4
#define MAX_PACKETS 96
#define BUFFER_SIZE (DATA_BYTES * MAX_PACKETS)

// Hold the data being piped through the squares
uint8_t buffer[BUFFER_SIZE];

void init_avr() {
    // Set all of port A to input
    DDRA = 0x00;

    // pull up on the chip select pin
    PORTA |= _BV(PA3);

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

    // Light the Green LEDs
    set_green(1023);
    set_blue(0);
    set_red(0);

    _delay_ms(1000);

    // Light the Blue LEDs
    set_green(0);
    set_blue(1023);
    set_red(0);

    _delay_ms(1000);

    // Light the Red LEDs
    set_green(0);
    set_blue(0);
    set_red(1023);

    _delay_ms(1000);

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
    // USIWM0 sets 3 wire mode, USICS1 sets an external clock source, and enable USI overflow interrupt
    USICR = _BV(USIWM0) | _BV(USICS1) | _BV(USIOIE);

    // Set alternate SPI pins on PORTA (PA0=DI, PA1=DO, PA2=USCK)
    USIPP = _BV(USIPOS);

    // Set PA1 to be an output for the DO SPI function
    DDRA |= _BV(DDA1);

    // Clear the data register
    USIDR = 0x00;

    // Clear the input buffer
    for (int i = 0; i < BUFFER_SIZE; i++) {
        buffer[i] = 0x00;
    }

    // Clear the overflow flag
    CLEAR_OVERFLOW();

    // Enable pin change interrupt group 0 (PINA)
    GIMSK |= _BV(PCIE0);
    // Enable interrupt on PINA3 (/CS)
    PCMSK0 |= CHIP_SELECT_MASK;

    sei(); 
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


uint8_t data_transferred = 0;

/*
ISR(USI_OVF_vect)
{
    set_red(1023);
    set_red(0);
    CLEAR_OVERFLOW();
}

ISR(PCINT_vect)
{
    if (IS_CHIP_UNSELECTED()) {
        data_transferred = 1;
        set_green(1023);
        set_red(1023);
        set_green(0);
        set_red(0);
    }
}
    */

uint16_t buffer_head = 4;
ISR(USI_OVF_vect) {
    // Load the byte we got and immediately write out the next byte to send
    uint8_t val_in = USIDR;
    USIDR = buffer[buffer_head-3];
    CLEAR_OVERFLOW();

    buffer[buffer_head] = val_in;

    // Increment the head of the buffer to point to the next byte to write to.  If for some
    // reason we are about to overrun the buffer, keep us 4 bytes from the end, so we just cycle
    // through with a full window until the data stops.
    buffer_head++;
    if (buffer_head >= BUFFER_SIZE) {
        buffer_head = BUFFER_SIZE - 4;
    }

    //set_red(1023);
    //set_red(0);
}

ISR(PCINT_vect) {
    // Check if CS pin has gone HIGH (chip unselected)
    if (IS_CHIP_UNSELECTED()) {
        data_transferred = 1;
        // Paranoid guard against partial data
        RESET_USI_COUNTER();

        //set_blue(1023);
        //set_blue(0);
    
    }
}

uint8_t in_select = 0;
void handle_spi(void) {

    if (IS_CHIP_SELECTED()) {
        in_select = 1;
        set_blue(1023);
    } else {
        set_blue(0);
        if (in_select == 1) {
            in_select = 0;
            data_transferred = 1;
        }
    }

    if (data_transferred) {

        set_green(1023);
        //_delay_ms(500);
        set_green(0);

        data_transferred = 0;

        // The value of head is incremented after the last byte is written, so our data starts at head - 1
        uint16_t red = DECODE_RED(buffer[buffer_head-4], buffer[buffer_head-3]);
        uint16_t green = DECODE_GREEN(buffer[buffer_head-3], buffer[buffer_head-2]);
        uint16_t blue = DECODE_BLUE(buffer[buffer_head-2], buffer[buffer_head-1]);

        set_red(red);
        set_green(green);
        set_blue(blue);
    }
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

        START_ADC_CONVERSION();
    }
}

int main(void) {
    init_avr();
    init_pwm();
    init_adc();
    init_spi();

    while (1) {
        handle_spi();
        handle_adc();
    }
}
