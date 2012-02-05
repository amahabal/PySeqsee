A brief motivation and overview of PySeqsee
=============================================

Goals
------

PySeqsee is a framework for writing programs to solve complex problems that are
not amenable to brute-force solutions. It is written in Python. The program that
is driving the framework's development attempts to understand and extend integer
sequences.

Architecture
------------------------

PySeqsee attempts to simulate some aspects of human cognition --- specifically,
the highly context-sensitive nature of thought, the pervasive use of categories,
and our roving-eye attention. It has a black-board architecture, and has much
in common with Hofstadter and Mitchell's Copycat and Bernaard Baars' Global
Workspace Theory.

Why focus on cognition?
-------------------------

Human minds are trivially the smartest machines around. Reverse engineering
some aspects of their functioning could be useful. I say this cautiously, fully
aware that the same minds that seem vastly superior at certain tasks (such as 
at philosophy) also seem woefully inferior in other tasks (such as mindless
number crunching, but also, these days, playing Chess). For the tasks where we
are much better, what enables us to do well, and what parts of these can be used
in programs? A concrete example might provide a partial answer.

A concrete example
---------------------

The following sequence is hard for computers to understand but presents no
problems for people::
 
  1 7 1 2 8 1 2 3 9 

To make sense of the sequence, one has to figure out how to split this 
into pieces.  This particular sequence is an interlacing of a pair of 
sequences "(1) (1 2) (1 2 3)" and "7 8 9".  Since each piece of either 
sequence could be of any size, the number of ways of splitting the 
sequence is enormous, even assuming that only two interlacing sequences 
are present.  Without that assumption, the number of potential splits 
becomes even larger and a naïve brute-force algorithm has little hope of 
solving such sequences.

What enables people to understand such a sequence 
effortlessly?  There are several easily picked up the hints as to the 
grouping of the terms: {{write this}}.  
