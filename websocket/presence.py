from collections import defaultdict

class PresenceManager:

    def __init__(self):
        self.online_user = defaultdict(int)
    
    def connect(self,user_id:int) -> bool:
        self.online_user[user_id] += 1

        if self.online_user[user_id] == 1:
            return True
        return False
    def disconnect(self,user_id:int)-> bool:
        if user_id not in self.online_user:
            return False
        
        self.online_user[user_id] -=1

        if self.online_user[user_id]<=0:
            del self.online_user[user_id]
            return True
        return False
    def is_online(self,user_id:int) -> bool:
        return user_id in self.online_user
    def get_online_users(self):
        return list(self.online_user.keys())

        
presence_manager = PresenceManager()