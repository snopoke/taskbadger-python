from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.task import Task
from ...models.task_request import TaskRequest
from ...types import Response


def _get_kwargs(
    organization_slug: str,
    project_slug: str,
    id: str,
    *,
    json_body: TaskRequest,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "put",
        "url": "/api/{organization_slug}/{project_slug}/tasks/{id}/".format(
            organization_slug=organization_slug,
            project_slug=project_slug,
            id=id,
        ),
        "json": json_json_body,
    }


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Task]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Task.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Task]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    organization_slug: str,
    project_slug: str,
    id: str,
    *,
    client: AuthenticatedClient,
    json_body: TaskRequest,
) -> Response[Task]:
    """Update Task

     Update a task

    Args:
        organization_slug (str):
        project_slug (str):
        id (str):
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
        id=id,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    organization_slug: str,
    project_slug: str,
    id: str,
    *,
    client: AuthenticatedClient,
    json_body: TaskRequest,
) -> Optional[Task]:
    """Update Task

     Update a task

    Args:
        organization_slug (str):
        project_slug (str):
        id (str):
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
        id=id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    organization_slug: str,
    project_slug: str,
    id: str,
    *,
    client: AuthenticatedClient,
    json_body: TaskRequest,
) -> Response[Task]:
    """Update Task

     Update a task

    Args:
        organization_slug (str):
        project_slug (str):
        id (str):
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
        id=id,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    organization_slug: str,
    project_slug: str,
    id: str,
    *,
    client: AuthenticatedClient,
    json_body: TaskRequest,
) -> Optional[Task]:
    """Update Task

     Update a task

    Args:
        organization_slug (str):
        project_slug (str):
        id (str):
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
            id=id,
            client=client,
            json_body=json_body,
        )
    ).parsed
