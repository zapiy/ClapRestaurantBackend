from django.conf import settings
from .handle_post_fields import SUPPORTED_QUILL_BLOB_TYPES


def rich_field_converter(value):
    if value is None:
        return None
    
    return [
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
