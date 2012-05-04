How to create a workspace
==========================

The workspace is the virtual blackboard on which various codelets make
annotations about their observations and relationships that they have observed.
The workspace will store the pieces of the problem at hand and of the solution
being developed.

In this section, I assume that you have started creating a new app called Cat.
Please note that the skeleton app generated already contains a file for the
workspace.

Initializing the workspace
----------------------------

When you start the cat application using::

  python3 run_cat.py <flags>

the flags can be used to specify the input. The generated app has a flag called
'--input' and a flag called '--expected_output' for use in automated tests. You
may choose to use names, or you can create a different flags that better reflect
your domain. Seqsee uses the flags 'sequence' and 'unrevealed_terms'.

These flags are available in the FLAGS variable. You can access them thus::

  from farg.third_party import gflags
  FLAGS = gflags.FLAGS
  FLAGS.input

In the "main" class (in this example, CatMain in "run_cat.py"), you can define
the method ProcessCustomFlags to do any processing at startup. Seqsee uses this
function to convert the input string to a more useful form, a list of numbers.

Objects in a workspace
------------------------

The way Seqsee works can be described very roughly as follows. The workspace
initially contains numbers from the input sequence. It repeatedly "focuses on"
objects in the workspace (initially just numbers, but latter this also includes
other structures that get built up), and such focusing triggers certain actions
either directly or via similarity to recently-focused-upon objects.

For Seqsee to focus on something, it must be an instance of the mixin class
FocusableMixin. This class provides the following over-ridable methods.

GetFringe
**********

I quote from the Seqsee Dissertation:

        In his  Principles of Psychology, James (1890) described the fringe as a 
        penumbra of vague experiences, sometimes using the terms  psychic overtones
        or suffusion. Consider the concept of Vietnam. When that concept is evoked, it 
        does not come alone. It brings along with it, to various degrees, such concepts 
        as war, Agent Orange, and Iraq; or perhaps  the beautiful beaches and the 
        brilliant green rice paddies and women in conical hats; or perhaps just idle facts 
        like "its capital is Hanoi" and "it is near China". To each person the package that 
        is Vietnam is differently filled, but for most, it is not empty. If I next mention 
        another place, it would appear more or less similar, depending on how, in the 
        reader's mind, its package overlaps with the reader's version of the Vietnam 
        package. Florida with its beaches, China with its rice paddies, Kosovo with its 
        war, or even New York with its "I enjoyed my vacation there" may appear 
        similar.

        Concepts in Seqsee also have such fringes ("packages") of related 
        concepts. If Seqsee has noticed that, by squinting, the group "(1 1) 2 3"  can be 
        seen as the ascending group "1 2 3", then the fringe of "(1 1) 2 3" will contain, 
        among other things, the concept ascending group, the concept blemished version 
        of an ascending group, and the concept "1 2 3"-group. In this context, the group 
        "4 5 6 (7 7) 8", being both ascending and blemished-ascending, will appear more 
        similar to this group than the merely ascending "5 6 7" does.

GetFringe returns the fringe of an object. It is passed in the constructor, and
through it, it has access to the LTM, the coderack, or whatever else it needs. It should
return a list of 2-tuples, the fringe element and its intensity.
    
    
GetSimilarityAffordances
*************************
    
When two items are focused on, one soon after the other, and it happens 
that their fringes overlap, this method suggests codelets that may be 
created to explore the similarity.  For example, in Seqsee, it "1 2 3" is seen
soon after "4 5 6", the fringes would overlap since both are ascending groups. In
this case, the 'GetSimilarityAffordances' for the *previous object* (in this case, 
"4 5 6") is called with three extra arguments: the current focus ("1 2 3"), and
the fringes of the two objects. It should returns a list of codelets, 0 or more
of which may finally get added to the coderack.

Since a current focus can overlap with multiple recent items, the GetSimilarityAffordances
method of each is called. They all suggest potential codelets, with an associated urgency.
Approximately two of these are stochastically chosen, biased by their urgency.

GetAffordances
***************

The following quote from Donald Norman's *The Design of Everyday Things*
(2002, p. 9) describes affordances:

        The term affordance refers to the perceived and actual properties of the 
        thing, primarily those fundamental properties that determine just how the 
        thing could possibly be used.

        Affordances provide strong clues for the operations of things.  Plates are 
        for pushing.  Knobs are for turning.  Slots are for inserting things into.  
        Balls are for throwing or bouncing.  

All manner of objects --- both physical entities and mental constructs ---
have affordances (here used in the limited sense of 'possible actions suggested 
by the object'). A humorous example is suggested by Mark Twain's advice to
writers, "If you find an adjective, kill it", and another by Jeremy Silman's advice 
to chess players (1998, p. 4): "The existence of an open center should be likened 
to a neon sign saying, 'Castle immediately! Castle immediately!'"

The GetAffordances method is called when an object is focused upon, and it should
return a list of codelets that could be run in response to observing this object.

OnFocus
********

This is a utility method that is called when an object is focused upon, and is
primarily useful for book-keeping.
