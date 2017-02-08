from farg.apps.pyseqsee.objects import PSElement, PSGroup

def PSObjectFromStructure(structure):
  if isinstance(structure, int):
    return PSElement(magnitude=structure)
  assert(isinstance(structure, tuple))
  parts = [PSObjectFromStructure(x) for x in structure]
  return PSGroup(items=parts)

