**********************************************************************
git-tag
**********************************************************************

----------------------------------------------------------------------
Showing all tags
----------------------------------------------------------------------

.. code-block:: bash

    $ git tag

.. code-block:: python

   >>> import re
   >>> regex = re.compile('^refs/tags/')
   >>> [r for r in repo.references if regex.match(r)]

----------------------------------------------------------------------
References
----------------------------------------------------------------------

- git-tag_.

.. _git-tag: https://www.kernel.org/pub/software/scm/git/docs/git-tag.html
