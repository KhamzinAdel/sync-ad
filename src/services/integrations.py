from repositories import ADRepository, DataRepository


class IntegrationService:

    def __init__(self):
        self.active_directory: ADRepository = ADRepository()
        self.data: DataRepository = DataRepository()

    def create_and_update_uo(self, ou_id: int) -> str:
        ou_name = self.data.get_user_computer_by_id(ou_id)

        if not ou_name:
            return f"Error: Не найдено ни одной записи с идентификатором {ou_id}"

        result = self.active_directory.create_ou(ou_name)

        return result

    def create_and_update_branches(self, ou_id: int, ou_name: str) -> str:
        branches = self.data.get_branches(ou_id)

        if not branches:
            return f"Error: Не найдено ни одной записи по идентификатором {ou_id}"

        result = self.active_directory.add_branches_to_ou(ou_name, branches)

        return result

    def check_ou(self, ou_name: str) -> str:
        return self.active_directory.check_ou_exists(ou_name)


#def main():
#    integration = IntegrationService()
#    create_ou = integration.create_and_update_uo(1)  # Создание университета
#    create_branches = integration.create_and_update_branches(1, create_ou)  # Создание филилов
#     check_ou = integration.check_ou('Университет')  # Проверка существования
#     print(create_ou)
#     print(create_branches)
#     print(check_ou)


#if __name__ == '__main__':
#    main()
