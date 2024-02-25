from django.db.models import DateField, TimeField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from datetime import datetime, date, time
import pendulum

DATE_FORMAT = "YYYY-MM-DD"
TIME_FORMAT = "HH:mm:ss" # HH:mm:ss.SSSSSS+zz:zz

UNZONED_ISO_FORMAT = "YYYY-MM-DD HH:mm:ss.SSSSSS"
ISO_FORMAT = "YYYY-MM-DD HH:mm:ss.SSSSSS+zz:zz"

class PendulumDateField(DateField):
    empty_strings_allowed = False
    description = _("Pendulum Date (without time)")

    def get_internal_type(self):
        return "DateField"

    def to_python(self, value: str) -> pendulum.Date:
        if value is None:
            return None
        if isinstance(value, (date, datetime)):
            value = pendulum.instance(value)
        if type(value) == pendulum.DateTime:
            value = value.date()
        if type(value) == pendulum.Date:
            return value

        try:
            parsed = pendulum.from_format(value, DATE_FORMAT)
            if parsed is not None:
                return parsed
        except:
            pass

        raise ValidationError(
            f"Database value '{value}' is not a valid date",
            code="invalid",
            params={"value": value},
        )

    def get_prep_value(self, value):
        return self.to_python(value)
    
    def pre_save(self, model_instance, add):
        if self.auto_now or (self.auto_now_add and add):
            value = pendulum.today().date()
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super().pre_save(model_instance, add)

    def value_to_string(self, obj):
        val: pendulum.Date = self.value_from_object(obj)
        return "" if val is None else val.format(DATE_FORMAT)


class PendulumDateTimeField(PendulumDateField):
    description = _("Pendulum Date (with time)")

    def get_internal_type(self):
        return "DateTimeField"

    def to_python(self, value):
        if value is None:
            return None
        if isinstance(value, datetime):
            value = pendulum.instance(value)
        if type(value) == pendulum.Date:
            value = pendulum.DateTime(value.year, value.month, value.day)
        if type(value) == pendulum.DateTime:
            if not settings.USE_TZ:
                value = value.replace(tzinfo=None)
            return value
        
        try:
            parsed = pendulum.from_format(
                value, (ISO_FORMAT if settings.USE_TZ else UNZONED_ISO_FORMAT), 
                tz = (pendulum.tz.UTC if settings.USE_TZ else None)
            )
            if parsed is not None:
                return parsed
        except:
            pass
        
        raise ValidationError(
            f"Database value '{value}' is not a valid datetime",
            code="invalid",
            params={"value": value},
        )

    def pre_save(self, model_instance, add):
        if self.auto_now or (self.auto_now_add and add):
            value = pendulum.now()
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super().pre_save(model_instance, add)

    def get_prep_value(self, value):
        return self.to_python(value)

    def get_db_prep_value(self, value, connection, prepared=False):
        if not prepared:
            value = self.get_prep_value(value)
        return connection.ops.adapt_datetimefield_value(value)

    def value_to_string(self, obj):
        val: pendulum.DateTime = self.value_from_object(obj)
        return "" if val is None else (
            val.isoformat() 
            if settings.USE_TZ else
            val.format(UNZONED_ISO_FORMAT)
        )


class PendulumTimeField(TimeField):
    empty_strings_allowed = False
    description = _("Pendulum Time")

    def get_internal_type(self):
        return "TimeField"

    def to_python(self, value):
        if value is None:
            return None
        if isinstance(value, (time, datetime)):
            value = pendulum.instance(value)
        if type(value) == pendulum.DateTime:
            value = value.time()
        if type(value) == pendulum.Time:
            return value

        try:
            parsed = pendulum.from_format(value, TIME_FORMAT)
            if parsed is not None:
                return parsed
        except:
            pass

        raise ValidationError(
            f"Database value '{value}' is not a valid time",
            code="invalid",
            params={"value": value},
        )

    def pre_save(self, model_instance, add):
        if self.auto_now or (self.auto_now_add and add):
            value = pendulum.now().time()
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super().pre_save(model_instance, add)

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        return self.to_python(value)

    def get_db_prep_value(self, value, connection, prepared=False):
        if not prepared:
            value = self.get_prep_value(value)
        return connection.ops.adapt_timefield_value(value)

    def value_to_string(self, obj):
        val: pendulum.Time = self.value_from_object(obj)
        return "" if val is None else val.format(TIME_FORMAT)
