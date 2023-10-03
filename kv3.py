from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from datetime import datetime, timedelta

def get_key_vault_url(region, vault_name):
    return f'https://{vault_name}.vault.azure.net'

def create_secret(vault_url, secret_name, secret_value, expiration_date=None):
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)

    secret_properties = {}
    if expiration_date:
        expires = datetime.utcnow() + timedelta(days=expiration_date)
        secret_properties['expires_on'] = expires

    client.set_secret(secret_name, secret_value, **secret_properties)
    print(f'Secret "{secret_name}" created successfully.')

def get_secret(vault_url, secret_name):
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)

    secret = client.get_secret(secret_name)
    print(f'Secret Value: {secret.value}')

def delete_secret(vault_url, secret_name):
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)

    client.begin_delete_secret(secret_name).result()
    print(f'Secret "{secret_name}" deleted successfully.')

def migrate_secret(source_vault_url, destination_vault_url, secret_name):
    credential = DefaultAzureCredential()
    source_client = SecretClient(vault_url=source_vault_url, credential=credential)
    destination_client = SecretClient(vault_url=destination_vault_url, credential=credential)

    secret = source_client.get_secret(secret_name)
    secret_value = secret.value
    secret_properties = secret.properties

    destination_client.set_secret(secret_name, secret_value, **secret_properties)
    print(f'Secret "{secret_name}" migrated successfully.')

# Replace these with your actual values
key_vault_region = 'East US'
source_vault_name = 'Nonso-kv-NP'
destination_vault_name = 'SIA-KV-US2'
secret_name = 'Password'
secret_value = 'IT'

source_vault_url = get_key_vault_url(key_vault_region, source_vault_name)
destination_vault_url = get_key_vault_url(key_vault_region, destination_vault_name)

# Uncomment the action you want to perform
# create_secret(source_vault_url, secret_name, secret_value, expiration_date=30)  # Set expiration in days
# get_secret(source_vault_url, secret_name)
# delete_secret(source_vault_url, secret_name)
migrate_secret(source_vault_url, destination_vault_url, secret_name)
