from _collections import defaultdict
from enum import Enum
from functools import wraps
from tkinter import Tk, ttk, LEFT, NW, BOTH, Button, Text, END, NORMAL, DISABLED


class EventType(object):
  CREATE = "Create"  # Used for object creation
  CODELET_RUN_START = "Start Codelet Run"
  CODELET_FORCED = "Force Codelet Run"
  CODELET_EXPUNGED = "Expunge Codelet"
  OBJECT_FOCUS = "Focus on Object"
  LTM_SPIKE = "Spike LTM Node"
  SUBSPACE_ENTER = "Enter Subspace"
  SUBSPACE_EXIT = "Exit Subspace"
  SUBSPACE_DEEPER_EX = "Subspace Go Deeper"
  OBJ_MERGED = "Merge Object Into Arena"


class ObjectType(object):
  CONTROLLER = "Controller"
  CODELET = "Codelet"
  SUBSPACE = "Subspace"
  WS_GROUP = "Element or Group"
  WS_RELN = "Relation"

class _HistoryEvent(object):
  def __init__(self, event_id, event_type, *, objects={},
               log_msg='', artefact_type='', **rest):
    self.event_id = event_id
    self.event_type = event_type
    self.log_msg = log_msg
    self.artefact_type = artefact_type
    self.objects = objects
    self.rest = rest

  def PrintIntoTextbox(self, history_gui, tb, indentation=0, vspace=0):
    ind_string = '    ' * indentation
    tb.insert(END, '%s Event# %d: %s %s --- %s\n' % (
       ind_string, self.event_id, self.event_type, self.artefact_type,
       self.log_msg))
    if self.objects:
      tb.insert(END, '%s   Participants\n%s   --------------\n' % (ind_string, ind_string))
      for hid, role in self.objects.items():
        tb.insert(END, '%s\t' % ind_string)
        object_details = History._object_details[hid]
        history_gui._insertHIDLinkIntoTextbox(hid, tb)
        tb.insert(END, ' -- %s %s\n' % (object_details['artefact_type'], object_details['class_name']))
        if role:
          tb.insert(END, '%s\t\tRole: %s\n' % (ind_string, role))
    if self.rest:
      tb.insert(END, '%s Extra: %s\n' % (ind_string, repr(self.rest))) 
    tb.insert(END, '\n' * vspace)

class History(object):
  """Maintains history of what happened during a run.

  Useful for learning weights and such. Stores a list of objects and events.
  Never stores actual objects, but string versions thereof.
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

  #: One entry per event. Each entry is a _HistoryEvent
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
    """Adds to history an artefact we wish to track."""
    if (not cls._is_history_on):
      return
    hid = cls._GetNewHID()
    eid = cls._GetNewEID()
    assert (not hasattr(item, '_hid'))
    item._hid = hid
    event_details = _HistoryEvent(eid, EventType.CREATE,
                                  objects={hid: "created"},
                                  artefact_type=artefact_type)
    cls._event_log.append(event_details)
    cls._object_events[hid].append(event_details)

    class_name = item.__class__.__name__
    if hasattr(item, 'ClassName'):
      class_name = item.ClassName()
    details_dict = dict(
        log=log_msg, artefact_type=artefact_type, class_name=class_name)
    if parents:
      details_dict['parents'] = [parent._hid for parent in parents]
      for parent in parents:
        cls._object_events[parent._hid].append(event_details)
    cls._object_details.append(details_dict)

  @classmethod
  def AddEvent(cls, event_type, log_msg, item_msg_list):
    """Add an event to the history.

    The event may touch multiple objects (as an example, if the event is that
    an object was merged into another, both are impacted.

    The item_msg_list is a dictionary, and should mention each impacted item,
    along with a msg.
    """
    if (not cls._is_history_on):
      return
    eid = cls._GetNewEID()
    item_msg_list_with_id = dict([(x[0]._hid, x[1]) for x in item_msg_list])
    history_event = _HistoryEvent(eid, event_type, log_msg=log_msg, objects=item_msg_list_with_id)
    cls._event_log.append(history_event)
    for item, msg in item_msg_list:
      cls._object_events[item._hid].append(history_event)

  @classmethod
  def Print(cls):
    if (not cls._is_history_on):
      return
    print('=================== HISTORY ====================')
    for idx, events in cls._object_events.items():
      print('\n-------- Object #', idx, ' ----------- ',
            cls._object_details[idx])
      for event in events:
        print('\t', event)


def NoteCallsInHistory(func):
  """Function decorator that increments history counter for wrapped function whenever it is called.

  The key used is the functions name.
  """

  @wraps(func)
  def Wrapped(*args, **kwargs):
    History.Note(func.__name__)
    return func(*args, **kwargs)

  return Wrapped


class HistoryGUI(object):
  """GUI for displaying history."""

  def __init__(self, root):
    self.root = root
    #: When this is not -1, the details for the object with the eid will be shown in the details
    #: pane.
    self._id_for_details = -1

    self.historyNB = ttk.Notebook(root)
    self._AddSummaryFrame()
    self._AddCountsFrame()
    self._AddObjectDetailsFrame()
    self._AddRecentEventsFrame()
    self.historyNB.pack(fill=BOTH)
    self.Refresh()

  def Refresh(self):
    for t in (self.countsText, self.summaryText, self.detailsText,
              self.recentText):
      t.config(state=NORMAL)
    self.countsText.delete(1.0, END)
    self.countsText.insert(END, self.PrintCounts())
    self._RefreshSummary(self.summaryText)
    self._RefreshDetails()
    self._RefreshRecent()
    for t in (self.countsText, self.summaryText, self.detailsText,
              self.recentText):
      t.config(state=DISABLED)

  def _RefreshDetails(self):
    self.detailsText.config(state=NORMAL)
    self.detailsText.delete(1.0, END)
    if self._id_for_details != -1:
      self.detailsText.insert(END, 'Details for #%d\n\nAncestry\n===========\n'
                              % self._id_for_details)
      self._insertAncestry(self.detailsText, self._id_for_details)
      self.detailsText.insert(END, '\n\nEvents:\n==========\n')
      events_to_show = History._object_events[self._id_for_details][-10:] 
      events_to_show.reverse()
      for e in events_to_show:
        e.PrintIntoTextbox(self, self.detailsText, indentation=1, vspace=1)
    self.detailsText.config(state=DISABLED)

  def _RefreshRecent(self):
    rt = self.recentText
    rt.delete(1.0, END)
    event_count = len(History._event_log)
    recent = History._event_log[-10:]
    recent.reverse()
    for idx, r in enumerate(recent):
      r.PrintIntoTextbox(self, rt, indentation=0, vspace=2)

  def _insertHIDLinkIntoTextbox(self, hid, tb):
    tag_name = 'id_%d' % hid
    tb.tag_configure(
      tag_name,
      underline=True,
      font=
      '-adobe-helvetica-bold-r-normal--20-140-100-100-p-105-iso8859-4',)

    def ClickAction(me, my_hid):
      return lambda x: me._SwitchToDetailPane(my_hid)

    tb.tag_bind(tag_name, '<Button-1>', ClickAction(self, hid))
    tb.insert(END, str(hid), tag_name)
    

  def _RefreshSummary(self, summaryText):
    summaryText.delete(1.0, END)
    obj_by_cls = sorted(
        self.GroupObjectsByClass().items(),
        reverse=True,
        key=lambda x: len(x[1]))
    for objClass, eventIds in obj_by_cls:
      summaryText.insert(END, '\n%5d\t' % len(eventIds))
      summaryText.insert(END, objClass, 'obj_type')
      summaryText.insert(END, '\t')
      for hid in eventIds[:10]:
        self._insertHIDLinkIntoTextbox(hid, summaryText)
        summaryText.insert(END, '\t')

  def _AddSummaryFrame(self):
    #####CREATE SUMMARY FRAME#####
    summaryFrame = ttk.Frame(self.root, name='summary')
    self.summaryText = Text(summaryFrame, height=55)
    self.summaryText.tag_configure(
        'obj_type',
        foreground='blue',
        font='-adobe-helvetica-bold-r-normal--20-140-100-100-p-105-iso8859-4',)
    self.summaryText.pack()
    self.historyNB.add(summaryFrame, text='Summary', underline=0, padding=2)

  def _AddCountsFrame(self):
    countsFrame = ttk.Frame(self.root, name='counts')
    self.countsText = Text(countsFrame, height=55)
    self.countsText.pack()
    self.historyNB.add(countsFrame, text='Counters', underline=0, padding=2)

  def _AddObjectDetailsFrame(self):
    detailsFrame = ttk.Frame(self.root, name='details')
    self.detailsText = Text(detailsFrame, height=55)
    self.detailsText.pack()
    self.historyNB.add(
        detailsFrame, text='Object Details', underline=0, padding=2)

  def _AddRecentEventsFrame(self):
    recentEventsFrame = ttk.Frame(self.root, name='recent')
    self.recentText = Text(recentEventsFrame, height=55)
    self.recentText.pack()
    self.historyNB.add(recentEventsFrame, text='Recent Events', underline=0, padding=2)

  def _SwitchToDetailPane(self, hid):
    """Focus on details pane."""
    self._id_for_details = hid
    self._RefreshDetails()
    self.historyNB.select(2)

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
      event_type = event.event_type
      if event_type is EventType.OBJECT_FOCUS:
        groupedObjects['FOCUS'].append(event.event_id)
      elif event_type is EventType.CREATE:
        hid_here = list(event.rest["objects"].items())[0][0]
        groupedObjects['CREATE ' + History._object_details[hid_here][
            'class_name']].append(event.event_id)
      else:
        groupedObjects['UNCLASSIFIED'].append(event.event_id)
    return groupedObjects

  #TODO(amahabal): THIS MAY BE UNNEEDED AND BROKEN. CHECK AND REMOVE.
  @classmethod
  def GetObjectsWithClass(cls, objClass):
    """Get objects with class objClass

    Returns:
      A list of the ids of all objects with the specified class
    """
    return [
        obj[0]['id'] for idx, obj in History._object_events
        if obj[0]['type'] is objClass
    ]

  #TODO(amahabal): THIS MAY BE UNNEEDED AND BROKEN. CHECK AND REMOVE.
  @classmethod
  def EventsForItem(cls, hid):
    eventsStr = ''
    hid = int(hid)
    obj_by_cls = sorted(
        cls.GroupObjectEventsByClass(hid).items(),
        reverse=True,
        key=lambda x: len(x[1]))
    for objClass, eventIds in obj_by_cls:
      eventsStr += '%5d\t%s' % (len(eventIds), objClass) + '\n'
      eventsStr += '\t\t' + '; '.join(str(eid) for eid in eventIds[:10]) + '\n'
    return eventsStr

  @classmethod
  def PrintCounts(cls):
    countsStr = ''
    for objClass, counts in sorted(
        History._counts.items(), reverse=True, key=lambda x: x[1]):
      countsStr += '\t%5d\t%s' % (counts, objClass) + '\n'
    return countsStr

  def _insertAncestry(self, detailsText, hid, print_depth=0, max_depth=5):
    try:
      details = History._object_details[hid]
    except:
      return
    detailsText.insert(END, '%s[%d]\t%s\t%s\n' % (
        '*    ' * print_depth, hid, details['class_name'], details['log']))
    if print_depth >= max_depth:
      return
    if 'parents' in details:
      for parent in details['parents']:
        self._insertAncestry(
            detailsText,
            parent,
            print_depth=print_depth + 1,
            max_depth=max_depth)
