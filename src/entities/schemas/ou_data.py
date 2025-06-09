from dataclasses import dataclass


@dataclass
class OrganizationUnitListSchema:
    id: int  # id подразделения
    parent_name: str  # Группа в которую входит подразделение
    name: str  # Наименование подразделения
    data_create: str  # Дата создания подразделения
    full_path: str   # Полный путь подразделения parent_name


@dataclass
class OrganizationUnitSchema:
    ou_uuid: str  # uuid подразделения


@dataclass
class OrganizationUnitADSchema:
    name: str  # Наименование подразделения
    base_code: str  # Кодировка даты создания подразделения
    ou_path: str   # Полный путь подразделения
