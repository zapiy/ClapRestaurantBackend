from third_party import FirebaseMessaging
from .models import *


class AppMessaging:
    EVENTS_TOPIC = "events"
    
    class Events:
        NEW_NEWS = "new_news"
        NEW_FOOD = "new_food"
        NEW_QUIZ = "new_quiz"
        NEWBIE_PROMOTION = "newbie_promotion"
        LOGOUT = "logout"
    
    
    @classmethod
    async def newbie_promotion(cls, user: MobileUserModel):
        await FirebaseMessaging.send_topic_message(
            topic=cls.user_topic_key(user),
            type=cls.Events.NEWBIE_PROMOTION,
        )
        
        tokens = set(user.sessions.values_list("fcm_token", flat=True))
        if tokens:
            await FirebaseMessaging.subscribe_to_topic(
                *tokens,
                topic=cls.EVENTS_TOPIC
            )
        
    @classmethod
    async def new_news(cls, news: MobileNewsModel):
        await FirebaseMessaging.send_topic_message(
            topic=cls.EVENTS_TOPIC,
            type=cls.Events.NEW_NEWS,
            data={
                "uuid": str(news.uuid),
                "name": news.name,
            }
        )
        
    @classmethod
    async def new_food(cls, food: MobileFoodModel):
        await FirebaseMessaging.send_topic_message(
            topic=cls.EVENTS_TOPIC,
            type=cls.Events.NEW_FOOD,
            data={
                "uuid": str(food.uuid),
                "name": food.name,
                "category": food.category.name,
            }
        )
        
    @classmethod
    async def new_quiz(cls, quiz: MobileQuizModel):
        await FirebaseMessaging.send_topic_message(
            topic=cls.EVENTS_TOPIC,
            type=cls.Events.NEW_QUIZ,
            data={
                "uuid": str(quiz.uuid),
                "name": quiz.name,
            }
        )
    
    @classmethod
    async def login_session(cls, session: MobileSessionModel):
        await FirebaseMessaging.subscribe_to_topic(
            session.fcm_token,
            topic=cls.user_topic_key(session.user)
        )
        if session.user.status != MobileUserModel.Status.NEWBIE:
            await FirebaseMessaging.subscribe_to_topic(
                session.fcm_token,
                topic=cls.EVENTS_TOPIC
            )
    
    @classmethod
    async def logout_session(cls, session: MobileSessionModel):
        await FirebaseMessaging.unsubscribe_from_topic(
            session.fcm_token,
            topic=cls.user_topic_key(session.user)
        )
        await FirebaseMessaging.unsubscribe_from_topic(
            session.fcm_token,
            topic=cls.EVENTS_TOPIC
        )
        await session.adelete()
    
    @classmethod
    async def logout_user(cls, user: MobileUserModel):
        tokens = set()
        async for session in user.sessions.all():
            tokens.add(session.fcm_token)
            await session.adelete()
        
        await FirebaseMessaging.send_topic_message(
            topic=cls.user_topic_key(user),
            type=cls.Events.LOGOUT
        )
        if tokens:
            await FirebaseMessaging.unsubscribe_from_topic(
                *tokens,
                topic=cls.user_topic_key(user)
            )
            await FirebaseMessaging.unsubscribe_from_topic(
                *tokens,
                topic=cls.EVENTS_TOPIC
            )
    
    @staticmethod
    def user_topic_key(user: MobileUserModel):
        return f"user--{user.uuid}"
    