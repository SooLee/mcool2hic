#!/usr/bin/perl

### WARNING : This code contains some HARDCODED elements - FIX IT ASAP ###


@resolutions = reverse (5000,10000,20000,40000,80000,160000,320000,640000,1280000,2560000,5120000,10240000,2048000);  #### WARNING : HARDCODED ####
@chrlist = map { "chr$_" } (1..22, 'X', 'Y', 'M');  #### WARNING : HARDCODED ####


if(@ARGV<2) { print "usage: $0 file_prefix outfile\n"; exit; }
$file_prefix = shift @ARGV;
$outfile = shift @ARGV;

open FW, ">$outfile";
for $resindex (0..$#resolutions){
  my $file_name = "$file_prefix.$resindex";
  print "$file_name\n";
  open $FH, $file_name;
  my %array=();
  while(<$FH>){
    chomp;
    my ($chr,$val)=(split/\s/)[0,3];
    if($val eq '') { $val=''; }
    elsif($val>0) { $val=1/$val; }
    elsif($val==0) { $val=''; }
    push @{$array{$chr}}, $val;
  }
  close $FH;
  for $chr (@chrlist){
    print FW "vector\tCooler\t$chr\t$resolutions[$resindex]\tBP\n";
    for $i (0..$#{$array{$chr}}){
      if($array{$chr}[$i] eq '') { $array{$chr}[$i]='.'; }
      print FW "$array{$chr}[$i]\n";
    }
  }
}
close FW;

