Theory
========

.. note::
    
  Need to add info on fluidity, the stream of thought, and mental spaces.

Parallel Terraced Scan
----------------------
From `the FARG website <http://cogsci.indiana.edu/parallel.html>`_
    
    The parallel terraced scan is the key characteristic of the FARG architecture. It is a nondeterministic, parallel (or at least simulated parallel) architecture in which the actions of many small agents holistically result in the attainment of a high-level goal. The cognitive process modeled may be perception, categorization, the making of analogies -- the underlying architecture used in FARG models is the same. The parallel terraced scan makes it possible to define a great number of microstrategies towards the goal, and actual paths to the goal are explored at different speeds according to their estimated promise.
    
    A good metaphor for this architecture (and the metaphor used in Hofstadter's earlier writings about the parallel terraced scan) is the similar action of enzymes on proteins in the cytoplasm of a (biological) cell. Each enzyme is as stupid as can be, and in no way can it be said to have a picture of the ultimate end of whatever metabolic process it aids (and it may participate in many processes at once) -- and in fact the actions of enzymes in the cytoplasm are a tearing chaos, with proteins being built up and broken down at random. However, all the enzymes working together, along with regulatory mechanisms consisting of yet more enzymes, end up as coherent (-seeming) high-level processes, and the whole thing works beautifully.
    
    Another useful metaphor is the action of ants or termites. Each insect performs an insignificant amount of the work of (say) building a nest, but the end result can be a surprisingly regular, sophisticated structure. Especially the nests of termites, which even have mechanisms for regulation of interior temperature, the effect is of some crafty intelligence, the seat of which is obviously not in any one termite.

The Workspace
-------------
Extending the cell analogy, the *workspace* corresponds with the cytoplasm in a cell, a place buzzing with chaotic activity.  The workspace is initially populated with nodes drawn from the long term memory.  Each of these nodes has an *activation*, a value between 0 and 1 that represents how important it is to solving the current problem.  Over time, the activation fades, causing less used nodes to have less importance. Nodes can have several types of predefined connections between them, specifying how they relate to one another.  Activation can spread along these connections.

Inside the workspace, snippets of code called *codelets* move around, modifying the activations of nodes and relationships between them, and potentially creating more codelets.  Codelets are the most basic and simple actions, corresponding to enzymes in a cell.  Despite their simplicity, however, they work together to solve the problem in a seemingly intelligent manner, just like the ants in the anthill analogy. Codelets are initially contained in the *coderack*, and then run sequentially.

Each workspace has a *temperature* associated with it.  The temperature represents how close the workspace is to finding a solution to the given problem.  The colder the temperature, the closer the problem is to being completed.  When the temperature is warmer, there is more activity, and codelets are a lot more willing to make changes to the workspace.  As the problem gets closer to being solved and the temperature gets cooler, the codelets are less likely to make changes to the workspace.  In effect, this makes the workspace try out several possible solutions at first, then focus in on the best solution as time goes on.  This is similar to how the human mind functions.
