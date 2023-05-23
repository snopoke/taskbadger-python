import dataclasses
import os
from typing import List

from _contextvars import ContextVar

from taskbadger import Action
from taskbadger.exceptions import ConfigurationError
from taskbadger.internal import AuthenticatedClient, errors
from taskbadger.internal.api.task_endpoints import task_create, task_get, task_partial_update
from taskbadger.internal.models import (
    PatchedTaskRequest,
    PatchedTaskRequestData,
    StatusEnum,
    TaskRequest,
    TaskRequestData,
)
from taskbadger.internal.types import UNSET

_local = ContextVar("taskbadger_client")

_TB_HOST = "https://taskbadger.net"


def init(organization_slug: str = None, project_slug: str = None, token: str = None):
    """Initialize Task Badger client

    Call this function once per thread
    """
    _init(_TB_HOST, organization_slug, project_slug, token)


def _init(host: str = None, organization_slug: str = None, project_slug: str = None, token: str = None):
    host = host or os.environ.get("TASKBADGER_HOST", "https://taskbadger.net")
    organization_slug = organization_slug or os.environ.get("TASKBADGER_ORG")
    project_slug = project_slug or os.environ.get("TASKBADGER_PROJECT")
    token = token or os.environ.get("TASKBADGER_API_KEY")

    if host and organization_slug and project_slug and token:
        client = AuthenticatedClient(host, token)
        settings = Settings(client, organization_slug, project_slug)
        Mug.current.bind(settings)
    else:
        raise ConfigurationError(
            host=host,
            organization_slug=organization_slug,
            project_slug=project_slug,
            token=token,
        )


def get_task(task_id: str) -> "Task":
    """Fetch a Task from the API based on its ID.

    Arguments:
        task_id: The ID of the task to fetch.
    """
    return Task(task_get.sync(**_make_args(id=task_id)))


def create_task(
    name: str,
    status: StatusEnum = StatusEnum.PENDING,
    value: int = None,
    value_max: int = None,
    data: dict = None,
    max_runtime: int = None,
    stale_timeout: int = None,
    actions: List[Action] = None,
    monitor_id: str = None,
) -> "Task":
    """Create a Task.

    Arguments:
        name: The name of the task.
        status: The task status.
        value: The current 'value' of the task.
        value_max: The maximum value the task is expected to achieve.
        data: Custom task data.
        max_runtime: Maximum expected runtime (minutes).
        stale_timeout: Maximum allowed time between updates (minutes).
        actions: Task actions.
        monitor_id: ID of the monitor to associate this task with.

    Returns:
        Task: The created Task object.
    """
    value = _none_to_unset(value)
    value_max = _none_to_unset(value_max)
    data = _none_to_unset(data)
    max_runtime = _none_to_unset(max_runtime)
    stale_timeout = _none_to_unset(stale_timeout)

    task = TaskRequest(
        name=name, status=status, value=value, value_max=value_max, max_runtime=max_runtime, stale_timeout=stale_timeout
    )
    if data:
        task.data = TaskRequestData.from_dict(data)
    if actions:
        task.additional_properties = {"actions": [a.to_dict() for a in actions]}
    kwargs = _make_args(json_body=task)
    if monitor_id:
        kwargs["x_taskbadger_monitor"] = monitor_id
    response = task_create.sync_detailed(**kwargs)
    _check_response(response)
    return Task(response.parsed)


def update_task(
    task_id: str,
    name: str = None,
    status: StatusEnum = None,
    value: int = None,
    value_max: int = None,
    data: dict = None,
    max_runtime: int = None,
    stale_timeout: int = None,
    actions: List[Action] = None,
) -> "Task":
    """Update a task.
    Requires only the task ID and fields to update.

    Arguments:
        task_id: The ID of the task to update.
        name: The name of the task.
        status: The task status.
        value: The current 'value' of the task.
        value_max: The maximum value the task is expected to achieve.
        data: Custom task data.
        max_runtime: Maximum expected runtime (minutes).
        stale_timeout: Maximum allowed time between updates (minutes).
        actions: Task actions.

    Returns:
        Task: The updated Task object.
    """
    name = _none_to_unset(name)
    status = _none_to_unset(status)
    value = _none_to_unset(value)
    value_max = _none_to_unset(value_max)
    data = _none_to_unset(data)
    max_runtime = _none_to_unset(max_runtime)
    stale_timeout = _none_to_unset(stale_timeout)

    data = UNSET if not data else PatchedTaskRequestData.from_dict(data)
    body = PatchedTaskRequest(
        name=name,
        status=status,
        value=value,
        value_max=value_max,
        data=data,
        max_runtime=max_runtime,
        stale_timeout=stale_timeout,
    )
    if actions:
        body.additional_properties = {"actions": [a.to_dict() for a in actions]}
    kwargs = _make_args(id=task_id, json_body=body)
    response = task_partial_update.sync_detailed(**kwargs)
    _check_response(response)
    return Task(response.parsed)


def _make_args(**kwargs):
    settings = Mug.current.settings
    ret_args = dataclasses.asdict(settings)
    ret_args.update(kwargs)
    return ret_args


def _get_settings():
    return _local.get()


def _check_response(response):
    if 200 <= response.status_code < 300:
        return response

    else:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}", response.content)


@dataclasses.dataclass
class Settings:
    client: AuthenticatedClient
    organization_slug: str
    project_slug: str


class MugMeta(type):
    @property
    def current(cls):
        mug = _local.get(None)
        if mug is None:
            mug = Mug(GLOBAL_MUG)
            _local.set(mug)
        return mug


class Mug(metaclass=MugMeta):
    def __init__(self, settings_or_mug=None):
        if isinstance(settings_or_mug, Mug):
            self.settings = settings_or_mug.settings
        else:
            self.settings = settings_or_mug

    def bind(self, settings):
        self.settings = settings

    def is_configured(self):
        return self.settings is not None


GLOBAL_MUG = Mug()
_local.set(GLOBAL_MUG)


class Task:
    """The Task class provides a convenient Python API to interact
    with Task Badger tasks.
    """

    @classmethod
    def get(cls, task_id: str) -> "Task":
        """Get an existing task"""
        return get_task(task_id)

    @classmethod
    def create(
        cls,
        name: str,
        status: StatusEnum = StatusEnum.PENDING,
        value: int = None,
        value_max: int = None,
        data: dict = None,
        max_runtime: int = None,
        stale_timeout: int = None,
        actions: List[Action] = None,
        monitor_id: str = None,
    ) -> "Task":
        """Create a new task"""
        return create_task(
            name,
            status,
            value,
            value_max,
            data,
            max_runtime=max_runtime,
            stale_timeout=stale_timeout,
            actions=actions,
            monitor_id=monitor_id,
        )

    def __init__(self, task):
        self._task = task

    def pre_processing(self):
        """Update the task status to `pre_processing`."""
        self.update_status(StatusEnum.PRE_PROCESSING)

    def starting(self):
        """Update the task status to `pre_processing` and set the value to `0`."""
        self.processing(value=0)

    def processing(self, value: int = None):
        """Update the task status to `processing` and set the value."""
        self.update(status=StatusEnum.PROCESSING, value=value)

    def post_processing(self, value: int = None):
        """Update the task status to `post_processing` and set the value."""
        self.update(status=StatusEnum.POST_PROCESSING, value=value)

    def success(self, value: int = None):
        """Update the task status to `success` and set the value."""
        self.update(status=StatusEnum.SUCCESS, value=value)

    def error(self, value: int = None, data: dict = None):
        """Update the task status to `error` and set the value and data."""
        self.update(status=StatusEnum.ERROR, value=value, data=data)

    def canceled(self):
        """Update the task status to `cancelled`"""
        self.update_status(StatusEnum.CANCELLED)

    def update_status(self, status: StatusEnum):
        """Update the task status"""
        self.update(status=status)

    def increment_progress(self, amount: int):
        """Increment the task progress.
        If the task value is not set it will be set to `amount`.
        """
        value = self._task.value
        value_norm = value if value is not UNSET and value is not None else 0
        new_amount = value_norm + amount
        self.update(value=new_amount)

    def update_progress(self, value: int):
        """Update task progress."""
        self.update(value=value)

    def set_value_max(self, value_max: int):
        """Set the `value_max`."""
        self.update(value_max=value_max)

    def update(
        self,
        name: str = None,
        status: StatusEnum = None,
        value: int = None,
        value_max: int = None,
        data: dict = None,
        max_runtime: int = None,
        stale_timeout: int = None,
        actions: List[Action] = None,
    ):
        """Generic update method used to update any of the task fields.

        This can also be used to add actions.
        """
        task = update_task(
            self._task.id,
            name=name,
            status=status,
            value=value,
            value_max=value_max,
            data=data,
            max_runtime=max_runtime,
            stale_timeout=stale_timeout,
            actions=actions,
        )
        self._task = task._task

    def add_actions(self, actions: List[Action]):
        """Add actions to the task."""
        self.update(actions=actions)

    def ping(self):
        """Update the task without changing any values. This can be used in conjunction
        with 'stale_timeout' to indicate that the task is still running."""
        self.update()

    @property
    def data(self):
        return self._task.data.additional_properties

    def __getattr__(self, item):
        return getattr(self._task, item)


def _none_to_unset(value):
    return UNSET if value is None else value
