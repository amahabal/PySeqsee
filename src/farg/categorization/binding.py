class Binding(object):
  """Specification of how an instance is a member of some category.
  
  .. Note::
  
    In the Perl version, the bindings had special slots for squinting, position, metotype
    etc. Here, all are part of the same hash, along with "regular" attributes such as length.
  
    This also means that the caller of the constructor needs to do all the work, unlike in
    Perl, where some bits were calculated by the constructor. 
  """
  def __init__(self, **bindings):
    self.bindings = dict(bindings)

  def GetBindingsForAttribute(self, attribute_name):
    """Get the binding of a single attribute."""
    return self.bindings[attribute_name]

  def __str__(self):
    return 'Bindings: %s' % self.bindings
