from farg.codelet import Codelet, CodeletFamily

class CF_CheckIfInstance(CodeletFamily):
  @classmethod
  def Run(cls, controller, obj, cat):
    if obj.DescribeAs(cat):
      # To convert: controller.ltm.Spike(cat, 10)
      # link = controller.ltm.InsertISALink(obj.GetPlatonic(), cat)
      # controller.ltm.Spike(link, 5)
      pass

class CF_FocusOn(CodeletFamily):
  """Not converted: this also looked for sameness around head. There was also a continuewith."""
  @classmethod
  def Run(cls, controller, what=None):
    if what:
      hits_map = controller.stream.FocusOn(what)
      # Should be handled by the controller. Where does *that* sit?
    else:
      what = controller.ws.SelectObjectOrRelation()
      if what:
        hits_map = controller.stream.FocusOn(what)
        # The controller should do something...


class CF_AttemptExtensionOfGroup(CodeletFamily):
  """Not converted: stuff about underlying_mapping."""
  @classmethod
  def Run(cls, controller, obj, rightward):
    if isinstance(obj, SElement):
      return
    extension = obj.FindExtension(rightward=rightward)
    if not extension: return
    if not obj.SafeExtend(extension, rightward): return
    if (Toss(obj.strength / 100)):
      controller.AddCodelet(CF_AreWeDone, 100, group=obj)

class CF_TryToSquint(CodeletFamily):
  @classmethod
  def Run(cls, controller, actual, intended):
    potential_squints = actual.CheckSquintability(intended)
    if not potential_squints: return
    chosen_squint = controller.SpikeAndChoose(100, potential_squints)
    if not chosen_squint: return
    cat, name = chosen_squint.GetCatAndName()
    actual.AnnotateWithMetonym(cat, name)
    actual.SetMetonymActiveness(True)
