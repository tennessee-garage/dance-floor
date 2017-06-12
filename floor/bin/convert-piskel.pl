#!/usr/bin/perl
use strict;
use warnings FATAL => 'all';

use Getopt::Long;
use Data::Dumper;

my ($file);
GetOptions("file|f=s", \$file);

if (! -e $file) {
    die "Can't find file '$file'\n";
}

my $fh;
open($fh, $file) or die "Can't open file '$file': $!\n";

read_to_frames($fh);
my $frames = read_frames($fh);

close($fh);

my $out_file = $file;
$out_file =~ s:([^/]+).c$:$1.py:;
write_floor_file($frames, $out_file);

# =============================================================================

sub read_to_frames {
    my ($fh) = @_;

    # Read lines until we get to the array data
    while (my $line = <$fh>) {
        if ($line =~ /static const uint32_t [^\[]+\[\d+\]\[64\] = {/) {
            return;
        }
    }
}

sub read_frames {
    my ($fh) = @_;
    my @frames;

    while (1) {
        my $f = read_frame($fh);
        if ($f) {
            push @frames, $f;
        } else {
            last;
        }
    }

    return \@frames;
}

sub read_frame {
    my ($fh) = @_;
    my @frame;

    while (my $line = <$fh>) {
        next if $line =~ /^\{/;
        last if $line =~ /^\}/;

        my @values = $line =~ /0x[0-9a-f]{2}([0-9a-f]{6})(?:, )?/g;
        push @frame, @values;
    }

    if (@frame) {
        return \@frame;
    } else {
        return undef;
    }
}

sub write_floor_file {
    my ($frames, $out_file) = @_;

    my $out_fh;
    open($out_fh, "> $out_file") or die "Can't write to file '$out_file': $!\n";

    print $out_fh "\n\ndef anim():\n";
    print $out_fh "    return [\n";

    foreach my $f (@$frames) {
        frame_to_list($out_fh, $f);
    }

    print $out_fh "    ]\n";

    close($out_fh);
}

sub frame_to_list {
    my ($out_fh, $frame) = @_;

    print $out_fh "        [";

    my @tuples;
    foreach my $val (@$frame) {
        my ($b, $g, $r) = $val =~ /([]0-9a-f]{2})([]0-9a-f]{2})([]0-9a-f]{2})/;
        push @tuples, "(".join(', ', hex($r), hex($g), hex($b)).")";
    }
    print $out_fh join(', ', @tuples);

    print $out_fh "],\n";
}
