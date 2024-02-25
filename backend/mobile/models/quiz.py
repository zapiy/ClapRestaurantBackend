from typing import Optional
from uuid import uuid4
from django.db import models
import pendulum

from utils.web.fields import PendulumDateTimeField
from cdn.utils import get_file_url
from cdn.models import FileStoreModel
from .user import MobileUserModel
from utils import SN, SNF
from utils.web.field_handlers import rich_field_converter


class MobileQuizModel(models.Model):
    SN_preview = SN(
        'uuid', "name",
        image = get_file_url(default = "/static/media_defaults/quiz.jpg"),
    )
    
    SN_public = SN(
        'uuid',
        image = get_file_url(default = "/static/media_defaults/quiz.jpg"),
        name = SNF(str, limit=range(1, 100)),
        passing_percentage = SNF(int, limit=range(1, 100)),
        newbie_required = SNF(bool),
        content = rich_field_converter
    )
    
    class Meta:
        db_table = 'mobile_quiz'

    uuid: str = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    image: Optional[FileStoreModel] = models.OneToOneField(FileStoreModel, models.SET_NULL, null=True)
    passing_percentage: int = models.IntegerField(null=False, default=100)

    name: str = models.CharField(max_length=100, null=False)
    content: Optional[dict] = models.JSONField(null=True)
    newbie_required: bool = models.BooleanField(null=False, default=False)
    
    created_at: pendulum.DateTime = PendulumDateTimeField(auto_now_add=True)
    
    questions: models.QuerySet['MobileQuizQuestionModel']
    user_sprints: models.QuerySet['MobileQuizUserSprintModel']


class MobileQuizQuestionModel(models.Model):
    class Meta:
        db_table = 'mobile_quiz_question'
        
    class Type(models.TextChoices):
        OPTION = "option"
        TEXT = "text"

    SN_public = SN(
        'uuid', 'created_at',
        name = SNF(str, limit=range(1, 100)),
        type = SNF(str, validate=lambda v: v in MobileQuizQuestionModel.Type.values),
        description = SNF(str, null=True, limit=range(0, 1000)),
        image = get_file_url(default = "/static/media_defaults/quiz.jpg"),
        answers = SN('$public'),
    )

    uuid: str = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    quiz: MobileQuizModel = models.ForeignKey(
        MobileQuizModel, models.CASCADE, 
        null=False, related_name="questions"
    )
    
    name: str = models.CharField(max_length=100, null=False)
    image: Optional[FileStoreModel] = models.OneToOneField(FileStoreModel, models.SET_NULL, null=True)
    
    description: Optional[str] = models.TextField(max_length=1000, null=True)
    
    type: Type = models.CharField(
        max_length=20,
        choices=Type.choices,
        default=Type.TEXT,
    )
    
    created_at: pendulum.DateTime = PendulumDateTimeField(auto_now_add=True)
    
    answers: models.QuerySet['MobileQuizAnswerModel']
    correct_answer: Optional['MobileQuizAnswerModel'] = models.ForeignKey(
        'MobileQuizAnswerModel', models.SET_NULL, null=True)
    
    user_answers: models.QuerySet['MobileQuizUserAnswerModel']


class MobileQuizAnswerModel(models.Model):
    SN_public = SN('uuid', 'name')
    
    class Meta:
        db_table = 'mobile_quiz_answer'

    uuid: str = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    name: str = models.CharField(max_length=100, null=False)
    question: 'MobileQuizQuestionModel' = models.ForeignKey(
        MobileQuizQuestionModel, models.CASCADE,
        null=False, related_name="answers"
    )


class MobileQuizUserSprintModel(models.Model):
    SN_public = SN(
        'uuid', "status", "finished_at", "created_at",
        quiz_image = ("quiz", 
            lambda val: get_file_url("/static/media_defaults/quiz.jpg")(val.image)),
        user_image = ("user", 
            lambda val: get_file_url("/static/media_defaults/avatar.jpg")(val.avatar)),
        user = ("user", lambda val: val.full_name),
        quiz = ("quiz", lambda val: val.name),
    )
    
    class Meta:
        db_table = 'mobile_quiz_user_sprint'
    
    class Status(models.TextChoices):
        WHILE_TAKING = "while_taking"
        ON_VERIFICATION = "on_verification"
        CORRECT = "correct"
        INCORRENT = "incorrect"
    
    uuid: str = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    quiz: MobileQuizModel = models.ForeignKey(
        MobileQuizModel, models.CASCADE, 
        null=False, related_name="user_sprints"
    )
    
    user: MobileUserModel = models.ForeignKey(
        MobileUserModel, models.CASCADE, 
        null=False, related_name="quiz_sprints"
    )
    
    status: Status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.WHILE_TAKING,
    )
    
    finished_at: Optional[pendulum.DateTime] = PendulumDateTimeField(null=True)
    created_at: pendulum.DateTime = PendulumDateTimeField(auto_now_add=True)
    
    answers: models.QuerySet['MobileQuizUserAnswerModel']
    
    
class MobileQuizUserAnswerModel(models.Model):
    SN_public = SN(
        'uuid', 'text_answer', "status",
        question = SN(
            '$public', 
            correct_answer = SN('$public'),
        ),
        option_answer = SN('$public'),
    )
    
    class Meta:
        db_table = 'mobile_quiz_user_answer'
    
    class Status(models.TextChoices):
        ON_VERIFICATION = "on_verification"
        INCORRENT = "incorrect"
        CORRECT = "correct"
    
    uuid: str = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    
    sprint: MobileQuizUserSprintModel = models.ForeignKey(
        MobileQuizUserSprintModel, models.CASCADE, 
        null=False, related_name="answers"
    )
    question: MobileQuizQuestionModel = models.ForeignKey(
        MobileQuizQuestionModel, models.CASCADE,
        null=False, related_name="user_answers"
    )
    
    status: Status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ON_VERIFICATION,
    )
    
    text_answer: Optional[str] = models.TextField(null=True, max_length=1000)
    option_answer: Optional[MobileQuizAnswerModel] = models.ForeignKey(
        MobileQuizAnswerModel, models.CASCADE, null=True)
    
    updated_at: pendulum.DateTime = PendulumDateTimeField(auto_now=True)
    
