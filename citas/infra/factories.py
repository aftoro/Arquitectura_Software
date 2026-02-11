import os


class EmailService:
    def send(self, to, subject, body):
        print("Enviando email a", to)


class SMSService:
    def send(self, to, subject, body):
        print("Enviando SMS a", to)


class MockNotificationService:
    def send(self, to, subject, body):
        print("Notificacion mock para", to)


class NotificationFactory:
    @staticmethod
    def get_notifier():
        notifier_type = os.getenv("NOTIFIER_TYPE", "mock").lower()
        if notifier_type == "email":
            return EmailService()
        if notifier_type == "sms":
            return SMSService()
        if notifier_type == "mock":
            return MockNotificationService()
        raise ValueError("Tipo de notificacion no soportado")
