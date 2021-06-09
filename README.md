# RangRang - Server

<p align="center">
  <img src="assets/logo.png" alt="logo" width="300px" height="300px" />
</p>

[![python](https://img.shields.io/badge/Made%20with-Python-1f425f?style=plastic&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-3.2-green?style=plastic&logo=django)](https://docs.djangoproject.com/en/3.2/)
[![djangorestframework](https://img.shields.io/badge/djangorestframework-3.12-blue?style=plastic)](https://www.django-rest-framework.org/)
[![TensorFlow 2.5](https://img.shields.io/badge/TensorFlow-2.5-FF6F00?logo=tensorflow)](https://github.com/tensorflow/tensorflow/releases/tag/v2.5.0) [![Protobuf Compiler >= 3.0](https://img.shields.io/badge/ProtoBuf%20Compiler-%3E3.0-brightgreen)](https://grpc.io/docs/protoc-installation/#install-using-a-package-manager)

[![web](https://img.shields.io/badge/website%20status-online-green?style=plastic)](http://35.222.141.247/)

## Steps to Replicate the Server Deployment

1. Open the Google Cloud Platform
2. Go into the Cloud Console
3. To Provision a New Compute Instance for the Back-End Server, Run the Following Commands
   ```
   gcloud beta compute --project=<YOUR PROJECT ID> instances create rangrang-backend --zone=asia-southeast2-b --machine-type=n1-standard-2 --subnet=default --address=34.101.140.95 --network-tier=PREMIUM --maintenance-policy=TERMINATE --service-account=1083353886178-compute@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/cloud-platform --tags=http-server,https-server --image=ubuntu-2004-focal-v20210603 --image-project=ubuntu-os-cloud --boot-disk-size=10GB --boot-disk-type=pd-ssd --boot-disk-device-name=rangrang-backend --no-shielded-secure-boot --shielded-vtpm --shielded-integrity-monitoring --reservation-affinity=any

   gcloud compute --project=<YOUR PROJECT ID> firewall-rules create default-allow-http --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:80 --source-ranges=0.0.0.0/0 --target-tags=http-server

   gcloud compute --project=<YOUR PROJECT ID> firewall-rules create default-allow-https --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:443 --source-ranges=0.0.0.0/0 --target-tags=https-server
   ```
 4. SSH into the Server either by GUI, or through the Command Line Interface
 5. Update Packages on the Ubuntu VM by Running the Following Commands
      ```bash
      sudo apt update && sudo apt upgrade -y
      ```
 6. Setup Machine Learning Dependencies with the Following Commands
      * Clone models repository from tensorflow
         ```bash
         git clone https://github.com/tensorflow/models.git
         ```
      * Install tensorflow object detection API
         ```bash
         cd models/research
         protoc object_detection/protos/*.proto --python_out=.
         cp object_detection/packages/tf2/setup.py .
         sudo pip3 install --use-feature=2020-resolver .
         ```
7. Clone *This* Repository by Running the Following Command
      ```bash
      git clone https://github.com/Hyuto/rangrang-server.git
      cd rangrang-server
      ```
8. Install `Django`, `djangorestframework` and `whitenoise`
      ```bash
      sudo pip3 install django djangorestframework whitenoise
      ```
9. Setup `django` application
      * Setup main directory
         ```bash
         mkdir static files
         ```
      * Migrate db
         ```bash
         python3 manage.py migrate
         ```
      * Collectstatic
         ```bash
         python3 manage.py collectstatic
         ```
10. Exit the SSH Session by Running:
      ```bash
      exit
      ```
11. Turn off the VM Instance for the Back End Server by
   * Clicking on the Checkbox of the VM that is Going to be Turned Off
   * On the Top Panel, Click Stop
12. Click on the Back End Server VM then Click on the Edit Button.
13. Navigate to the Custom metadata Section, and add the Following:<br>
   Key: `startup-script`<br>
   Value: 
      ```bash
      #! /bin/bash
      sudo service apache2 stop
      cd /home/rangrang-server
      sudo nohup python3 manage.py runserver 0.0.0.0:80 >> log.log 2>&1 | tee &
      ```
14. Save the Changes
15. Turn on the VM Instance to Start the Back End Server Service
16. Navigate to the External IP Address to Check Its Availability by Going to these Paths:
      ```
      http://<EXTERNAL-IP-ADDRESS>/cd-api/video/
      http://<EXTERNAL-IP-ADDRESS>/cd-api/picture/
      http://<EXTERNAL-IP-ADDRESS>/od-api/video/
      http://<EXTERNAL-IP-ADDRESS>/od-api/picture/
     ```
     
Once all the Paths are Working, the Server is Considered Fully Functioning and Ready to Use

## Navigation 

|  | Repository |
| :--- | :--------: |
| Android | [grrrracia/RangRang-MobileApp](https://github.com/grrrracia/RangRang-MobileApp) |
| Cloud Computing | [Hyuto/rangrang-server](https://github.com/Hyuto/rangrang-server) |
| Machine Learning | [Hyuto/rangrang-ML](https://github.com/Hyuto/rangrang-ML) |