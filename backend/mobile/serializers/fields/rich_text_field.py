from rest_framework.fields import JSONField
from django.conf import settings
from utils.web.field_handlers import SUPPORTED_QUILL_BLOB_TYPES


class RichTextField(JSONField):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs, read_only=True)

    def to_representation(self, value):
        if value:
            value = [
                (
                    (
                        {
                            **line,
                            "insert": { blob_key: settings.INTERNET_URL + line['insert'][blob_key] }
                        }
                        if (blob_key := next(filter(lambda k: k in line['insert'], SUPPORTED_QUILL_BLOB_TYPES), None))
                            is not None
                        else { "insert": "\n" }
                    )
                    if isinstance(line['insert'], dict) else line
                )
                for line in value
            ]
        return super().to_representation(value)
    