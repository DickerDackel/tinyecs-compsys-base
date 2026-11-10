tinyecs-compsys-base
====================

These are some very basic and framework independent components.

``tinyecs.compsys.base`` provides a set of components and systems that are
independent from any graphics framework or backend.  These components and
systems are mostly about entity management.  See the API docs for a list.

Synopsis
--------

While this package can be imported directly, the more flexible approach is to
have ``tinyecs.compsys`` find it and import it with all other ``compsys``
packages under a common namespace.

.. code:: python

   import tinyecs.compsys as cs

   cs.register()

Installation
------------

It's up to you, if you install the currently provided `compsys` packages from
`tinyecs` by using

.. code:: console

   pip install tinyecs[base]

or include them by adding specific dependencies:

.. code:: console

   pip install tinyecs
   pip install tinyecs-compsys
   pip install tinyecs-compsys-base

Support / Contributing
----------------------

Issues can be opened on `github issues`_

.. _github issues: https://github.com/dickerdackel/tinyecs-compsys-base/issues


License
-------

This software is provided under the MIT license.

See LICENSE file for details.
