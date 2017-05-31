#!/usr/bin/perl -w

# Script to generate the dance floor tiles as a layout for openpixelcontrol
#
# The floor is 8 x 8, with 15" x 15" squares.
#
# Each strip has 15 lights that are 17mm (0.67in) apart
# Each strip is (15" - 1")/2 == 7" from the center

my $SQUARE_SIDE = 15;
my $OFFSET = 0.5;
my $LED_SPACING = 0.67;
my $LEDS_PER_SIDE = 15;

print "[\n";

my @out;

foreach my $x (0 .. 7) {
    foreach my $y (0 .. 7) {
	my $center_x = ($SQUARE_SIDE/2) + ($x*$SQUARE_SIDE);
	my $center_y = ($SQUARE_SIDE/2) + ($y*$SQUARE_SIDE);
	push @out, create_square($center_x, $center_y);
    }
}

print join(",\n", @out);

print "]\n";

sub create_square {
    my ($center_x, $center_y) = @_;
    my ($x, $y);
    my @out;

    # output top side
    $x = $center_x - int($LEDS_PER_SIDE/2)*$LED_SPACING; 
    $y = $center_y - int($LEDS_PER_SIDE/2);
    foreach my $led (0..14) {
        push @out, sprintf("{\"point\": [%f, %f, %f]}", $x + $led*$LED_SPACING, $y, 0); 
    }

    # output right side
    $x = $center_x + int($LEDS_PER_SIDE/2)*$LED_SPACING; 
    $y = $center_y - int($LEDS_PER_SIDE/2);
    foreach my $led (0..14) {
        push @out, sprintf("{\"point\": [%f, %f, %f]}", $x, $y + $led*$LED_SPACING, 0); 
    }

    # output bottom side
    $x = $center_x - int($LEDS_PER_SIDE/2)*$LED_SPACING; 
    $y = $center_y + int($LEDS_PER_SIDE/2);
    foreach my $led (0..14) {
        push @out, sprintf("{\"point\": [%f, %f, %f]}", $x + $led*$LED_SPACING, $y, 0); 
    }

    # output left side
    $x = $center_x - int($LEDS_PER_SIDE/2)*$LED_SPACING; 
    $y = $center_y - int($LEDS_PER_SIDE/2);
    foreach my $led (0..14) {
        push @out, sprintf("{\"point\": [%f, %f, %f]}", $x, $y + $led*$LED_SPACING, 0); 
    }

    return join(",\n", @out);
}
