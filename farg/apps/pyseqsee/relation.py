from farg.apps.pyseqsee.categorization.categorizable import Categorizable

class PSRelation(Categorizable):
  def __init__(self, *, first, second):
    self.first = first
    self.second = second
    Categorizable.__init__(self)

  def FindCategories(self, *, end_category):
    new_cats = []
    for reln_cat in end_category._RelationCategories:
      if self.IsKnownAsInstanceOf(reln_cat):
        continue
      if (self.DescribeAs(reln_cat)):
        new_cats.append(reln_cat)
    return new_cats

  def FindCategoriesUsingEndCategories(self):
    new_cats = []
    for shared_cat in self.first.CategoriesSharedWith(self.second):
      new_cats.extend(self.FindCategories(end_category=shared_cat))
    return new_cats
