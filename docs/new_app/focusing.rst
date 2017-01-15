Focusing and "the attention economy"
=====================================

As we go through a day, our attention jumps around. When driving, say, a few things that we spend attending to could include the following, not all of which hold our attention for the same duration:

* We may see a red traffic light, and stop
* Seeing a green traffic light turn yellow, we may wonder if we will get through before it turns red
* We may notice a red car weaving through traffic, and become more cautious
* Noticing traffic ahead slowing down, we wonder if there is an accident up ahead or perhaps a lurking cop.
* Further ahead, we notice that there indeed has been an accident. We pat ourselves on a correct guess, while also being saddened a tad, and reminded of our own mortality.
* Oh, the car that creashed is that red car. He was surely asking for it. What was the big hurry?

In each of these cases, something held our attention a bit, and directed subsequent thoughts and actions. This is the stream of thought or the stream of consciousness. 

In PySeqsee, the "stream" plays this role. Things can be focused on, and this leads to directing subsequent attention and actions. This is also, as explained below, how Pyseqsee makes serendipitous discoveries.


Effects of focusing
---------------------

In PySeqsee, focusing on an "object" leads to three kinds of consequences. But first, a few words on what can be "objects". There is no restriction on what these can be, and two large classes have been seen to be useful: first, structures or patterns that have been seen in the input problem (in understanding a sequence, this could include a chunk "1 1 1" in the input), and second, subgoals and subproblems that pop up along the way. The three kinds of consequences are:

1. The object may suggest actions. For example, in the Bongard problems, focusing on a "17" that we have already noticed is a prime number can lead to checking if other primes are present. This kind of action occurs via the addition of codelets.
2. Associated concepts in the long-term memory may get a small jolt of activation, and
3. If this object is deemed similar to another recently seen object, this similarity can also create more codelets to direct subsequent actions. This is how serendipity shows up in PySeqsee: chance seeing of related items soon after one another can lead to unexpected connections. Of note here is that similarity in PySeqsee is a very fluid notion: what concepts have been activated and what categories have been associated can shape how similar two items are. Experimental psychology has shown that such warping of similarity happens in people and the act of labeling to abstract objects with the same category makes them appear similar.

Fringe of an object
---------------------

This notion, borrowed from the american psychologist and philosopher William James, is needed to complete the story. I quote from Chapter 5 of the `Seqsee dissertation <http://cogsci.indiana.edu/pub/Seqsee%20--%20double%20sided.pdf>`_

	In his *Principles of Psychology*, James (1890) described the fringe as a
	*penumbra* of vague experiences, sometimes using the terms *psychic overtones*
	or *suffusion*. Consider the concept of *Vietnam*. When that concept is evoked, it
	does not come alone. It brings along with it, to various degrees, such concepts
	as war, Agent Orange, and Iraq; or perhaps the beautiful beaches and the
	brilliant green rice paddies and women in conical hats; or perhaps just idle facts
	like "its capital is Hanoi" and "it's near China". To each person the package that
	is Vietnam is differently filled, but for most, it is not empty. If I next mention
	another place, it would appear more or less similar, depending on how, in the
	reader‘s mind, its package overlaps with the reader‘s version of the Vietnam
	package. Florida with its beaches, China with its rice paddies, Kosovo with its
	war, or even New York with its "I enjoyed my vacation there" may appear
	similar.

Two objects in PySeqsee are deemed to be similar to the extent that their fringes overlap. The fringe of an object can change over the course of a run as it is understood more, and thus the similarity between objects also evolves over the course of a run (and beyond, because of long-term memory).

Fringe overlap
----------------

When the fringes of two objects overlap, it suggests that the two are similar. Moreover, the greater the overlap, the greater is the potential similarity. I will call out one particular happy situation, when one object is in fact a goal. The other object whose fringe overlaps it may be a solution. The anecdote of the discovery of dynamite fits this mold:

	If similarity is perceived between a problem
	we have been struggling with (take, for example, the case of Alfred Nobel
	struggling to find something to mix with nitroglycerine to decrease unintended
	explosions) and a chance observation (as happened when Nobel dropped some
	nitroglycerin by mistake on sawdust and the feared explosion did not happen), 
	we may realize that the observation might somehow help us solve the problem
	and follow the lead. If, on the other hand, similarity is perceived between a
	failed attempt at solving some problem and another recent failed attempt, we
	may attempt something radically different.


Mechanics of focusing
-----------------------

Now we turn to mundane matters of what this looks like in code.

To make is possible to focus on an object, it needs to be made an instance of the class :py:class:`~farg.core.focusable_mixin.FocusableMixin`. It would also override some or all of these methods.

GetAffordances(self, controller)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This method can implement consequences of types 1 and 2 above. Codelets may be added to the passed in controller, thereby influencing what is likely to happen next. Instead of merely influencing probabilities of what happens next, it is also possible to force what the next codelet will be, and thereby have a more targeted effect.

GetFringe(self, controller)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 
This returns the fringe of the object, which consists of a weighted set of strings.

GetSimilarityAffordances(self, other, my_fringe, other_fringe, controller)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When focusing on an object, if there is sufficient fringe overlap with a prior object, this method is called, and it can add codelets to influence what the program is likely to do next.



