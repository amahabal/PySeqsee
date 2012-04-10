Coderack
============

The Coderack in Seqsee is like a todo list.  It consists of promising 
actions to take next, each associated with a number indicating the degree 
of promise.  Seqsee chooses an item and runs it, and in that process of 
running it may come up with other promising actions that are then added to 
the Coderack.  

The probability of choosing an item depends on its promise.  Higher 
promise actions are likelier to be chosen, but it is still possible for 
ignore promise actions to occasionally get chosen.  

Each action is called a codelet.  As that term suggests, the action is a 
tiny and targeted.  In fact, Seqsee requires several dozens of codelets to 
understand even simple sequences.  

Just as the contents of a person's to do list can strongly suggest their 
actions over the next few hours, the Coderack's contents indicate the 
directions Seqsee will pursue in the near future.

* To create, specify the maximum number of codelets it can hold::
  
    cr = Coderack(10)
  
* Adding a codelet may expunge an existing codelet if too many are present::

    self.AddCodelet(codelet)
  
* To test for emptyness::

    self.IsEmpty()

* Retrieving a codelet should only be done on a non-empty coderack::

    self.GetCodelet()  # Raises CoderackEmptyException if coderack is empty.
  
* For testing, it is possible to stuff a codelet that is guaranteed to be returned by the
  next call to GetCodelet (provided that there are no AddCodelets in between)::
  
    self.ForceNextCodelet(codelet)

