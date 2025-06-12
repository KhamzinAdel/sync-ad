from dataclasses import dataclass


@dataclass
class OrganizationUnitListSchema:
    id: int
    parent_name: str
    name: str
    data_create: str
    full_path: str


@dataclass
class OrganizationUnitSchema:
    ou_uuid: str


@dataclass
class OrganizationUnitADSchema:
    name: str
    base_code: str
    ou_path: str
