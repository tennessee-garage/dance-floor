#!/usr/bin/perl -w

# Script to generate the dance floor tiles as a layout for openpixelcontrol
#
# The floor is 8 x 8, with 15" x 15" squares.

use strict;
use warnings;

my $SQUARE_SIDE = .5;

print "[\n";

my @out;

foreach my $x (0 .. 7) {
    foreach my $y (0 .. 7) {
        my $center_x = ($SQUARE_SIDE/2) + ($x*$SQUARE_SIDE);
        my $center_y = ($SQUARE_SIDE/2) + ($y*$SQUARE_SIDE);

        push @out, sprintf("{\"point\": [%f, %f, %f]}", $center_x , $center_y, 0);
    }
}

print join(",\n", @out);

print "]\n";
