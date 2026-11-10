from collections.abc import Callable
from dataclasses import dataclass, InitVar

import tinyecs as ecs

from aenum import extend_enum
from pgcooldown import CronD, Cooldown
from tinyecs import EntityID
from tinyecs.compsys import Comp


extend_enum(Comp, 'CROND')
extend_enum(Comp, 'FOLLOWUP')
extend_enum(Comp, 'IS_KILLED')
extend_enum(Comp, 'KILL_WITH_PARENT')
extend_enum(Comp, 'LIFETIME')
extend_enum(Comp, 'TIMER')


@dataclass
class Timer:
    """An optionally repeating timer component.

    :param cooldown: Either a pgcooldown.Cooldown object or a number of seconds
    :param callback: The function to run when the timer fires
    :param repeat: Decides if the timer is reoccurring

    The prototype of the callback function is::

        def callback() -> None:
            ...

    .. note:: If ``repeat`` is false, when using :func:`sys_timer`, the
        component will be removed after it fired.
    """

    cooldown: InitVar[float | Cooldown]
    callback: Callable[[], None]
    repeat: bool = False

    def __post_init__(self, cooldown: Cooldown | float) -> None:
        self.cooldown = cooldown if isinstance(cooldown, Cooldown) else Cooldown(cooldown)


def sys_crond(eid: EntityID, crond: CronD) -> None:
    """Update a pgcooldown.CronD queue.

    :param eid: The entity ID
    :param crond: The schedule queue for the entity.  See :class:`pgcooldown.CronD`

    pgcooldown's ``CronD`` class needs to have its ``update`` method called
    frequently.  Running this system will ensure exactly that.

    """

    crond.update()


def sys_followup(eid: EntityID, is_killed: bool, followup: Callable[[EntityID], None]) -> None:
    """Run a followup function after an entity is marked as dead.

    :param eid: The entity ID
    :param is_killed: The marker component that indicates that this entity is killed
        The existence of this component alone is sufficient, its value is ignored
    :param followup: A callback to run

    The prototype for the callback is::

        def callback(eid: EntityID) -> None:
            ...

    The followup component is removed before the callback is called.
    """

    ecs.remove_component(eid, Comp.FOLLOWUP)
    followup(eid)


def sys_kill_with_parent(eid: EntityID, parent: EntityID):
    """Mark this entity as "killed" if its parent is marked as killed as well.

    :param eid: The entity ID
    :param parent: The parent entity to watch

    Relies on :func:`sys_reap` or your own system to actually remove the entity.
    """

    if ecs.eid_has(parent, Comp.IS_KILLED):
        ecs.add_component(eid, Comp.IS_KILLED, True)


def sys_lifetime(eid: EntityID, lifetime: Cooldown) -> None:
    """Mark the entity as killed if its lifetime has run out.

    :param eid: The entity ID
    :param lifetime: A `pgcooldown.Cooldown` instance

    Relies on :func:`sys_reap` or your own system to actually remove the entity.
    """

    if lifetime.cold():
        ecs.add_component(eid, Comp.IS_KILLED, True)


def sys_reap(eid: EntityID, is_killed: bool) -> None:
    """Remove entities that have a Comp.IS_KILLED component.

    :param eid: The entity ID
    :param is_killed: The marker component that indicates that this entity is killed
        The existence of this component alone is sufficient, its value is ignored

    """

    ecs.remove_entity(eid)


def sys_timer(eid: EntityID, timer: Timer) -> None:
    """Run a callback function after a timer runs out.

    :param eid: The entity ID
    :param timer: A :class:`Timer` object

    .. note:: If timer.repeat is not set, the component is removed after the
        timer has run out.  Otherwise the timer is reset.

    The prototype for the callback is::

        def callback() -> None:
            ...

    """

    if timer.cooldown.cold():
        if timer.repeat:
            timer.cooldown.reset()
        else:
            ecs.remove_component(eid, Comp.TIMER)

        timer.callback()
