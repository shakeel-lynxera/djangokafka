

class UserProxyEventHandler:

    def __init__(self):
        pass

    def login_user(self, event_data):
        """
        Update Authentication with of User Proxy
        """
        instance = event_data.get("event", None)
        if instance:
            if event_data.get("is_authenticated") and event_data.get("user_id"):
                print("User Login successfully.")
