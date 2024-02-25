from third_party import Configurator
from django.conf import settings


config = Configurator(
    settings.BASE_DIR / "conf" / "conf.json",
    default={
        "password": 'qwerty123',
    }
)
