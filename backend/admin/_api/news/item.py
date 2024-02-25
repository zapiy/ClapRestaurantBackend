from mobile.models import MobileNewsModel
from mobile.app_messaging import AppMessaging
from utils.web.field_handlers import generate_admin_item_view, FieldType


news = generate_admin_item_view(
    MobileNewsModel,
    on_added=AppMessaging.new_news,
    extra_mapping={
        "image": FieldType.IMAGE,
        "content": FieldType.RICH,
    },
)
