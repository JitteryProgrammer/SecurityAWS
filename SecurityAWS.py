
# importando bibliotecas necessárias
import boto3
from botocore.exceptions import ClientError

# configurando as credenciais da AWS
ACCESS_KEY = 'your_access_key'
SECRET_KEY = 'your_secret_key'

# configurando o serviço da AWS
client = boto3.client(
    'ec2',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name='your_region'
)

# definindo a função que verificará a segurança do AWS
def check_security():
    # listando as regras de segurança
    try:
        security_groups = client.describe_security_groups()
    except ClientError as e:
        print(f'Erro ao listar as regras de segurança: {e}')
        return False

    # listando as instâncias
    try:
        instances = client.describe_instances()
    except ClientError as e:
        print(f'Erro ao listar as instâncias: {e}')
        return False

    # verificando se as instâncias estão usando as regras de segurança corretas
    for instance in instances['Reservations']:
        for i in instance['Instances']:
            for security_group in i['SecurityGroups']:
                security_group_name = security_group['GroupName']
                for rule in security_groups['SecurityGroups']:
                    if rule['GroupName'] == security_group_name:
                        # verificando as regras
                        if not rule['IpPermissions']:
                            print(f'A instância {i["InstanceId"]} não possui regras de segurança.')
                            return False
                        else:
                            print(f'A instância {i["InstanceId"]} está usando as regras de segurança corretas.')
                            return True

    return False


# chamando a função para verificar a segurança
check_security()
