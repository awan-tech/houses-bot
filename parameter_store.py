import boto3

def para_store(para_name):
    ssm = boto3.client('ssm', region_name='us-east-1')
    response = ssm.get_parameter(Name=para_name, WithDecryption=True)
    return response['Parameter']['Value']

if __name__ == '__main__': ## Test
    print('main')