class ReadInputSpec:
  def Read(self, filelike):
    for line in filelike:
      if line.strip().startswith('#'):
        continue
      if not '|' in line:
        continue
      input, continuation = (x.split() for x in line.strip().split('|'))
      yield dict(spec=dict(sequence=' '.join(input),
                           unrevealed_terms=' '.join(continuation)),
                 name=' '.join(input))

  def ReadFile(self, filename):
    return self.Read(open(filename))
