/**
 * Extremely simple SPI to UART bridge
 *
 * Data is only read from SPI and written to UART.  Any data transmitted
 * via UART is ignored.
 */

#include <avr/io.h>
#include "main.h"

// define baud
//#define BAUD 9600
#define BAUD 57600

// set baud rate value for UBRR
#define BAUD_RATE ((F_CPU/(16L*BAUD))-1L)

#define DDR_SPI DDRB
#define DD_MISO DDB3

void init_avr() {
    // Set PC0 and PC1 as outputs
    DDRC = _BV(DD0) | _BV(DD1);
    PORTC = 0x00;
}

/**
 * Initialize UART
 */
void init_uart() {
    // Set baud rate
    UBRR0H = BAUD_RATE >> 8;
    UBRR0L = BAUD_RATE & 0xFF;

    // Enable receiver and transmitter
    UCSR0B = _BV(TXEN0) | _BV(RXEN0);

    // 8bit data format
    UCSR0C = _BV(UCSZ00) | _BV(UCSZ01);
}

void init_spi() {
    // Set MISO output, all others input
    DDR_SPI = _BV(DD_MISO);

    // Enable SPI
    SPCR = _BV(SPE);
}

/**
 * Send one byte of data
 *
 * @param data
 */
void uart_transmit(uint8_t data) {
    // wait until register is free
    while (!(UCSR0A & _BV(UDRE0)));

    // load data in the register
    UDR0 = data;
}

uint8_t spi_receive() {
    while (!(SPSR & _BV(SPIF)));

    return SPDR;
}

int main() {
    init_avr();
    init_uart();
    init_spi();

    while (1) {
        uart_transmit(spi_receive());
    }
}
