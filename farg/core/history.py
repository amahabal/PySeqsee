from _collections import defaultdict
from enum import Enum
from functools import wraps
from tkinter import Tk, ttk, LEFT, NW, BOTH, Button, Text, END
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
  #: parents: parents of the object; log: log message for what it was when created.
  _object_details = []

  #: Object events: lists events involving the object. Each entry is thus a list.
  _object_events = defaultdict(list)

  #: Grab-bag for arbitrary counts.
  _counts = defaultdict(int)

  @classmethod
  def Note(cls, note_string, *, times=1):
    cls._counts[note_string] += times

  @classmethod
  def AddArtefact(cls, item, artefact_type, log_msg, parents=None):
    if (not cls._is_history_on):
      return
    hid = cls._GetNewHID()
    eid = cls._GetNewEID()
    assert(not hasattr(item, '_hid'))
    item._hid = hid
    event_details = dict(eid=eid, type=EventType.CREATE, hid=hid, artefact_type=artefact_type)
    cls._event_log.append(event_details)
    cls._object_events[hid].append(event_details)

    class_name = item.__class__.__name__
    if hasattr(item, 'ClassName'):
      class_name = item.ClassName()
    details_dict = dict(log=log_msg, artefact_type=artefact_type, class_name=class_name)
    if parents:
      details_dict['parents'] = [parent._hid for parent in parents]
      for parent in parents:
        cls._object_events[parent._hid].append(event_details)
    cls._object_details.append(details_dict)

  @classmethod
  def AddEvent(cls, event_type, log_msg, item_msg_list):
    if (not cls._is_history_on):
      return
    eid = cls._GetNewEID()
    item_msg_list_with_id = [(x[0]._hid, x[1]) for x in item_msg_list]
    event_details = dict(eid=eid, type=event_type, log=log_msg, objects=item_msg_list_with_id)
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
      for event in events:
        print('\t', event)

def NoteCallsInHistory(func):
  """Function decorator that increments history counter for wrapped function whenever it is called.

  The key used is the functions name."""
  @wraps(func)
  def Wrapped(*args, **kwargs):
    History.Note(func.__name__)
    return func(*args, **kwargs)
  return Wrapped

class HistoryGUI(object):
  """GUI for displaying history."""

  def __init__(self):
    self.root = Tk()
    root = self.root
    root.title("History")
    root.minsize(width=640, height=490)

    self.historyNB = ttk.Notebook(root)
    self._AddCountsFrame()
    self._AddSummaryFrame()
    self._AddObjectHistoryFrame()
    self._AddEventsFrame()
    self.historyNB.pack(fill=BOTH)
    self.Refresh()

  def Refresh(self):
    self.countsText.delete(1.0, END)
    self.countsText.insert(END, self.PrintCounts())
    self.summaryText.delete(1.0, END)
    self.summaryText.insert(END, self.Summary())

  def _AddSummaryFrame(self):
    #####CREATE SUMMARY FRAME#####
    summaryFrame = ttk.Frame(self.root, name="summary")
    self.summaryText = Text(summaryFrame)
    self.summaryText.pack()
    self.historyNB.add(summaryFrame, text='Summary', underline=0, padding=2)

  def _AddCountsFrame(self):
    countsFrame = ttk.Frame(self.root, name="counts")
    self.countsText = Text(countsFrame)
    self.countsText.pack()
    self.historyNB.add(countsFrame, text='Counters', underline=0, padding=2)

  def _AddObjectHistoryFrame(self):
    objHistFrame = ttk.Frame(self.root, name="history")

    HID = ttk.Label(objHistFrame, text="HID: ")
    HID.pack()

    histHIDInput = ttk.Entry(objHistFrame)
    histHIDInput.focus_set()
    histHIDInput.pack()

    objHistoryLbl = ttk.Label(objHistFrame, wraplength='4i', justify=LEFT, anchor=NW,
                              text="")

    submit = Button(objHistFrame, text="Get Ancestry",
                    width=10,
                    command=lambda: objHistoryLbl.config(text=self.EventsForItem(histHIDInput.get())))

    submit.pack()
    objHistoryLbl.pack()
    self.historyNB.add(objHistFrame, text="Object History", underline=0, padding=2)

  def _AddEventsFrame(self):
    eventsFrame = ttk.Frame(self.root, name="events")

    HID = ttk.Label(eventsFrame, text="HID: ")
    HID.pack()

    eventsHIDInput = ttk.Entry(eventsFrame)
    eventsHIDInput.focus_set()
    eventsHIDInput.pack()

    eventsLbl = ttk.Label(eventsFrame, wraplength='4i', justify=LEFT, anchor=NW,
                          text="")

    submit = Button(eventsFrame, text="Get Events",
                    width=10,
                    command=lambda: eventsLbl.config(text=self.EventsForItem(eventsHIDInput.get())))

    submit.pack()
    eventsLbl.pack()
    self.historyNB.add(eventsFrame, text="Object Events", underline=0, padding=2)


  @classmethod
  def GroupObjectsByClass(cls):
    """Groups objects by class.

    Returns:
      A dictionary with cls as key and list of object indices as value.
    """
    groupedObjects = defaultdict(list)
    for idx, obj in enumerate(History._object_details):
      groupedObjects[obj['class_name']].append(idx)
    return groupedObjects

  @classmethod
  def GroupObjectEventsByClass(cls, hid):
    groupedObjects = defaultdict(list)
    try:
      events = History._object_events[hid]
    except:
      return groupedObjects
    for event in events:
      if event['type'] is EventType.OBJECT_FOCUS:
        groupedObjects['FOCUS'].append(event['eid'])
      elif event['type'] is EventType.CREATE:
        hid_here = event['hid']
        groupedObjects['CREATE ' + History._object_details[hid_here]['class_name']].append(event['eid'])
      else:
        groupedObjects['UNCLASSIFIED'].append(event['eid'])
    return groupedObjects

  @classmethod
  def GetObjectsWithClass(cls, objClass):
    """Get objects with class objClass

    Returns:
      A list of the ids of all objects with the specified class
    """
    return [obj[0]['id'] for idx, obj in History._object_events if obj[0]['type'] is objClass]

  @classmethod
  def Summary(cls):
    summaryStr = ""
    obj_by_cls = sorted(cls.GroupObjectsByClass().items(), reverse=True, key=lambda x: len(x[1]))
    for objClass, eventIds in obj_by_cls:
      summaryStr += "\t%5d\t%s" % (len(eventIds), objClass) + "\n"
      summaryStr += "\t\t" + '; '.join(str(eid) for eid in eventIds[:10]) + "\n"
    return summaryStr

  @classmethod
  def EventsForItem(cls, hid):
    eventsStr = ""
    hid = int(hid)
    obj_by_cls = sorted(cls.GroupObjectEventsByClass(hid).items(), reverse=True, key=lambda x: len(x[1]))
    for objClass, eventIds in obj_by_cls:
      eventsStr += "\t%5d\t%s" % (len(eventIds), objClass) + "\n"
      eventsStr += "\t\t" + '; '.join(str(eid) for eid in eventIds[:10]) + "\n"
    return eventsStr

  @classmethod
  def PrintCounts(cls):
    countsStr = ""
    for objClass, counts in sorted(History._counts.items(), reverse=True, key=lambda x: x[1]):
      countsStr += '\t%5d\t%s' % (counts, objClass) + "\n"
    return countsStr

  @classmethod
  def ObjectHistory(cls, hid, print_depth=0, max_depth=5):
    hid = int(hid)
    objHistoryStr = ""
    try:
      details = History._object_details[hid]
    except:
      return

    objHistoryStr += '*    ' * print_depth, '[%d]\t%s\t%s' % (hid, details['class_name'], details['log']) + "\n"
    if print_depth >= max_depth:
      return
    if 'parents' in details:
      for parent in details['parents']:
        cls.ObjectHistory(parent, print_depth=print_depth+1, max_depth=max_depth)
