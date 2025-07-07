import boto3
import json
import time
from datetime import datetime, timedelta
from botocore.config import Config

# Abrindo arquivo JSON
with open('config.json', 'r') as file:
    ec2_config_json = json.load(file)

# Checks com o valor do tempo
if type(ec2_config_json['time_min']) != int:
    print("O tipo da variável tem que ser inteiro, não deve ser entre aspas!")
    exit()
if ec2_config_json['time_min'] <= 0:
    print("Tempo não pode ser menor ou igual a 0.")
    exit()
if ec2_config_json['time_min'] > 180:
    print("Não será liberado tempo acima de 3 horas")
    exit()

# Definindo tempo do EC2 ligado
tempo_formato_legivel = "%d/%m/%Y - %H:%M:%S"
tempo_formato_calculavel = "%d%m%Y%H%M%S"
#tempo_atual = datetime.now()
tempo_limite = datetime.now() + timedelta(minutes=ec2_config_json['time_min'])

# Configurando EC2 Boto3 Client
ec2_config = Config(
    region_name = ec2_config_json['region']
)
ec2_client = boto3.client(
    'ec2',
    aws_access_key_id=ec2_config_json['access_key'],
    aws_secret_access_key=ec2_config_json['secret_key'],
    config=ec2_config
)

# Funções para a instância EC2
def checar_instancia(ec2_client, id_instancia):
    ec2_response = ec2_client.describe_instance_status(
        InstanceIds=[id_instancia],
        IncludeAllInstances=True
    )
    return ec2_response['InstanceStatuses'][0]['InstanceState']['Name']

def pegar_dns_pub_instancia(ec2_client, id_instancia):
    ec2_response = ec2_client.describe_instances(
        InstanceIds=[
            id_instancia,
        ],
    )
    return ec2_response['Reservations'][0]['Instances'][0]['NetworkInterfaces'][0]['Association']['PublicDnsName']

def ligar_instancia(ec2_client, id_instancia):
    ec2_response = ec2_client.start_instances(
        InstanceIds=[id_instancia],
    )
    if ec2_response['StartingInstances'][0]['PreviousState']['Name'] == "running":
        print("Instância", ec2_response['StartingInstances'][0]['InstanceId'], "já está iniciado.")
    else:
        print("Instância", ec2_response['StartingInstances'][0]['InstanceId'], "está iniciando.")

def desligar_instancia(ec2_client, id_instancia):
    ec2_response = ec2_client.stop_instances(
        InstanceIds=[id_instancia],
    )
    if ec2_response['StoppingInstances'][0]['PreviousState']['Name'] == "stopped":
        print("Instância", ec2_response['StoppingInstances'][0]['InstanceId'], "já está parado.")
    else:
        print("Instância", ec2_response['StoppingInstances'][0]['InstanceId'], "está parando.")

# Função principal
def main():
    print("JOMM - Just One More Minute")
    print("Tempo até instância desligar:", tempo_limite.strftime(tempo_formato_legivel))
    ligar_instancia(ec2_client, ec2_config_json['ec2_id'])
    while checar_instancia(ec2_client, ec2_config_json['ec2_id']) != "running":
        time.sleep(30)
    print("Se conecte à instância com o IP à seguir:", pegar_dns_pub_instancia(ec2_client, ec2_config_json['ec2_id']))
    while tempo_limite >= datetime.now():
        pass
    desligar_instancia(ec2_client, ec2_config_json['ec2_id'])

if __name__ == "__main__":
    main()