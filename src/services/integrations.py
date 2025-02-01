import asyncio

from src.services.database import UserComputerService, BranchService
from active_directory import ADService


class IntegrationService:

    @classmethod
    async def process_and_update_uo(cls, ou_id: int) -> str:
        ou_name = await UserComputerService.get_user_computer_by_id(ou_id)

        if not ou_name:
            return f"Error: Не найдено ни одной записи с идентификатором {ou_id}"

        result = await ADService.create_ou(ou_name)

        return result

    @classmethod
    async def process_and_update_branches(cls, ou_id: int, ou_name: str) -> str:
        branches = await BranchService.get_branches(ou_id)

        if not branches:
            return f"Error: Не найдено ни одной записи по идентификатором {ou_id}"

        result = await ADService.add_branches_to_ou(ou_name, branches)

        return result


async def main():
    create_ou = await IntegrationService.process_and_update_uo(1)  # Создание университета
    create_branches = await IntegrationService.process_and_update_branches(1, create_ou)  # Создание филилов
    print(create_ou)
    print(create_branches)


if __name__ == '__main__':
    result = asyncio.run(main())
