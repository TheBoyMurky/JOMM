def checar_instancia(ec2_client, id_instancia):
    ec2_status_response = ec2_client.describe_instance_status(
        InstanceIds=[id_instancia]
    )
    
    # print("Instância está", ec2_status_response['InstanceStatuses']['InstanceState']['Name'])

def ligar_instancia(ec2_client):
    ec2_response = ec2_client.start_instances(
        InstanceIds=[ec2_config_json['ec2_id']],
    )