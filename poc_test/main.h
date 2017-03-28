#ifndef _MAIN_H
#define _MAIN_H

extern int8_t adc_value;
extern int8_t base_adc_value;
extern uint8_t adc_conversions;

void init_avr(void);
void init_pwm(void);
void init_timer(void);
void init_adc(void);
void set_red(uint16_t val);
void set_green(uint16_t val);
void set_blue(uint16_t val);
int main(void);

#endif