import boto3
import json

def assume_role(role_arn):
    sts_client = boto3.client('sts')
    assumed_role = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName="LambdaDeploymentSession"
    )
    creds = assumed_role['Credentials']
    return creds

def update_lambda(creds, lambda_function_name, zip_file_path, region):
    lambda_client = boto3.client(
        'lambda',
        aws_access_key_id=creds['AccessKeyId'],
        aws_secret_access_key=creds['SecretAccessKey'],
        aws_session_token=creds['SessionToken'],
        region_name=region
    )

    with open(zip_file_path, 'rb') as f:
        zipped_code = f.read()

    response = lambda_client.update_function_code(
        FunctionName=lambda_function_name,
        ZipFile=zipped_code,
        Publish=True
    )
    print("Lambda update response:", json.dumps(response, indent=4))

if __name__ == "__main__":
    ROLE_ARN = "arn:aws:iam::396608812584:role/AUTOMATION"
    FUNCTION_NAME = "cross-deploy-fun"
    ZIP_FILE = "lambda.zip"
    REGION = "us-east-1"

    creds = assume_role(ROLE_ARN)
    update_lambda(creds, FUNCTION_NAME, ZIP_FILE, REGION)

