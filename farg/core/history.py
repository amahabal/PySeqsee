from enum import Enum
from _collections import defaultdict
from functools import wraps
from tkinter import Tk, ttk, LEFT, NW, BOTH, Button

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

def NoteCallsInHistory(func):
  """Function decorator that increments history counter for wrapped function whenever it is called.

  The key used is the functions name."""
  @wraps(func)
  def Wrapped(*args, **kwargs):
    History.Note(func.__name__)
    return func(*args, **kwargs)
  return Wrapped

class GUIHistoryMethods(object):
  """GUI version of InteractionHistoryMethods.  Enabled using --history_interactive"""

  @classmethod
  def gui(cls):
    root = Tk()
    root.title("History")
    root.minsize(width=640, height=490)

    historyNB = ttk.Notebook(root)

    #####CREATE SUMMARY FRAME#####
    summaryFrame = ttk.Frame(root, name="summary")
    summaryLbl = ttk.Label(summaryFrame, wraplength='4i', justify=LEFT, anchor=NW,
    text=cls.Summary())
    summaryLbl.pack()

    #####CREATE OBJECT COUNTS FRAME#####
    countsFrame = ttk.Frame(root, name="counts")
    countsLbl = ttk.Label(countsFrame, wraplength='4i', justify=LEFT, anchor=NW,
    text=cls.PrintCounts())
    countsLbl.pack()
   
    #####CREATE OBJECT HISTORY FRAME#####
    objHistFrame = ttk.Frame(root, name="history")

    HID = ttk.Label(objHistFrame, text="HID: ")
    HID.pack()

    histHIDInput = ttk.Entry(objHistFrame)
    histHIDInput.focus_set()
    histHIDInput.pack()

    objHistoryLbl = ttk.Label(objHistFrame, wraplength='4i', justify=LEFT, anchor=NW,
    text="")

    submit = Button(objHistFrame, text="Get Ancestry", width=10, command=lambda: objHistoryLbl.config(text=cls.EventsForItem(histHIDInput.get())))

    submit.pack()
    objHistoryLbl.pack()

    #####CREATE EVENTS NOTEBOOK TAB#####
    eventsFrame = ttk.Frame(root, name="events")

    HID = ttk.Label(eventsFrame, text="HID: ")
    HID.pack()

    eventsHIDInput = ttk.Entry(eventsFrame)
    eventsHIDInput.focus_set()
    eventsHIDInput.pack()

    eventsLbl = ttk.Label(eventsFrame, wraplength='4i', justify=LEFT, anchor=NW,
    text="")
 
    submit = Button(eventsFrame, text="Get Events", width=10, command=lambda: eventsLbl.config(text=cls.EventsForItem(eventsHIDInput.get())))

    submit.pack()
    eventsLbl.pack()

    #####ADD FRAMES TO NOTEBOOK#####
    historyNB.add(summaryFrame, text='Summary', underline=0, padding=2)
    historyNB.add(countsFrame, text='Counters', underline=0, padding=2)
    historyNB.add(eventsFrame, text="Object Events", underline=0, padding=2)
    historyNB.add(objHistFrame, text="Object History", underline=0, padding=2)
    
    historyNB.pack(fill=BOTH)
    root.mainloop()
    
  @classmethod
  def GroupObjectsByClass(cls):
    """Groups objects by class.

    Returns:
      A dictionary with cls as key and list of object indices as value.
    """
    ret = defaultdict(list)
    for idx, obj in enumerate(History._object_details):
      ret[obj['cls']].append(idx)
    return ret

  @classmethod
  def GroupObjectEventsByClass(cls, hid):
    ret = defaultdict(list)
    try:
      events = History._object_events[hid]
    except:
      return ret
    for e in events:
      if e['t'] is EventType.OBJECT_FOCUS:
        ret['FOCUS'].append(e['eid'])
      elif e['t'] is EventType.CREATE:
        hid_here = e['hid']
        ret['CREATE ' + History._object_details[hid_here]['cls']].append(e['eid'])
      else:
        ret['UNCLASSIFIED'].append(e['eid'])
    return ret

  @classmethod
  def Summary(cls):
    summaryStr = ""
    obj_by_cls = sorted(cls.GroupObjectsByClass().items(), reverse=True, key=lambda x: len(x[1]))
    for k, v in obj_by_cls:
      summaryStr += "\t%5d\t%s" % (len(v), k) + "\n"
      summaryStr += "\t\t" + '; '.join(str(x) for x in v[:10]) + "\n"
    return summaryStr

  @classmethod
  def EventsForItem(cls, hid):
    eventsStr = ""
    hid=int(hid)
    obj_by_cls = sorted(cls.GroupObjectEventsByClass(hid).items(), reverse=True, key=lambda x: len(x[1]))
    for k, v in obj_by_cls:
      eventsStr += "\t%5d\t%s" % (len(v), k) + "\n"
      eventsStr += "\t\t" + '; '.join(str(x) for x in v[:10]) + "\n"
    return eventsStr

  @classmethod
  def PrintCounts(cls):
    countsStr = ""
    for k, v in sorted(History._counts.items(), reverse=True, key=lambda x: x[1]):
      countsStr += '\t%5d\t%s' % (v, k) + "\n"
    return countsStr

  @classmethod
  def ObjectHistory(cls, hid, print_depth=0, max_depth=5):
    hid=int(hid)
    objHistoryStr = ""
    try:
      details = History._object_details[hid]
    except:
      return

    objHistoryStr += '*    ' * print_depth, '[%d]\t%s\t%s' % (hid, details['cls'], details['l']) + "\n"
    if print_depth >= max_depth:
      return
    if 'p' in details:
      for parent in details['p']:
        cls.ObjectHistory(parent, print_depth=print_depth+1, max_depth=max_depth)

class InteractionHistoryMethods(object):
  """Interactive methods for exploring the contents stored in history.

  We drop into the interactive shell if --history_interactive is passed in."""

  @classmethod
  def help(cls):
    print("i.Summary() or s(): Prints summary of what happened during the run.")
    print("i.EventsForItem(hid) or e(hid): Prints events that happened to given hid.")
    print("i.PrintCounts() or c(): Prints counters.")
    print("i.ObjectHistory(hid) or h(hid): Prints the ancestry of objects: what caused them to exist.")
    print("dir(h) for what is present in the history class.")

  @classmethod
  def GroupObjectsByClass(cls):
    """Groups objects by class.

    Returns:
      A dictionary with cls as key and list of object indices as value.
    """
    ret = defaultdict(list)
    for idx, obj in enumerate(History._object_details):
      ret[obj['cls']].append(idx)
    return ret

  @classmethod
  def GroupObjectEventsByClass(cls, hid):
    ret = defaultdict(list)
    try:
      events = History._object_events[hid]
    except:
      return ret
    for e in events:
      if e['t'] is EventType.OBJECT_FOCUS:
        ret['FOCUS'].append(e['eid'])
      elif e['t'] is EventType.CREATE:
        hid_here = e['hid']
        ret['CREATE ' + History._object_details[hid_here]['cls']].append(e['eid'])
      else:
        ret['UNCLASSIFIED'].append(e['eid'])
    return ret


  @classmethod
  def Summary(cls):
    print("==== What kinds of objects were created? ==========")
    obj_by_cls = sorted(cls.GroupObjectsByClass().items(), reverse=True, key=lambda x: len(x[1]))
    for k, v in obj_by_cls:
      print("\t%5d\t%s" % (len(v), k))
      print("\t\t", '; '.join(str(x) for x in v[:10]))

  @classmethod
  def EventsForItem(cls, hid):
    obj_by_cls = sorted(cls.GroupObjectEventsByClass(hid).items(), reverse=True, key=lambda x: len(x[1]))
    for k, v in obj_by_cls:
      print("\t%5d\t%s" % (len(v), k))
      print("\t\t", '; '.join(str(x) for x in v[:10]))

  @classmethod
  def PrintCounts(cls):
    for k, v in sorted(History._counts.items(), reverse=True, key=lambda x: x[1]):
      print('\t%5d\t%s' % (v, k))

  @classmethod
  def ObjectHistory(cls, hid, print_depth=0, max_depth=5):
    try:
      details = History._object_details[hid]
    except:
      return

    print('*    ' * print_depth, '[%d]\t%s\t%s' % (hid, details['cls'], details['l']))
    if print_depth >= max_depth:
      return
    if 'p' in details:
      for parent in details['p']:
        cls.ObjectHistory(parent, print_depth=print_depth+1, max_depth=max_depth)
