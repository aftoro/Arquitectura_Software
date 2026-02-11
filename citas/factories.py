from .models import Cita

class CitaFactory:

    @staticmethod
    def crear_cita(tipo, data):
        if tipo == "normal":
            return Cita.objects.create(**data)
        
        elif tipo == "premium":
            data["estado"] = "VIP"
            return Cita.objects.create(**data)
        
        else:
            raise ValueError("Tipo de cita no valida")

class EmailService:
    def send(self, to, subject, body):
        print("Enviando email a", to)

class SMSService:
    def send(self, to, subject, body):
        print("Enviando SMS a", to)
    
class NotificationFactory:

    @staticmethod
    def get_notifier(tipo):
        if tipo == "email":
            return EmailService()
        elif tipo == "sms":
            return SMSService()
        else:
            raise ValueError("Tipo de notificacion no soportado")