#ifndef _MAIN_H
#define _MAIN_H

void init_avr(void);
void init_pwm(void);
void init_adc(void);
void set_red(uint16_t val);
void set_green(uint16_t val);
void set_blue(uint16_t val);
void handle_spi(void);
void handle_adc(void);
int main(void);

#endif
