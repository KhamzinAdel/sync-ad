from dataclasses import dataclass


@dataclass
class ADGroupSchema:
    group_name: str
    group_dn: str


@dataclass
class ADParentGroupSchema:
    parent_groups_dn: list[tuple]
