import os
from typing import get_type_hints, Union
from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__))

dotenv_path = os.path.join(BASEDIR, '.env')
load_dotenv(dotenv_path)


class AppConfigError(Exception):
    pass


def _parse_bool(val: Union[str, bool]) -> bool:
    return val if type(val) == bool else val.lower() in ['true', 'yes', '1']


class Config:
    EXCEL_FILE_PATH: str = os.getenv("EXCEL_FILE_PATH")
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")
    REDIS_HOST: str = os.getenv("REDIS_HOST")
    CACHE_METHOD: str = "file"
    JSON_FILE_NAME: str = "temp.json"

    def __init__(self, env):
        for field in self.__annotations__:
            if not field.isupper():
                continue

            default_value = getattr(self, field, None)
            if default_value is None and env.get(field) is None:
                raise AppConfigError('The {} field is required'.format(field))

            try:
                var_type = get_type_hints(Config)[field]
                if var_type == bool:
                    value = _parse_bool(env.get(field, default_value))
                else:
                    value = var_type(env.get(field, default_value))

                self.__setattr__(field, value)
            except ValueError:
                raise AppConfigError('Unable to cast value of "{}" to type "{}" for "{}" field'.format(
                    env[field],
                    var_type,
                    field
                ))


config: Config = Config(os.environ)
