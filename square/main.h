#ifndef _MAIN_H
#define _MAIN_H

#define SET_PA0() SET_PIN(PORTA, PA0)
#define SET_PA1() SET_PIN(PORTA, PA1)
#define SET_PA2() SET_PIN(PORTA, PA2)
#define SET_PA3() SET_PIN(PORTA, PA3)
#define SET_PA4() SET_PIN(PORTA, PA4)
#define SET_PA5() SET_PIN(PORTA, PA5)
#define SET_PA6() SET_PIN(PORTA, PA6)
#define SET_PA7() SET_PIN(PORTA, PA7)
#define CLEAR_PA0() CLEAR_PIN(PORTA, PA0)
#define CLEAR_PA1() CLEAR_PIN(PORTA, PA1)
#define CLEAR_PA2() CLEAR_PIN(PORTA, PA2)
#define CLEAR_PA3() CLEAR_PIN(PORTA, PA3)
#define CLEAR_PA4() CLEAR_PIN(PORTA, PA4)
#define CLEAR_PA5() CLEAR_PIN(PORTA, PA5)
#define CLEAR_PA6() CLEAR_PIN(PORTA, PA6)
#define CLEAR_PA7() CLEAR_PIN(PORTA, PA7)

#define SET_PB0() SET_PIN(PORTB, PB0)
#define SET_PB1() SET_PIN(PORTB, PB1)
#define SET_PB2() SET_PIN(PORTB, PB2)
#define SET_PB3() SET_PIN(PORTB, PB3)
#define SET_PB4() SET_PIN(PORTB, PB4)
#define SET_PB5() SET_PIN(PORTB, PB5)
#define SET_PB6() SET_PIN(PORTB, PB6)
#define SET_PB7() SET_PIN(PORTB, PB7)
#define CLEAR_PB0() CLEAR_PIN(PORTB, PB0)
#define CLEAR_PB1() CLEAR_PIN(PORTB, PB1)
#define CLEAR_PB2() CLEAR_PIN(PORTB, PB2)
#define CLEAR_PB3() CLEAR_PIN(PORTB, PB3)
#define CLEAR_PB4() CLEAR_PIN(PORTB, PB4)
#define CLEAR_PB5() CLEAR_PIN(PORTB, PB5)
#define CLEAR_PB6() CLEAR_PIN(PORTB, PB6)
#define CLEAR_PB7() CLEAR_PIN(PORTB, PB7)

#define SET_PIN(port, pin) port |= _BV(pin)
#define CLEAR_PIN(port, pin) port &= ~_BV(pin)

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
