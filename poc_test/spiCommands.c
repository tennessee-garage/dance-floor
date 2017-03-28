/**
 * Handle SPI communication
 *
 * The master sends 3 10-bit LED values per square.  This gives 30 bits so we use 4 bytes for this transfer.
 * The remaining two bits are 00 by default, leaving room for 3 additional commands in the future.  The
 * format of the data is:
 *
 *   From master to slave
 *   byte | 0               1               2               3
 *   bit  | 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0
 *   data | C C R R R R R R R R R R G G G G G G G G G G B B B B B B B B B B
 *
 *   Byte 0
 *   C[7:6] - Commands bits. 00 = read LED values send weight value
 *   R[5:0] - Top 6 red value bits
 *
 *   Byte 1
 *   R[7:4] - Bottom 4 red value bits
 *   G[3:0] - Top 4 green value bits
 *
 *   Byte 2
 *   G[7:2] - Bottom 6 green value bits
 *   B[2:0] - Top 2 blue value bits
 *
 *   Byte 3
 *   B[7:0] - Bottom 8 blue value bits
 *
 *   To master from slave
 *   byte | 0               1               2               3
 *   bit  | 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0
 *   data | 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 W W W W W W W W W W
 *
 *   Bytes 0-1 - Zeros
 *
 *   Byte 2
 *   W[1:0] - Top 2 weight value bits
 *
 *   Byte 3
 *   W[7:0] - Bottom 8 weight value bits
 */

#include <avr/io.h>
#include <avr/interrupt.h>
#include "spiCommands.h"
#include "main.h"

#define LATCH_PIN PORTA3
#define USI_OVERFLOW_VECTOR USI_OVF_vect

// Clear the overflow flag to reset the data transfer buffer
#define CLEAR_OVERFLOW() USISR |= _BV(USIOIF)
#define NOT_IN_OVERFLOW() !(USISR & _BV(USIOIF))

// Clear the counter when chip select goes low
#define CLEAR_USI_COUNTER() USISR &= 0xF0

uint8_t byte_count = 0;
uint8_t buffer[DATA_BYTES];

void init_spi(void) {
    // Enable interrupts with USIOIE, USIWM0 sets 3 wire mode, USICS1 sets an external clock source
    USICR = _BV(USIOIE) | _BV(USIWM0) | _BV(USICS1);
    //USICR = _BV(USIWM0) | _BV(USICS1);

    // Set alternate SPI pins on PORTA (PA0=DI, PA1=DO, PA2=USCK)
    USIPP = _BV(USIPOS);

    // Set PA0 to be an output for the DO SPI function
    DDRA |= _BV(DDA1);

    // Pin Change Interrupt Enable (PCIE1)
    GIMSK |= _BV(PCIE1);

    // Set PCINT3 as an interrupt source (PORTA3)
    PCMSK0 |= _BV(PCINT3);

    for (int i = 0; i < DATA_BYTES; i++) {
        buffer[i] = 0x00;
    }

    byte_count = 0;

    // Clear the overflow flag
    CLEAR_OVERFLOW();
}

void handle_spi(void) {
    //uint8_t val = read_spi();
    //latch_on_chip_select();
}

uint8_t read_spi(void) {
    // Write the value we will send to the master
    //USIDR = adc_value;

    // Clear the overflow flag
    CLEAR_OVERFLOW();

    // Wait for overflow condition
    while (NOT_IN_OVERFLOW());

    // Return the value we got
    return USIBR;
}

ISR( SIG_PIN_CHANGE ) {

    if (PINA & _BV(PINA3)) {
        // If we just went high, load the next value of the ADC
        PORTB |= _BV(PORTB0);

        for (int i = 0; i < DATA_BYTES; i++) {
            buffer[i] = (uint8_t) adc_value;
        }

        // Set byte zero up to be transferred the next time we get SPI activity
        USIDR = buffer[0];
    } else {
        // If we've been selected (PA3 pulled low) clear the counters
        CLEAR_USI_COUNTER();
        CLEAR_OVERFLOW();

        PORTB &= ~_BV(PORTB0);
    }
}

ISR( USI_OVERFLOW_VECTOR ) {
    PORTB |= _BV(PORTB1);

    // Increment byte count since 1 byte has just been received and sent
    byte_count++;

    // Shift the data through the buffer.  We shift to the left since we receive byte 0 first
    // from the master
    //for (int i = 1; i < DATA_BYTES; i++) {
    //    buffer[i-1] = buffer[i];
    //}
    //buffer[DATA_BYTES-1] = USIDR;

    if (byte_count != 0) {
        // If byte_count is non-zero, set the next byte to be transferred
        USIDR = buffer[byte_count];
    }

    PORTB &= ~_BV(PORTB1);

    CLEAR_OVERFLOW();
}

void clear_usi_data_counter(void) {

    USISR &= 0xF0;
}

/**
*   From master to slave
*   byte | 0               1               2               3
*   bit  | 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0
*   data | C C R R R R R R R R R R G G G G G G G G G G B B B B B B B B B B
*/
void latch_on_chip_select(void) {
    // Test if the latch pin is high
    //if (!(PORTA & _BV(LATCH_PIN))) {
    if (byte_count != 3) {
        // The latch pin is not set, return
        return;
    }

    uint16_t val;

    // Take B0 R[5:0] + B1 R[7:4]
    val = ((buffer[0] & 0x3F) << 4) | ((buffer[1] & 0xF0) >> 4);
    set_red(val);

    // Take B1 G[4:0] + B2 G[7:2]
    val = ((buffer[1] & 0x0F) << 6) | ((buffer[2] & 0xFC) >> 2);
    set_green(val);

    // Take B2 B[2:0] + B3 G[7:0]
    val = ((buffer[2] & 0x03) << 8) | buffer[3];
    set_blue(val);

    // Put the current weight value onto the buffer to shift out on the next cycle
    buffer[0] = 0;
    buffer[1] = 0;
    buffer[2] = 0; //base_adc_value;
    buffer[3] = 0x9A; //adc_value;
}