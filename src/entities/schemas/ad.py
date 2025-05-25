import uuid
from typing import Optional
from dataclasses import dataclass


@dataclass
class ADSchema:
    ou_name: str
    ou_path: str
    ou_uuid: Optional[uuid.UUID] = None


@dataclass
class ADGuidSchema:
    guid: str
