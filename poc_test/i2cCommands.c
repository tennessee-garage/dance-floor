/**
 * Handles I2C functions using the usiTwiSlave library to communicate
 */

#include <stdint.h>
#include "usiTwiSlave.h"
#include "main.h"

#ifndef SLAVE_ADDRESS
#define SLAVE_ADDRESS 0x26
#endif

#define COMMAND_SET_LED 0x10
#define COMMAND_REQUEST_WEIGHT 0x11
#define COMMAND_LAST 0x12
#define COMMAND_REQUEST_BASE_WEIGHT 0x13

// Keep track of the last i2c command seen (debugging)
uint8_t last_i2c_command;

void init_i2c(void) {
    usiTwiSlaveInit(SLAVE_ADDRESS);
}

void handle_i2c_command_last(void) {
    usiTwiTransmitByte(last_i2c_command);
}

void handle_i2c_command_request_weight(void) {
    usiTwiTransmitByte((uint8_t) adc_value);
}

void handle_i2c_command_request_base_weight(void) {
    usiTwiTransmitByte((uint8_t) base_adc_value);
}

void handle_i2c_command_set_led(void) {
    uint8_t red = usiTwiReceiveByte();
    uint8_t green = usiTwiReceiveByte();
    uint8_t blue = usiTwiReceiveByte();

    set_red(red);
    set_green(green);
    set_blue(blue);
}

void handle_i2c_command(void) {
    uint8_t command;

    command = usiTwiReceiveByte();

    switch(command) {
        case COMMAND_REQUEST_WEIGHT:
            handle_i2c_command_request_weight();
            break;
        case COMMAND_REQUEST_BASE_WEIGHT:
            handle_i2c_command_request_base_weight();
            break;
        case COMMAND_SET_LED:
            handle_i2c_command_set_led();
            break;
        case COMMAND_LAST:
            handle_i2c_command_last();
            break;
        default:
            break;
    }
    last_i2c_command = command;
}

void handle_i2c(void) {
    if (usiTwiDataInReceiveBuffer()) {
        handle_i2c_command();
    }
}