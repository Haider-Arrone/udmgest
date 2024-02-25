from django.conf import settings
from django.core.mail import send_mail
def enviar_email(subject, message, recipient_list):
    send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            recipient_list,
            fail_silently=False,
        )
    
def enviar_email_novo_protocolo( procol,usuario_email):
    subject = 'Notificação de Novo Protocolo'
    message = f"""Prezado(a),

Gostaríamos de informar que um novo protocolo foi submetido em nosso sistema.

ID do Protocolo: {procol}

Por favor, tome as medidas necessárias conforme apropriado.

Atenciosamente,

UDMGest"""
    
    recipient_list = usuario_email  # Certifique-se de que usuario_email seja uma string de e-mail válida
    sender_email = settings.EMAIL_HOST_USER
    
    print(recipient_list)
    send_mail(subject, message, sender_email, recipient_list)
    
def enviar_email_protocolo_confirmado(protocolo_id, destinatario_email):
    subject = 'Protocolo Confirmado'
    message = f"""Prezado(a),

Gostaríamos de informar que o protocolo com ID {protocolo_id} foi confirmado.

Atenciosamente,

UDMGest"""
    #destinatario_email.append('haider.arrone12@gmail.com')
    sender_email = settings.EMAIL_HOST_USER

    try:
        # Tentar enviar o e-mail
        send_mail(subject, message, sender_email, destinatario_email)
    except Exception as e:
        # Lidar com erros de envio de e-mail
        print(f"Erro ao enviar e-mail de confirmação de protocolo: {str(e)}")