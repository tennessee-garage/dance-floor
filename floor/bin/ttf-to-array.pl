#!/opt/local/bin/perl -w
#
# A script that takes a true type font file and outputs a Python file containing a data structure
# holding the bitmap version of that font.  Usage is:
#
#    ./ttf-to-array.pl --file /path/to/truetype.ttf > processor/fonts/font_name.py
#
# This can be used by processors to display text.  For an example, see message.py
#

use strict;
use warnings;

use Getopt::Long;

my $file;
GetOptions("file=s" => \$file);

if (! -e $file) {
    die "TTF file '$file' does not exist\n";
}

my $convert_tmpl = "convert -font $file -pointsize 8 label:%s xbm:-";

my @chars;
foreach my $letter ("a".."z", "A".."Z", "0".."9", ",", ".", "-", "_", "!") {
    my $data = convert_char($letter);
    push @chars, inflate_char($letter, $data);
}
push @chars, space_char();

print "\n\ndef alpha():\n";
print "    return {\n";
print join(",\n", @chars)."\n";
print "    }\n";

sub convert_char {
    my ($char) = @_;
    my $convert = sprintf($convert_tmpl, $char);
    my $pipe;
    my @data;

    open($pipe, "$convert|") or die "Can't exec '$convert': $!\n";
    while (my $line = <$pipe>) {
        next unless $line =~ /^\s+([^}]+)/;

        @data = map { s/^\s+|\s+$//g; hex($_) } (split(",", $1))[0..7];
    }

    return \@data;
}

sub inflate_char {
    my ($letter, $data) = @_;
    my $width = find_width($data);
    my @lines;

    foreach my $row (@$data) {
        my @line;
        for my $y (0..$width) {
            my $mask = 1 << $y;

            if ($mask & $row) {
                push @line, 1;
            } else {
                push @line, 0;
            }

            # If this is a single pixel wide (e.g. "!" or similar) then add a trailing
            # comma to make it a python tuple.  Python why you gotta be so cray?
            if ($width == 0) {
                $line[-1] .= ',';
            }
        }
        push @lines, "(".join(", ", @line).")";
    }

    return "        '$letter': (\n" .
           "            ".join(",\n            ", @lines) . "\n" .
           "        )";
}

sub space_char {
    return "
        ' ': (
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0)
        )
    "
}

sub find_width {
    my ($data) = @_;
    my $max = 0;

    foreach my $row (@$data) {
        next unless $row > 0;

        # The closest power of 2 will give us the highest bit set.  This is the width
        my $len = int(log($row)/log(2));
        if ($len > $max) {
            $max = $len;
        }
    }

    return $max;
}