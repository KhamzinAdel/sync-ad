from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class OrganizationUnitSchema:
    id: int  # id подразделения
    parent_name: Optional[str]  # Группа в которую входит подразделение
    name: str  # Наименование подразделения
    data_create: Optional[datetime]  # Дата создания подразделения
    full_path: str   # Полный путь подразделения parent_name


@dataclass
class OrganizationUnitADSchema:
    name: str  # Наименование подразделения
    base_code: str  # Кодировка даты создания подразделения
    ou_path: str   # Полный путь подразделения
