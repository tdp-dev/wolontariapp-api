from datetime import datetime, timedelta

from azure.storage.blob import (
    AccountSasPermissions,
    BlobServiceClient,
    ResourceTypes,
    generate_account_sas,
)

from backend.settings import Settings


def upload_blob(
    settings: Settings,
    container_name: str,
    blob_name: str,
    blob_data,
) -> None:
    blob_service_client = BlobServiceClient(
        account_url=f"https://{settings.AZURE_STORAGE['ACCOUNT_NAME']}.blob.core.windows.net",
        credential=settings.AZURE_STORAGE["KEY"],
    )
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob_name.encode("utf-8"))
    blob_client.upload_blob(blob_data, overwrite=True)


def generate_blob_url(settings: Settings, container_name: str, blob_name: str) -> str:
    storage_account_name = settings.AZURE_STORAGE["ACCOUNT_NAME"]
    sas_token = generate_account_sas(
        account_name=storage_account_name,
        account_key=settings.AZURE_STORAGE["KEY"],
        resource_types=ResourceTypes(object=True),
        permission=AccountSasPermissions(read=True),
        expiry=datetime.utcnow()
        + timedelta(seconds=settings.AZURE_STORAGE["SAS_LIFETIME"]),
    )
    return f"https://{storage_account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}"
