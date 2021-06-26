from django.conf import settings
from storages.backends.azure_storage import AzureStorage

class PublicAzureStorage(AzureStorage):
  account_name = settings.AZURE_ACCOUNT_NAME
  azure_container = settings.AZURE_CONTAINER_NAME
  account_key = settings.AZURE_ACCESS_KEY