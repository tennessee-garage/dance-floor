/**
 *
 */

#include <avr/io.h>
#include <util/delay.h>
#include "main.h"

// define baud
//#define BAUD 9600
#define BAUD 57600

// set baud rate value for UBRR
#define BAUD_RATE ((F_CPU/(16*BAUD))-1)

#define PWR_LED PIN0
#define TX_LED PIN1

#define POWER_LED_ON PORTC |= _BV(PWR_LED)
#define POWER_LED_OFF PORTC &= ~_BV(PWR_LED)

#define TX_LED_ON PORTC |= _BV(TX_LED)
#define TX_LED_OFF PORTC &= ~_BV(TX_LED)

#define DDR_SPI DDRB
#define DD_MISO DDB3

// Read the value off the chip select
#define CHIP_SELECT() (PINB & _BV(PINB2))
#define IS_CHIP_SELECTED() (CHIP_SELECT() == 0)

// Each packet received has 4 bytes.  The dance floor has 64 squares so will send 64 packets
// of weight values * 4 byes == 256 bytes.  Using 96 packets to give some extra room
#define DATA_BYTES 4
#define MAX_PACKETS 96

// Hold the data being piped through the squares
uint8_t buffer[DATA_BYTES * MAX_PACKETS];
// Keep track of where we're at in the buffer
uint16_t head;

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
    UBRR0H = 16 >> 8; // BAUD_RATE >> 8;
    UBRR0L = 0xFF & 16; // BAUD_RATE;

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

    for (int i = 0; i < DATA_BYTES * MAX_PACKETS; i++) {
        buffer[i] = 0x00;
    }
    head = 0;
}

/**
 * Send one byte of data
 *
 * @param data
 */
void uart_transmit(unsigned char data) {
    // wait while register is free
    while (!(UCSR0A & _BV(UDRE0)));

    // load data in the register
    UDR0 = data;
}

void spi_receive() {
    head = 0;

    // Block until some data comes our way
    while (!IS_CHIP_SELECTED());

    // Once the data comes, keep reading until it stops
    while (IS_CHIP_SELECTED()) {
        // Wait for reception to complete, but don't get hung here if chip select is no longer active
        while (!(SPSR & _BV(SPIF)) && IS_CHIP_SELECTED());

        // Make sure we left the loop above because data arrived
        if (IS_CHIP_SELECTED()) {
            buffer[head++] = SPDR;
        }
    }
}

void send_to_host() {
    for (int i = 0; i < head; i++) {
        uart_transmit(buffer[i]);
    }
    uart_transmit_stop();
}

void uart_transmit_stop() {
    // Data received is always 4 bytes, but only the first two bytes ever have data.  Transmit
    // any understood 4 byte pattern to signal the end of the transmission
    uart_transmit('s');
    uart_transmit('t');
    uart_transmit('o');
    uart_transmit('p');
}

int main() {
    init_avr();
    init_uart();
    init_spi();

    POWER_LED_ON;

    while (1) {
        spi_receive();

        TX_LED_ON;
        send_to_host();
        TX_LED_OFF;
    }
}
