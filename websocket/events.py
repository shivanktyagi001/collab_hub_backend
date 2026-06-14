from models.message import Message
from models.users import User
def message_created_event(message:Message):
    return {
        "event":"message_created",
        "data" :{
           "id":message.id,
           "channel_id":message.channel_id,
           "sender_id": message.sender_id,
           "content":message.content,
           "edited":message.edited,
            "is_deleted": message.is_deleted,
            "created_at": str(message.created_at),
            "updated_at": str(message.updated_at)
        }
    }

def typing_started_event(user:User):
    return {
        "event":"typing_started",
        "data":{
            "user_id":user.id,
            "username":user.username
        }
    }

def typing_stopped_event(user:User):
    return{
        "event":"typing_stopped",
        "data":{
            "user_id":user.id,
            "username":user.username
        }
    }


def user_online_event(user:User):
    return {
        "event":"user_online",
        "data":{
            "user_id":user.id,
            "username":user.username
        }
    }
def user_offline_event(user:User):
    return {
        "event":"user_offline",
        "data":{
            "user_id":user.id,
            "username":user.username
        }
    }