import json
import os


class MemoryService:

    FILE_PATH = "data/user_preferences.json"

    @staticmethod
    def get_preferences():

        if not os.path.exists(MemoryService.FILE_PATH):
            return {}

        try:

            with open(MemoryService.FILE_PATH, "r") as file:

                content = file.read()

                if not content.strip():
                    return {}

                return json.loads(content)

        except Exception:
            return {}

    @staticmethod
    def save_preferences(new_data):

        data = MemoryService.get_preferences()

        data.update(new_data)

        os.makedirs(
            os.path.dirname(MemoryService.FILE_PATH),
            exist_ok=True
        )

        with open(
            MemoryService.FILE_PATH,
            "w"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

        return data

    @staticmethod
    def clear():

        if os.path.exists(
            MemoryService.FILE_PATH
        ):
            os.remove(
                MemoryService.FILE_PATH
            )