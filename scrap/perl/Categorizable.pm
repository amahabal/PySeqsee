package Categorizable;
use 5.010;
use Moose::Role;

sub get_categories {
  my ($self) = @_;
  return [ map { $category_registry{$_} } $self->category_list_as_strings ];
}

sub get_common_categories {
  my @objects = @_;
  my $count   = scalar(@objects);

  my %key_count;
  for my $object (@objects) {
    confess "Funny arg $object" unless ref($object);
    my @categories_for_object = $object->category_list_as_strings;
    $key_count{$_}++ for @categories_for_object;
  }

  my @common_strings = grep { $key_count{$_} == $count } keys %key_count;
  return map {
    $category_registry{$_}
    or confess "not a cat: $_\ncats known:\n"
    . join( ', ', %category_registry )
  } @common_strings;
}

sub HasNonAdHocCategory {
  my ($item) = @_;
  for ( $item->category_list_as_strings ) {
    return 1 unless $_ =~ m#Interlaced#;
  }
  return 0;
}

sub CopyCategoriesTo {
  my ( $from, $to ) = @_;
  my $any_failure_so_far;
  for my $category ( @{ $from->get_categories() } ) {
    my $bindings;
    unless ( $bindings = $to->describe_as($category) ) {
      $any_failure_so_far++;
      next;
    }
  }
  return $any_failure_so_far ? 0 :1;
}
1;

