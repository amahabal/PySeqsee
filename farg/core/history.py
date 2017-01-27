from enum import Enum
from _collections import defaultdict

class EventType(Enum):
  CREATE = 1  # Used for object creation
  CODELET_RUN_START = 2
  CODELET_FORCED = 3
  CODELET_EXPUNGED = 4
  OBJECT_FOCUS = 5
  LTM_SPIKE = 6
  SUBSPACE_ENTER = 7
  SUBSPACE_EXIT = 8
  SUBSPACE_DEEPER_EX = 9

class ObjectType(Enum):
  CONTROLLER = 1
  CODELET = 2
  SUBSPACE = 3
  WS_GROUP = 4
  WS_RELN = 5

class History(object):
  """Maintains history of what happened during a run. Useful for learning weights and such.

  Stores a list of objects and events. Never stores actual objects, but string versions thereof.
  """

  _is_history_on = False
  
  @classmethod
  def TurnOn(cls):
    cls._is_history_on = True

  #: Next available hid (history id). Each "registered" object stores its h_id in the ._hid field.
  _next_hid = 0
  #: Next available event-id.
  _next_eid = 0

  @classmethod
  def _GetNewHID(cls):
    cls._next_hid += 1
    return cls._next_hid - 1

  @classmethod
  def _GetNewEID(cls):
    cls._next_eid += 1
    return cls._next_eid - 1

  #: One entry per event. Each entry is a list (h_id, event_type, possibly-other-info)
  _event_log = []

  #: Object details. There is an entry for each object, and each entry is a dict, with these keys:
  #: p: parents; l: log message for what it was when created.
  _object_details = []

  #: Object events: lists events involving the object. Each entry is thus a list.
  _object_events = defaultdict(list)

  @classmethod
  def AddArtefact(cls, item, artefact_type, log_msg, parents=None):
    if (not cls._is_history_on):
      return
    hid = cls._GetNewHID()
    eid = cls._GetNewEID()
    assert(not hasattr(item, '_hid'))
    item._hid = hid
    event_details = dict(eid=eid, t=EventType.CREATE, hid=hid, ot=artefact_type)
    cls._event_log.append(event_details)
    cls._object_events[hid].append(event_details)

    class_name = item.__class__.__name__
    if hasattr(item, 'ClassName'):
      class_name = item.ClassName()
    details_dict = dict(l=log_msg, t=artefact_type, cls=class_name)
    if parents:
      details_dict['p'] = [x._hid for x in parents]
      for x in parents: 
        cls._object_events[x._hid].append(event_details)
    cls._object_details.append(details_dict)

  @classmethod
  def AddEvent(cls, event_type, log_msg, item_msg_list):
    if (not cls._is_history_on):
      return
    eid = cls._GetNewEID()
    item_msg_list_with_id = [(x[0]._hid, x[1]) for x in item_msg_list]
    event_details = dict(eid=eid, t=event_type, l=log_msg, objects=item_msg_list_with_id)
    cls._event_log.append(event_details)
    for item, msg in item_msg_list:
      cls._object_events[item._hid].append(event_details)

  @classmethod
  def Print(cls):
    if (not cls._is_history_on):
      return
    print("=================== HISTORY ====================")
    for idx, events in cls._object_events.items():
      print("\n-------- Object #", idx, ' ----------- ', cls._object_details[idx])
      for l in events:
        print('\t', l)

