#!/opt/local/bin/perl -w

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
foreach my $letter ("a".."z", "A".."Z", "0".."9") {
    my $data = convert_char($letter);
    push @chars, inflate_char($letter, $data);
}

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
        }
        push @lines, "(".join(", ", @line).")";
    }

    return "        '$letter': (\n" .
           "            $width,\n" .
           "            ".join(",\n            ", @lines) . "\n" .
           "        )";
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