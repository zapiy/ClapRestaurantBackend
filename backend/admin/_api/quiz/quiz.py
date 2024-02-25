from mobile.models import MobileQuizModel
from mobile.app_messaging import AppMessaging
from utils.web.field_handlers import generate_admin_item_view, FieldType
from .const import ensure_check_newbie


async def on_deleted_quiz(model: MobileQuizModel):
    await ensure_check_newbie()


quiz = generate_admin_item_view(
    MobileQuizModel,
    on_added=AppMessaging.new_quiz,
    on_deleted=on_deleted_quiz,
    extra_mapping={
        "image": FieldType.IMAGE,
        "content": FieldType.RICH,
    },
)
