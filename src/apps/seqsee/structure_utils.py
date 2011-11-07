def StructureDepth(structure):
  """Returns how deeply nested a structure is. 0 is no nesting, 1 is flat, etc."""
  if isinstance(structure, int):
    return 0
  return 1 + max(StructureDepth(x) for x in structure)
