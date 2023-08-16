from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.task import Task
from ...models.task_request import TaskRequest
from ...types import UNSET, Response, Unset


def _get_kwargs(
    organization_slug: str,
    project_slug: str,
    *,
    client: AuthenticatedClient,
    json_body: TaskRequest,
    x_taskbadger_monitor: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/{organization_slug}/{project_slug}/tasks/".format(
        client.base_url, organization_slug=organization_slug, project_slug=project_slug
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(x_taskbadger_monitor, Unset):
        headers["X-TASKBADGER-MONITOR"] = x_taskbadger_monitor

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": json_json_body,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Task]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = Task.from_dict(response.json())

        return response_201
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Task]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    organization_slug: str,
    project_slug: str,
    *,
    client: AuthenticatedClient,
    json_body: TaskRequest,
    x_taskbadger_monitor: Union[Unset, str] = UNSET,
) -> Response[Task]:
    """Create Task

     Create a task

    Args:
        organization_slug (str):
        project_slug (str):
        x_taskbadger_monitor (Union[Unset, str]):
        json_body (TaskRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Task]
    """

    kwargs = _get_kwargs(
        organization_slug=organization_slug,
        project_slug=project_slug,
        client=client,
        json_body=json_body,
        x_taskbadger_monitor=x_taskbadger_monitor,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    organization_slug: str,
    project_slug: str,
    *,
    client: AuthenticatedClient,
    json_body: TaskRequest,
    x_taskbadger_monitor: Union[Unset, str] = UNSET,
) -> Optional[Task]:
    """Create Task

     Create a task

    Args:
        organization_slug (str):
        project_slug (str):
        x_taskbadger_monitor (Union[Unset, str]):
        json_body (TaskRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Task
    """

    return sync_detailed(
        organization_slug=organization_slug,
        project_slug=project_slug,
        client=client,
        json_body=json_body,
        x_taskbadger_monitor=x_taskbadger_monitor,
    ).parsed


async def asyncio_detailed(
    organization_slug: str,
    project_slug: str,
    *,
    client: AuthenticatedClient,
    json_body: TaskRequest,
    x_taskbadger_monitor: Union[Unset, str] = UNSET,
) -> Response[Task]:
    """Create Task

     Create a task

    Args:
        organization_slug (str):
        project_slug (str):
        x_taskbadger_monitor (Union[Unset, str]):
        json_body (TaskRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Task]
    """

    kwargs = _get_kwargs(
        organization_slug=organization_slug,
        project_slug=project_slug,
        client=client,
        json_body=json_body,
        x_taskbadger_monitor=x_taskbadger_monitor,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    organization_slug: str,
    project_slug: str,
    *,
    client: AuthenticatedClient,
    json_body: TaskRequest,
    x_taskbadger_monitor: Union[Unset, str] = UNSET,
) -> Optional[Task]:
    """Create Task

     Create a task

    Args:
        organization_slug (str):
        project_slug (str):
        x_taskbadger_monitor (Union[Unset, str]):
        json_body (TaskRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Task
    """

    return (
        await asyncio_detailed(
            organization_slug=organization_slug,
            project_slug=project_slug,
            client=client,
            json_body=json_body,
            x_taskbadger_monitor=x_taskbadger_monitor,
        )
    ).parsed
