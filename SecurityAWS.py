# importando bibliotecas necessárias
import boto3
from botocore.exceptions import ClientError
import csv
import datetime

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
    results = []
    for instance in instances['Reservations']:
        for i in instance['Instances']:
            for security_group in i['SecurityGroups']:
                security_group_name = security_group['GroupName']
                for rule in security_groups['SecurityGroups']:
                    if rule['GroupName'] == security_group_name:
                        # verificando as regras
                        if not rule['IpPermissions']:
                            result = {'instance_id': i["InstanceId"], 'security_group': security_group_name, 'status': 'Failed', 'reason': 'No security rules'}
                            results.append(result)
                            print(f'A instância {i["InstanceId"]} não possui regras de segurança.')
                        else:
                            #verificando se a porta 22 está fechada
                            flag = False
                            for perm in rule['IpPermissions']:
                                for port in perm['FromPort']:
                                    if port == 22:
                                        flag = True
                                        break
                                if flag:
                                    break
                            if flag:
                                result = {'instance_id': i["InstanceId"], 'security_group': security_group_name, 'status': 'Failed', 'reason': 'Port 22 is open'}
                                results.append(result)
                                print(f'A instância {i["InstanceId"]} não possui regras de segurança para porta 22.')
                            else:
                                result = {'instance_id': i["InstanceId"], 'security_group': security_group_name, 'status': 'Passed'}
                                results.append(result)
                                print(f'A instância {i["InstanceId"]} está usando as regras de segurança corretas.')
                            try:
                                addresses = client.describe_addresses()
                            except ClientError as e:
                                print(f'Erro ao listar os endereços Elastic IP: {e}')
                                return False
                            for address in addresses['addresses']:
                                if not address['InstaceId']:
                                    result = {'instance_id': 'N/A', 'security_group': 'N/A', 'status':'Failed', 'reason': 'Elastic IP is not associated with an instance'}
                                    results.append(result)
                                    print(f'O Elastic IP {address["PublicIp"]} não está vinculado a uma instância.')
                                    filename = "security_check_results_" + str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")) + ".csv"
                                with open(filename, 'w', newline='') as csvfile:
                                    fieldnames = ['instance_id', 'security_group', 'status', 'reason']
                                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                                    writer.writeheader()
                                    for result in results:
                                        writer.writerow(result)
                                    if any(result['status'] == 'Failed' for result in results):
                                        print('Uma notificação de erro foi enviada por email.')
                                    else:
                                        print('Tudo está seguro.')
                                    return

