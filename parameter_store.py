'''This script is used to connect to the AWS parameter store and get parameters,
it should be used as a module.
'''
import boto3

def para_store(para_name):
    '''Get parameters from AWS'''
    ssm = boto3.client('ssm', region_name='us-east-1')
    response = ssm.get_parameter(Name=para_name, WithDecryption=True)
    return response['Parameter']['Value']

if __name__ == '__main__':
    print('This should be used as a module.')
    