class MessagingClient:
    def __init__(self, messaging_service):
        self.messaging_service = messaging_service

    def update_status(self, user_name, status):
        self.messaging_service.update_status(user_name, status)