from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class OrganizationUnitSchema:
    id: int  # id подразделения
    parent_name: str  # Группа в которую входит подразделение
    name: str  # Наименование подразделения
    data_create: str  # Дата создания подразделения
    full_path: str   # Полный путь подразделения parent_name


@dataclass
class OrganizationUnitADSchema:
    name: str  # Наименование подразделения
    base_code: str  # Кодировка даты создания подразделения
    ou_path: str   # Полный путь подразделения
