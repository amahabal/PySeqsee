from apps.seqsee.categories import Number, MappingBasedCategory
from apps.seqsee.mapping import NumericMapping
from apps.seqsee.testing_utils import FringeOverlapTest, MockSeqseeController, \
  CodeletPresenceSpec

# Too many public methods because of unittest. pylint: disable=R0904
class FringeOverlapTestForAnchored(FringeOverlapTest):
  def TestSanity(self):
    controller = MockSeqseeController(range(0, 10))
    ws = controller.ws
    item_at_pos_1 = ws.GetItemAt(1, 1)
    item_1_node = controller.ltm.GetNodeForContent(item_at_pos_1.object)
    self.AssertFringeContains(controller, item_at_pos_1, {'pos:1': 0.5,
                                                          'pos:2': 0.3,
                                                          item_1_node: 0.4,
                                                          })

    item_at_pos_2 = ws.GetItemAt(2, 2)
    self.AssertFringeOverlap(controller,
                             prior_focus=item_at_pos_1,
                             current_focus=item_at_pos_2,
                             min_expected_overlap=0.3,
                             expected_similarity_affordances=())

  def Test_123_123(self):
    controller = MockSeqseeController((1, 2, 3, 1, 2, 3))
    ws = controller.ws
    numeric_succesor_mapping = NumericMapping('succ', Number)
    ascending_group = MappingBasedCategory.Construct(numeric_succesor_mapping)
    group1 = self.HelperCreateAndInsertGroup(ws, (0, 1, 2), numeric_succesor_mapping)
    group2 = self.HelperCreateAndInsertGroup(ws, (3, 4, 5), numeric_succesor_mapping)
    group1.object.DescribeAs(ascending_group)
    group2.object.DescribeAs(ascending_group)
    self.AssertFringeContains(controller, group1, { numeric_succesor_mapping: 0.9 })

    from apps.seqsee.get_mapping import CF_FindAnchoredSimilarity
    self.AssertFringeOverlap(
        controller, group1, group2, 0.4,
        expected_similarity_affordances=(
            CodeletPresenceSpec(CF_FindAnchoredSimilarity, {'left': group1,
                                                            'right': group2 }),))

    controller.stream.FocusOn(group2)
    controller.Step()
    from apps.seqsee.codelet_families.all import CF_FocusOn
    self.AssertCodeletPresent(CodeletPresenceSpec(CF_FocusOn),
                              controller.coderack._codelets)
