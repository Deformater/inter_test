from decouple import config


class Settings:
    YANDEX_MAP_API = config("YANDEX_MAP_API", cast=str)
    YANDEX_MAP_API_BASE_URL = config("YANDEX_MAP_API_BASE_URL", cast=str)

    TOMORROW_IO_API_BASE_URL = config("TOMORROW_IO_API_BASE_URL", cast=str)
    TOMORROW_IO_API_KEY = config("TOMORROW_IO_API_KEY", cast=str)

    WEATHERBIT_API_KEY = config("WEATHERBIT_API_KEY", cast=str)
    WEATHERBIT_API_BASE_URL = config("WEATHERBIT_API_BASE_URL", cast=str)
