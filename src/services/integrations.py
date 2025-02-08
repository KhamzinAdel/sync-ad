from src.services.database import UserComputerService, BranchService
from active_directory import ADService


class IntegrationService:

    @classmethod
    def create_and_update_uo(cls, ou_id: int) -> str:
        ou_name = UserComputerService.get_user_computer_by_id(ou_id)

        if not ou_name:
            return f"Error: Не найдено ни одной записи с идентификатором {ou_id}"

        result = ADService.create_ou(ou_name)

        return result

    @classmethod
    def create_and_update_branches(cls, ou_id: int, ou_name: str) -> str:
        branches = BranchService.get_branches(ou_id)

        if not branches:
            return f"Error: Не найдено ни одной записи по идентификатором {ou_id}"

        result = ADService.add_branches_to_ou(ou_name, branches)

        return result

    @classmethod
    def check_ou(cls, ou_name: str) -> str:
        return ADService.check_ou_exists(ou_name)


def main():
    #create_ou = IntegrationService.create_and_update_uo(1)  # Создание университета
    #create_branches = IntegrationService.create_and_update_branches(1, create_ou)  # Создание филилов
    check_ou = IntegrationService.check_ou('Университет')  # Проверка существования
    #print(create_ou)
    #print(create_branches)
    print(check_ou)


if __name__ == '__main__':
    main()
