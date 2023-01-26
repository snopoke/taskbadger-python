import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.status_enum import StatusEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.task_data import TaskData


T = TypeVar("T", bound="Task")


@attr.s(auto_attribs=True)
class Task:
    """
    Attributes:
        id (str): Task ID
        organization (str):
        project (str):
        created (datetime.datetime):
        updated (datetime.datetime):
        name (Union[Unset, None, str]): Name of the task
        status (Union[Unset, StatusEnum]):  Default: StatusEnum.PENDING.
        value (Union[Unset, None, int]): Current progress value
        value_percent (Optional[int]):
        data (Union[Unset, None, TaskData]): Custom metadata
    """

    id: str
    organization: str
    project: str
    created: datetime.datetime
    updated: datetime.datetime
    value_percent: Optional[int]
    name: Union[Unset, None, str] = UNSET
    status: Union[Unset, StatusEnum] = StatusEnum.PENDING
    value: Union[Unset, None, int] = UNSET
    data: Union[Unset, None, "TaskData"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        organization = self.organization
        project = self.project
        created = self.created.isoformat()

        updated = self.updated.isoformat()

        name = self.name
        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        value = self.value
        value_percent = self.value_percent
        data: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.data, Unset):
            data = self.data.to_dict() if self.data else None

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "organization": organization,
                "project": project,
                "created": created,
                "updated": updated,
                "value_percent": value_percent,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if status is not UNSET:
            field_dict["status"] = status
        if value is not UNSET:
            field_dict["value"] = value
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.task_data import TaskData

        d = src_dict.copy()
        id = d.pop("id")

        organization = d.pop("organization")

        project = d.pop("project")

        created = isoparse(d.pop("created"))

        updated = isoparse(d.pop("updated"))

        name = d.pop("name", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, StatusEnum]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = StatusEnum(_status)

        value = d.pop("value", UNSET)

        value_percent = d.pop("value_percent")

        _data = d.pop("data", UNSET)
        data: Union[Unset, None, TaskData]
        if _data is None:
            data = None
        elif isinstance(_data, Unset):
            data = UNSET
        else:
            data = TaskData.from_dict(_data)

        task = cls(
            id=id,
            organization=organization,
            project=project,
            created=created,
            updated=updated,
            name=name,
            status=status,
            value=value,
            value_percent=value_percent,
            data=data,
        )

        task.additional_properties = d
        return task

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
