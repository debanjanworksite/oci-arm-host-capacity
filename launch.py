import oci, os

config = {
    'user': os.environ['OCI_USER_ID'],
    'fingerprint': os.environ['OCI_KEY_FINGERPRINT'],
    'tenancy': os.environ['OCI_TENANCY_ID'],
    'region': os.environ['OCI_REGION'],
    'key_file': os.path.expanduser('~/.oci/private_key.pem')
}

client = oci.core.ComputeClient(config)

# List available ARM images
images = client.list_images(
    compartment_id=os.environ['OCI_TENANCY_ID'],
    operating_system='Canonical Ubuntu',
    shape='VM.Standard.A1.Flex'
)

for img in images.data:
    print(f"Name: {img.display_name}")
    print(f"OCID: {img.id}")
    print()
