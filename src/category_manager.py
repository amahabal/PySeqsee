class CategoryManager:
  def __init__(self):
    self._attribute_store = { 'global': {} }
    self._categories = set()
    self._non_categories = set()

  def HasAttribute(self, attribute_name, ns='global'):
    if ns not in self._attribute_store:
      return self.HasAttribute(attribute_name)
    if attribute_name in self._attribute_store[ns]:
      return True
    elif attribute_name in self._attribute_store['global']:
      return True
    else:
      return False
  def AddAttribute(self, attribute_name, value, ns='global'):
    if ns not in self._attribute_store:
      self._attribute_store[ns] = {}
    self._attribute_store[ns][attribute_name] = value

  def GetAttribute(self, attribute_name, ns='global'):
    if ns not in self._attribute_store:
      return self.GetAttribute(attribute_name)
    if attribute_name in self._attribute_store[ns]:
      return self._attribute_store[ns][attribute_name]
    elif attribute_name in self._attribute_store['global']:
      return self._attribute_store['global'][attribute_name]
    else:
      raise Exception("Attribute %s missing" % attribute_name)
  
  def GetBindings(self, ns='global'):
    if ns is 'global':
      return dict(self._attribute_store['global'].items())
    else:
      l = self._attribute_store['global'].items()
      l.extend(self._attribute_store[ns].items())
      return dict(l)
    
  def MarkAsInstance(self, cat):
    self._non_categories.discard(cat)
    self._categories.add(cat)
    
  def MarkAsNonInstance(self, cat):
    self._categories.discard(cat)
    self._non_categories.add(cat)
  
  def IsKnownInstanceOf(self, cat):
    return cat in self._categories
  
  def IsKnownNonInstanceOf(self, cat):
    return cat in self._non_categories
  