#!/usr/bin/perl
my $what = $ARGV[0] or die "Need argument";
my $cmd = "grep '$what' farg/*.py farg/*/*.py farg/*/*/*.py farg/*/*/*/*.py farg/*/*/*/*/*.py tests/*.py tests/*/*.py";
system $cmd;
