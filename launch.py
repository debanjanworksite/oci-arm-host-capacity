import oci, os

config = {
    'user': os.environ['OCI_USER_ID'],
    'fingerprint': os.environ['OCI_KEY_FINGERPRINT'],
    'tenancy': os.environ['OCI_TENANCY_ID'],
    'region': os.environ['OCI_REGION'],
    'key_file': os.path.expanduser('~/.oci/private_key.pem')
}

client = oci.core.ComputeClient(config)

# Get latest Ubuntu 22.04 ARM image automatically
images = client.list_images(
    compartment_id=os.environ['OCI_TENANCY_ID'],
    operating_system='Canonical Ubuntu',
    operating_system_version='22.04',
    shape='VM.Standard.A1.Flex',
    sort_by='TIMECREATED',
    sort_order='DESC'
)

image_id = images.data[0].id
print(f"Using image: {images.data[0].display_name}")
print(f"Image ID: {image_id}")

details = oci.core.models.LaunchInstanceDetails(
    availability_domain='AP-HYDERABAD-1-AD-1',
    compartment_id=os.environ['OCI_TENANCY_ID'],
    shape='VM.Standard.A1.Flex',
    shape_config=oci.core.models.LaunchInstanceShapeConfigDetails(ocpus=4, memory_in_gbs=24),
    source_details=oci.core.models.InstanceSourceViaImageDetails(image_id=image_id),
    create_vnic_details=oci.core.models.CreateVnicDetails(
        subnet_id=os.environ['OCI_SUBNET_ID'],
        assign_public_ip=True
    ),
    metadata={'ssh_authorized_keys': os.environ['OCI_SSH_PUBLIC_KEY']},
    display_name='gyanaloy-server'
)

try:
    response = client.launch_instance(details)
    print('Success:', response.data.id)
except oci.exceptions.ServiceError as e:
    if 'Out of host capacity' in str(e):
        print('Out of capacity, will retry')
    else:
        print('Error:', e)
