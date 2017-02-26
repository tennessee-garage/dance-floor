#ifndef _MAIN_H
#define _MAIN_H

void init_avr(void);
void init_pwm(void);
void init_timer(void);
void init_adc(void);
void set_red(uint16_t val);
void set_green(uint16_t val);
void set_blue(uint16_t val);
void handle_i2c_command_last(void);
void handle_i2c_command_request_weight(void);
void handle_i2c_command_set_led(void);
void handle_i2c_command(void);
void main(void);

#endif