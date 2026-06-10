from models.message import Message
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