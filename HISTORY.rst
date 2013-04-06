History
=======

06.04.2013
----------

- added initial origin param to ``fn.Stream``
- ``monad.Option`` is flatten by default, Full(Empty) -> Empty, Empty(Full) -> Empty
- added ``op.unfold`` operator 

31.03.2013
----------

- added example of using tail call optimization with changing callable

16.02.2013
----------

- fixed @23 about flipping of underscore function
- added special uniform module
- fixed @22 (underscore functions representation)
- adjustments to unary operators processing in underscore

02.02.2013
----------

- prelimitary implementation of ``recur.tco`` to deal with recursive functions
- ``iters.flatten`` is reimplemented to work with different iterators

27.01.2013
----------

- ``iters.accumulate`` - backported version for Python < 3.3
- first implementation for ``monad.Option`` with tests and README samples

23.01.2013
----------

- ``fn.Stream`` slice is another ``fn.Stream``
- ``fn.Stream`` got new public method ``cursor`` to get position on next evaluated element

21.01.2013
----------

- Update documentation with special ``fn._`` use cases for interactive shells
- Move ``zipwith`` from ``fn.iters`` to ``fn.op``
- ``fn._`` dump to string

18.01.2013
----------

-  Added 22 itertools recipes to ``fn.iters``
-  Documentation is converted to RST

17.01.2013
----------

-  Unit tests coverage for ``fn.stream.Stream``
-  ``_StreamIterator`` works fine both in Python 2/3

16.01.2013
----------

-  Finished underscore module functionality
-  Test cases for all implemented modules/functions
-  Update in Readme file with several fixes
-  Get rid of F.flip classmethod in pref. for simple building blocks
-  Optimized version for fn.op.flip operator

14.01.2013
----------

-  Simplest ``Stream`` implementation
-  Code samples for streams, labdas (``_``) and functions compositions
-  Plan, contribute section in readme file

13.01.2013
----------

-  Full list of ideas on paper
-  Repository is created
-  Initial commit
