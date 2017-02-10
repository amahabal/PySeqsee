class Categorizable(object):

  def __init__(self):
    #: Map from categories to the logic describing how this is an instance.
    self.categories = dict()

  def IsKnownAsInstanceOf(self, category):
    """True if known to be an instance of category."""
    return category in self.categories

  def DescribeAs(self, category):
    """Describes item as instance of category, and remembers the logic if one is found.

    Args:
      category: Describe as instance of this category.

    Returns:
      Returns the logic for instancehood if `self` is instance of `category`, None otherwise.
    """
    if category in self.categories:
      return self.categories[category]
    logic = category.IsInstance(self)
    if logic:
      self.categories[category] = logic
      return logic
    return None

  def MergeCategoriesFrom(self, other):
    for cat, logic in other.categories.items():
      if cat in self.categories:
        self.categories[cat].MergeLogic(logic)
      else:
        self.categories[cat] = logic
