problem-visuals: A python visualization suit for common introductary Computer Science Problems
========================================


Introduction
------------
This Module is meant as a tool for visualizing common introductary Computer Science Problems like the n-Queens Problem or the Knight Problem


Installing
----------

Requires Python 3.7+. Download and install the latest release:

::

    pip install git+https://github.com/reclinarka/problem-visuals

Documentation <WIP>
-------------------



Features <WIP>
--------

* IPython/Jupyter Notebook integration.

    .. code:: python

        >>> test = Board(15)
        >>> test.add_piece((2,2),"k")
        >>> test.add_piece((2,3),"P")

    .. image:: https://i.imgur.com/vJqYaMa.png
        :alt: A 9x9 board

* Game Problems

    * Chess Problems (i.e N-Queens)

        .. code:: python

            >>> problem_board(10,Qs=[1,None,2,3])

        .. image:: https://i.imgur.com/n8azSne.png
            :alt: A 9x9 board

    * Sudoku

        .. code:: python

            >>> g = Grid()
            >>> for i in range(9):
            >>>    g.add_number(i+1,0,i)
            >>> g

        .. image:: https://i.imgur.com/sF3anv6.png
            :alt: A 9x9 board

* Puzzles

    * Coloring

    .. code:: python

        >>> assignment = { "WA":"red", "NT":"green", ... "T":"green", }
        >>> Australia(Solution = assignment)

    .. image:: https://i.imgur.com/uXtA7tH.png

    * Logic
