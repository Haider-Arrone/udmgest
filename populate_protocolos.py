import os
import django
import random
from faker import Faker
from datetime import timedelta
from django.utils import timezone

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

# Importar os modelos
from expedient.models import Protocolo, Funcionario, Departamento

# Inicializar o Faker
fake = Faker()

# Função para criar registros de Protocolo
def create_protocolos(num):
    funcionarios = list(Funcionario.objects.all())
    departamentos = list(Departamento.objects.all())
    estados = ['Pendente', 'Concluído']
    
    for _ in range(num):
        descricao = fake.text(max_nb_chars=200)
        observacao = fake.text(max_nb_chars=200)
        data_emissao = timezone.now()
        remetente = random.choice(funcionarios) if funcionarios else None
        destinatario = random.choice(departamentos) if departamentos else None
        estado = random.choice(estados)
        prazo = data_emissao.date() + timedelta(days=random.randint(1, 30))
        data_confirmacao_recepcao = data_emissao + timedelta(days=random.randint(1, 30)) if random.choice([True, False]) else None
        confirmacao_user_status = random.choice([True, False])
        confirmacao_user = random.choice(funcionarios) if confirmacao_user_status and funcionarios else None

        protocolo = Protocolo(
            descricao=descricao,
            observacao=observacao,
            data_emissao=data_emissao,
            remetente=remetente,
            destinatario=destinatario,
            estado=estado,
            prazo=prazo,
            data_confirmacao_recepcao=data_confirmacao_recepcao,
            confirmacao_user_status=confirmacao_user_status,
            confirmacao_user=confirmacao_user
        )
        protocolo.save()

    print(f'{num} registros de Protocolo criados com sucesso.')

# Executar a função para criar registros
if __name__ == "__main__":
    create_protocolos(600)
