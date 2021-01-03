class UserContent:
    def __init__(self, user_id, content_id, completion_status=None, owned=None, user_rating=None):
        self.user_id = user_id
        self.content_id = content_id
        self.completion_status = completion_status
        self.owned = owned
        self.user_rating = user_rating


