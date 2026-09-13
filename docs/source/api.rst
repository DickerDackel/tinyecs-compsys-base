tinyecs-compsys-base API
========================

.. contents::
   :class: this-will-duplicate-information-and-it-is-still-useful-here

Components
----------

Registers the following CIDs to ``tinyecs-compsy.Comp``:

* CROND
* FOLLOWUP
* IS_KILLED
* KILL_WITH_PARENT
* TIMER

.. autoclass:: tinyecs.compsys.base.Timer
   :members:


Systems
-------

.. autofunction:: tinyecs.compsys.base.
.. autofunction:: tinyecs.compsys.base.sys_crond
.. autofunction:: tinyecs.compsys.base.sys_followup
.. autofunction:: tinyecs.compsys.base.sys_kill_with_parent
.. autofunction:: tinyecs.compsys.base.sys_lifetime
.. autofunction:: tinyecs.compsys.base.sys_reap
.. autofunction:: tinyecs.compsys.base.sys_timer
