def PSObjectFromStructure(structure):
  """Creates an object given the structure.

  Structure can be an integer (and this results is a PSElement), or a tuple of structures (and this
  results in a PSGroup).

  TODO: We need to add support for "unknowns" here, once we have objects representing an unknown.
  """
  from farg.apps.pyseqsee.objects import PSElement, PSGroup

  if isinstance(structure, int):
    return PSElement(magnitude=structure)
  assert(isinstance(structure, tuple))
  parts = [PSObjectFromStructure(x) for x in structure]
  return PSGroup(items=parts)

def StructureToString(structure):
  """Converts a structure to serialized form.
  
  Structure can be an integer (and this results in str(int)), or a tuple of structures (and this
  results in a comma-separated strings ensconced in parentheses).
  
  
  Examples:
    4                   ==> "4"
    (4, )               ==> "(4)"
    ((4, ), )           ==> "((4))"
    (5, 6)              ==> "(5, 6)"
    (8, (9, 10))        ==> "(8, (9, 10))"
    (8, (9, (10, ())))  ==> "(8, 9, (10, ()))"
  """
  if isinstance(structure, int):
    return str(structure)
  assert(isinstance(structure, tuple))
  return '(' + ', '.join(StructureToString(x) for x in structure) + ')'
