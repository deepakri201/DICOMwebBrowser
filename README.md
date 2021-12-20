# DICOMwebBrowser

# DICOMwebBrowser

This script DICOMwebBrowser.py implements the basic functionality of the SlicerDICOMwebBrowser extension. Instead of using gcloud to perform the GCP commands, this script uses the python commands. 

It does not require the user to use their own environment, and instead relies on Slicer's own python environment. (Note -- currently the code in DICOMwebBrowser.py can be run on Slicer command line, but cannot be run as a script). 

The text file Healthcare_API_commands.txt contains a list of gcloud commands needed to create a dataset and a DICOM store, and how to add DICOM data to that store. Alternatively, a bucket can be created and data imported to the DICOM store using the import_dicom_instance.py script. 

The user must install the Google Cloud SDK, and create an environment from the requirements text files in order to run the commands in Healthcare_API_commands.txt.  
