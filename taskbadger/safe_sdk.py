import logging
from typing import Optional

try:
    from typing import ParamSpec
except ImportError:
    from typing_extensions import ParamSpec

from .mug import Badger
from .sdk import Task, create_task, update_task

P = ParamSpec("P")

log = logging.getLogger("taskbadger")


def create_task_safe(name: str, **kwargs: P.kwargs) -> Optional[Task]:
    """Safely create a task. Any errors are handled and logged.

    Arguments:
        name: The name of the task.
        **kwargs: See [taskbadger.create_task][]

    Returns:
        The created task or None
    """
    if not Badger.is_configured():
        return None

    try:
        return create_task(name, **kwargs)
    except Exception:
        log.exception("Error creating task '%s'", name)


def update_task_safe(task_id: str, **kwargs: P.kwargs) -> Optional[Task]:
    """Safely update a task. Any errors are handled and logged.

    Arguments:
        task_id: The ID of the task to update.
        **kwargs: See [taskbadger.update_task][]

    Returns:
        The updated task or None
    """
    if not Badger.is_configured():
        return

    try:
        return update_task(task_id, **kwargs)
    except Exception:
        log.exception("Error updating task '%s'", task_id)
