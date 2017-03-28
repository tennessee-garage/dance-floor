//
// Created by Garth Webb on 3/18/17.
//

#ifndef DEMO2_SPICOMMANDS_H
#define DEMO2_SPICOMMANDS_H

#include <stdint.h>

// 3 10-bit LED values gives 30 bits.  The leading two bits are 00, leaving room for additional commands
// if necessary.
#define DATA_BYTES 4

extern uint8_t byte_count;
extern uint8_t buffer[DATA_BYTES];

void init_spi(void);
void handle_spi(void);
uint8_t read_spi(void);
void latch_on_chip_select(void);

#endif //DEMO2_SPICOMMANDS_H

