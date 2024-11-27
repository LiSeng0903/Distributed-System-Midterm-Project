import boto3
import socket
import msgpackrpc
import requests

### contants ###
CHORD_PORT = 5057
ASG_REGION = 'us-east-1'
ASG_NAME = 'midterm-project-chord'
### end constants ###

def new_client(ip, port):
	return msgpackrpc.Client(msgpackrpc.Address(ip, port))

def get_instance_ips(asg_name):
    autoscaling_client = boto3.client('autoscaling', region_name=ASG_REGION)
    ec2_client = boto3.client('ec2', region_name=ASG_REGION)

    response = autoscaling_client.describe_auto_scaling_groups(
        AutoScalingGroupNames=[asg_name]
    )
    instance_ids = [
        instance['InstanceId']
        for instance in response['AutoScalingGroups'][0]['Instances']
    ]

    instances_info = ec2_client.describe_instances(InstanceIds=instance_ids)
    instance_ips = []
    for reservation in instances_info['Reservations']:
        for instance in reservation['Instances']:
            instance_ips.append({
                'InstanceId': instance['InstanceId'],
                'PublicIP': instance.get('PublicIpAddress'),
                'PrivateIP': instance.get('PrivateIpAddress'),
            })

    return instance_ips

my_public_IPAddr = requests.get('https://api.ipify.org?format=json').json()['ip']
instances = get_instance_ips(ASG_NAME)
# count not none instance
instance_num = 0
for i in range(len(instances)):
    if instances[i]['PublicIP'] != None:
        instance_num += 1

if instance_num == 1:
    print('I am the first instance')
    my_chord_client = new_client(my_public_IPAddr, CHORD_PORT)
    my_chord_client.call('create')
else:
    print('I am not the first instance')
    for i in range(len(instances)):
        if instances[i]['PublicIP'] != my_public_IPAddr:
            my_chord_client = new_client(my_public_IPAddr, CHORD_PORT)
            print('create my chord client')
            chord_client_2 = new_client(instances[i]['PublicIP'], CHORD_PORT)
            print('create chord client 2')
            my_chord_client.call('join', chord_client_2.call('get_info'))
            print('join chord client 2')
            break