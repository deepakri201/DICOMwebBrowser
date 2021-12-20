# DICOMwebBrowser.py 
# 
# This script implements the basic functionality of the SlicerDICOMwebBrowser 
# extension. Instead of using gcloud to perform the GCP commands, this 
# script uses the python commands. 
# 
# To store data, use the commands from 
# 
# Issues:
#     Cannot currently run as a script - but executes in Slicer command line.
# 
# Notes: 
#     list projects: 
#         https://stackoverflow.com/questions/58366396/google-cloud-platform-list-available-projects-using-api
#     list locations: 
#         https://cloud.google.com/tasks/docs/reference/rest/v2/projects.locations/list 
#     list datasets: 
#         https://cloud.google.com/healthcare-api/docs/samples/healthcare-list-datasets#healthcare_list_datasets-python 
#     list datastores: 
#         https://cloud.google.com/healthcare-api/docs/samples/healthcare-list-dicom-stores#healthcare_list_dicom_stores-python
#     dicomweb client
#         https://dicomweb-client.readthedocs.io/en/latest/usage.html 
#     
# 
# Deepa Krishnaswamy
# Brigham and Women's Hospital
# Dec 2021
##############################################################################

print ('started script')

import os 
import sys
import numpy as np
import matplotlib.pyplot as plt 
import re 
import json 
import SimpleITK as sitk 
import glob 

import slicer
from slicer.ScriptedLoadableModule import *

### Use pip to install the necessary packages ###
# slicer.util.pip_install("jupyter ipywidgets pandas ipyevents ipycanvas --no-warn-script-location")
slicer.util.pip_install('google')
slicer.util.pip_install('dicomweb-client')
slicer.util.pip_install('dicomweb-client[gcp]')
slicer.util.pip_install('oauth2client')
slicer.util.pip_install('google-api-core')
slicer.util.pip_install('google-api-python-client')
slicer.util.pip_install('google-cloud-core')
slicer.util.pip_install('google-cloud-storage')
print ('Used pip to install the necessary packages')

### Import the necessary packages ### 

import google 
# Imports the Google API Discovery Service.
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
# Import packages for the DICOM web client. 
from dicomweb_client.api import DICOMwebClient
from dicomweb_client.session_utils import create_session_from_gcp_credentials

### Set some variables related to the Healthcare API ### 
api_version = "v1"
service_name = "healthcare"

##############################################################################

########################################################################################
### To represent the selection menu in the SlicerDICOMwebBrowser - list the projects ### 
########################################################################################

print ('***** Getting the project id *****')

credentials = GoogleCredentials.get_application_default()
service = discovery.build('cloudresourcemanager', api_version, credentials=credentials)
request = service.projects().list()

project_list = []
 
if request is not None: 
    response = request.execute()
    if response is not None: 
        for project in response.get('projects', []):
            print('{:<20} {:<22} {:<21}'.format(project['projectId'], project['name'], project['projectNumber']))
            project_list.append(project['projectId'])
    else: 
        print ('Cannot get response')
else:
    print ('Cannot get request')

### Pick the first project for now and set the os.environ variable ### 
print ('project_list: ' + str(project_list))
project_id = project_list[0]
print ('project_id: ' + str(project_id))

##############################################################
### List the regions/locations, for now set to us-central1 ### 
### (How to get the default region?) ### 
##############################################################

print ('***** Getting the location *****')

service = discovery.build(service_name, api_version, credentials=credentials)
name = 'projects/' + project_id
request = service.projects().locations().list(name=name)

locations = [] 
locations_temp = [] 

if request is not None: 
    response = request.execute()
    if response is not None:
        locations_temp = response.get('locations', [])
        num_locations = len(locations_temp)
        for n in range(0,num_locations):
            locations.append(locations_temp[n]['locationId'])
    else:
        print ('Cannot get response')
else:
    print ('Cannot get request')

### Set the location ### 
print ('locations: ' + str(locations))
location = 'us-central1' # User has to set this. 
print ('location: ' + str(location))

########################################################################################
### To represent the selection menu in the SlicerDICOMwebBrowser - list the datasets ###
########################################################################################  

print ('***** Getting the dataset *****')

service = discovery.build(service_name, api_version, credentials=credentials)
dataset_parent = "projects/{}/locations/{}".format(project_id, location)
request = service.projects().locations().datasets().list(parent=dataset_parent)

datasets = [] 

if request is not None: 
    response = request.execute()
    if response is not None: 
        datasets = response.get("datasets", [])
    else:
        print ('Cannot get response')
else:
    print ('Cannot get request')

### Pick the first dataset for now ### 
print ('datasets: ' + str(datasets))
dataset_id = os.path.basename(datasets[0]['name']) 
print ('dataset_id: ' + str(dataset_id))

################################################################################################
### To represent the selection menu in the SlicerDICOMwebBrowser - list the dicom datastores ### 
################################################################################################

### Set the os.environ variable -- needed for this part? ### 
os.environ['GOOGLE_CLOUD_PROJECT'] = project_id 

service = discovery.build(service_name, api_version, credentials=credentials)
dicom_store_parent = "projects/{}/locations/{}/datasets/{}".format(project_id, location, dataset_id)
request = service.projects().locations().datasets().dicomStores().list(parent=dicom_store_parent)

dicom_stores = [] 

if request is not None: 
    response = request.execute()
    if response is not None: 
        dicom_stores = response.get("dicomStores", [])
    else:
        print ('Cannot get response')
else:
    print ('Cannot get request')

### Pick the first dicom datastore for now ### 
print ('dicom_stores: ' + str(dicom_stores))
dicom_store = os.path.basename(dicom_stores[0]['name'])
print ('dicom_store: ' + str(dicom_store))

#####################################################
### Create a dicom web client,list the studies    ###
### (don't need to pick and list series, we       ###
### know the extension should be able to do that  ###  
#####################################################

session = create_session_from_gcp_credentials()
print ('session: ' + str(session)) 

# client = DICOMwebClient(
#     url="https://healthcare.googleapis.com/v1/projects/idc-external-018/locations/us-central1/datasets/SlicerDICOMWeb_test/dicomStores/dicom-store-test/dicomWeb",
#     session=session
# )
url = r"https://" + service_name + ".googleapis.com/" + api_version + "/projects/" + project_id + "/locations/" + location + '/datasets/' + dataset + '/dicomStores/' + dicom_store + '/dicomWeb' 

client = DICOMwebClient(url=url, session=session)
print ('client: ' + str(client))

studies = client.search_for_studies(offset=0)
print ('studies: ' + str(studies))


