#ifndef _MAIN_H
#define _MAIN_H

void init_avr(void);
void init_uart(void);
void init_spi(void);

void uart_transmit (unsigned char data);
void uart_transmit_stop(void);
void spi_receive(void);
void send_to_host(void);

int main(void);

#endif
