Adding ability to perceive something
=====================================

Recently (May 2011), I added the ability to see interlaced sequences such as::

  Sequence A)  1 7 2 8 3 9

and (parantheses added for readability)::

  Sequence B)  (1 7 6) (4 11 10) (9 13 15) (16 17 21)

It does not yet see::

  Sequence C) ((1) 7) ((1 2) 8) ((1 2 3) 9)

I will use the recent addition as a case study in adding the ability to see
something that Seqsee did not previously see.

A key philosophy of this entire work is "No brute force".  That is, no 
deep exploration should be undertaken by Seqsee without a good cause.  
What Seqsee uses is similar in spirit to how one goes about doing math, as 
described by George Pólya.  in his books Mathematics and Plausible 
Inference.  Pólya makes a strong case for the idea that mathematics 
proceeds by educated guesses, and he suggests ways of estimating the 
strength of a guess.  Imagine that a mathematician has guessed a new 
theorem based on some observation, but has not yet proved the guess to 
be correct.  If the guess leads to some prediction that turns out to be 
true, the guess is rendered more palatable, more plausible.  If the guess 
predicts something surprising that also turns out to be true, this confers 
a higher degree of credibility on the guess.  If, furthermore, the guess 
is seen to be analogous to some well-known result, it becomes yet more 
trustworthy.  Pólya offers dozens of detailed examples (including a 
translation of some of Euler's writings to the same effect), showing how a 
multitude of tiny facts can add up to a fair amount of trust or distrust 
in an initial guess, and how these kinds of instincts guide mathematicians 
at all stages.  In its far humbler pursuit of extrapolating sequences, I 
like to think, Seqsee acts in a similar way.  

We thus need to accumulate evidence that a sequence is possibly an interlaced sequence.
Where might such evidence be found?

A hallmark of the interlacing of n sequences is the presence of relations 
whose ends are not adjacent.  In Sequence B above, Seqsee will probably 
discover that 1 and 4 are related (they are successive squares), 7 and 11 
are related (successive primes), and 15 and 21 are related (successive 
triangular numbers).  Each of these relations have two intervening numbers 
between the two ends (for example, "7" and "6" are present between "1" and 
"4"), suggesting an interlacing of three sequences.  

With the latest change, whenever Seqsee is focusing on a long-distance 
relation, it pumps a tiny bit of activation into the long-term memory 
concept corresponding to an appropriate number of interlaced sequences.  
If this node is sufficiently active, it will have realized that 
interlacing might be at play in the sequence at hand and will launch a 
subspace to explore this.  The details of how that works do not concern us 
here since we are focused on how that concept is awaken rather that what 
it does thereafter.  

The reason Seqsee does not see Sequence C as of this writing is that 
evidence for more complex interlacing is not accumulated.  One way of 
awakening the relevant concept is noting that the number of intervening 
items between "7" and "8" in that sequence can be seen as "2 elements" 
(namely, "1" and "2"), or as "1 group" (namely, "(1 2)").  If it could see 
the latter, the two-ness of that sequence (which is more hidden than it is 
for Sequence A) will be perceived.  

Accumulation of evidence is pervasive
--------------------------------------

This idea of slowly awakening a concept based on other tangential activity is present everywhere in Seqsee. Some examples:

* The relevance of categories such as Prime is seen this way.  Given a 
  sequence where primality is relevant, Seqsee will not automatically see 
  all primes as being primes.  Whenever a "7" is focused on, because of the 
  link between it and "Prime" in the LTM, the node for "Prime" gets some 
  activation.  If many primes are present, this activation will climb 
  quickly.  When it has become sufficiently active, "7" or other primes may 
  get described as primes, thereby adding "Prime" to its fringe.  This in 
  turn will allow it to be seen as similar to "11" by virtue of being a 
  prime.  One the notion Prime is active, it can cause it to see other 
  things as prime that it could not before (since it did not have an edge 
  between, say, "13" and "Prime").  Extending rightward from (7, 11), Seqsee 
  will try to describe the next number as Prime.  
