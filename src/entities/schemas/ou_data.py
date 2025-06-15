from dataclasses import dataclass
from datetime import datetime


@dataclass
class OrganizationUnitListSchema:
    id: int
    parent_name: str
    name: str
    date_create: datetime
    full_path: str


@dataclass
class OrganizationUnitSchema:
    ou_uuid: str


@dataclass
class OrganizationUnitADSchema:
    name: str
    date_create: datetime
    ou_path: str
