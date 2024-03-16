import re
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
        
def enviar_email_resposta_expediente(expediente_id, destinatario_email, resposta):
    # Assunto do e-mail
    subject = f"Resposta ao Expediente {expediente_id}"
    resposta_sem_tags = remover_tags_html(resposta)
    # Corpo do e-mail
    message = f"""Prezado(a),

Gostaríamos de informar que o expediente com ID {expediente_id} recebeu a seguinte resposta:

{resposta_sem_tags}

Atenciosamente,
UDMGest"""

    # Remetente do e-mail (configurado nas configurações do Django)
    sender_email = settings.EMAIL_HOST_USER

    try:
        # Enviar e-mail
        send_mail(subject, message, sender_email, [destinatario_email])
        print(f"E-mail de resposta do expediente enviado para {destinatario_email}")
    except Exception as e:
        # Lidar com erros de envio de e-mail
        print(f"Erro ao enviar e-mail de resposta do expediente para {destinatario_email}: {str(e)}")
        
def remover_tags_html(texto):
    # Expressão regular para encontrar tags HTML
    padrao = re.compile(r'<[^>]+>')
    # Substituir as tags HTML por uma string vazia
    texto_sem_tags = padrao.sub('', texto)
    return texto_sem_tags

def enviar_email_parecer_confirmado(expedient_id, destinatario_email):
    subject = 'Parecer Confirmado'
    message = f"""Prezado(a),

Espero que esta mensagem o(a) encontre bem.

Gostaríamos de informar que recebemos com sucesso o parecer do expediente com o ID {expedient_id} e ele foi confirmado em nossos registros.

Por favor, esteja à vontade para nos contatar se precisar de mais informações ou assistência adicional.

Agradecemos pela sua colaboração e confiança em nossa plataforma.

Atenciosamente,"""
    #destinatario_email.append('haider.arrone12@gmail.com')
    sender_email = settings.EMAIL_HOST_USER

    try:
        # Tentar enviar o e-mail
        send_mail(subject, message, sender_email, destinatario_email)
    except Exception as e:
        # Lidar com erros de envio de e-mail
        print(f"Erro ao enviar e-mail de confirmação de protocolo: {str(e)}")