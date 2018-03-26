#ifndef _MAIN_H
#define _MAIN_H

void init_avr(void);
void init_uart(void);
void init_spi(void);

void uart_transmit(uint8_t data);
void uart_transmit_stop(void);
uint8_t spi_receive(void);
void send_to_host(void);

int main(void);

#endif
