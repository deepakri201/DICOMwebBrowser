# https://cloud.google.com/healthcare-api/docs/how-tos/dicom-import-export#api_1
def import_dicom_instance(
    project_id, location, dataset_id, dicom_store_id, content_uri
):
    """Imports data into the DICOM store by copying it from the specified
    source.

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/dicom
    before running the sample."""
    # Imports the Google API Discovery Service.
    from googleapiclient import discovery

    api_version = "v1"
    service_name = "healthcare"
    # Returns an authorized API client by discovering the Healthcare API
    # and using GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = discovery.build(service_name, api_version)

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'  # replace with your GCP project ID
    # location = 'us-central1'  # replace with the parent dataset's location
    # dataset_id = 'my-dataset'  # replace with the DICOM store's parent dataset ID
    # dicom_store_id = 'my-dicom-store'  # replace with the DICOM store's ID
    # content_uri = 'my-bucket/*.dcm'  # replace with a Cloud Storage bucket and DCM files
    dicom_store_parent = "projects/{}/locations/{}/datasets/{}".format(
        project_id, location, dataset_id
    )
    dicom_store_name = "{}/dicomStores/{}".format(dicom_store_parent, dicom_store_id)

    body = {"gcsSource": {"uri": "gs://{}".format(content_uri)}}

    # Escape "import()" method keyword because "import"
    # is a reserved keyword in Python
    request = (
        client.projects()
        .locations()
        .datasets()
        .dicomStores()
        .import_(name=dicom_store_name, body=body)
    )

    response = request.execute()
    print("Imported DICOM instance: {}".format(content_uri))

    return response




project_id = 'idc-external-018'
location = 'us-central1'
dataset_id = 'SlicerDICOMWeb_test' 
dicom_store_id = 'dicom-store-test' # created from create_dicom_store.py code. 
content_uri = 'slicer-dicomweb-bucket/*.dcm' 
response = import_dicom_instance(project_id, location, dataset_id, dicom_store_id, content_uri)

print ('response: ' + str(response))

# Returned: 
# Imported DICOM instance: slicer-dicomweb-bucket/*.dcm
# response: {'name': 'projects/idc-external-018/locations/us-central1/datasets/SlicerDICOMWeb_test/operations/13419329109100593153'}