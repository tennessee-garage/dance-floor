/**
 *
 */

#include <avr/io.h>
#include <util/delay.h>
#include <stdlib.h>
#include "main.h"

// define baud
#define BAUD 9600

// set baud rate value for UBRR
#define BAUD_RATE (F_CPU/16/BAUD-1)

#define LED_REG DD3
#define LED_PIN PIN3

void init_avr() {
    // Set PD3 to input
    DDRD = _BV(LED_REG);
    PORTD = 0x00;
}

/**
 * Initialize UART
 */
void init_uart() {
    // Set baud rate
    UBRR0H = (BAUD_RATE >> 8);
    UBRR0L = 0xFF & BAUD_RATE;

    // Enable receiver and transmitter
    UCSR0B = _BV(TXEN0) | _BV(RXEN0);

    // 8bit data format
    UCSR0C = _BV(UCSZ00) | _BV(UCSZ01);
}

/**
 * Send one byte of data
 *
 * @param data
 */
void uart_transmit (unsigned char data) {
    // wait while register is free
    while (!(UCSR0A & _BV(UDRE0)));

    // load data in the register
    UDR0 = data;
}

/**
 * Receive one byte of data
 * @return char
 */
unsigned char uart_recieve (void) {
    // wait while data is being received
    while(!(UCSR0A & _BV(RXC0)));

    return UDR0;
}

int main(void) {
    init_avr();
    init_uart();
    char x = 48;

    while (1) {
        _delay_ms(100);
        PORTD |= _BV(LED_PIN);


        uart_transmit(x++);
        if (x > 122) {
            x = 48;
        }

        _delay_ms(100);
        PORTD &= ~_BV(LED_PIN);

        uart_transmit(x++);
        if (x > 122) {
            x = 48;
        }
    }
}
