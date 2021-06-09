# RangRang - Server

<p align="center">
  <img src="assets/logo.png" alt="logo" width="300px" height="300px" />
</p>

[![python](https://img.shields.io/badge/Made%20with-Python-1f425f?style=plastic&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-3.2-green?style=plastic&logo=django)](https://docs.djangoproject.com/en/3.2/)
[![djangorestframework](https://img.shields.io/badge/djangorestframework-3.12-blue?style=plastic)](https://www.django-rest-framework.org/)
[![TensorFlow 2.3](https://img.shields.io/badge/TensorFlow-2.5-FF6F00?logo=tensorflow)](https://github.com/tensorflow/tensorflow/releases/tag/v2.5.0)

Server side of RangRang that use `Django` & `djangorestframework`

Steps to Replicate the Server Deployment:
1. Open the Google Cloud Platform
2. Go into the Cloud Console
3. To Provision a New Compute Instance for the Back-End Server, Run the Following Commands
```
    gcloud beta compute --project=still-bank-315212 instances create rangrang-backend --zone=asia-southeast2-b --machine-type=n1-standard-2 --subnet=default --address=34.101.140.95 --network-tier=PREMIUM --maintenance-policy=TERMINATE --service-account=1083353886178-compute@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/cloud-platform --tags=http-server,https-server --image=ubuntu-2004-focal-v20210603 --image-project=ubuntu-os-cloud --boot-disk-size=10GB --boot-disk-type=pd-ssd --boot-disk-device-name=rangrang-backend --no-shielded-secure-boot --shielded-vtpm --shielded-integrity-monitoring --reservation-affinity=any

    gcloud compute --project=still-bank-315212 firewall-rules create default-allow-http --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:80 --source-ranges=0.0.0.0/0 --target-tags=http-server

    gcloud compute --project=still-bank-315212 firewall-rules create default-allow-https --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:443 --source-ranges=0.0.0.0/0 --target-tags=https-server
  ```
 4. SSH into the Server either by GUI, or through the Command Line Interface
 5. Update Packages on the Ubuntu VM by Running the Following Commands
 ```BASH
    sudo apt update
    sudo apt upgrade
 ```
 6. Setup Machine Learning Dependencies with the Following Commands
 ```BASH
    clone models repository from tensorflow
    git clone https://github.com/tensorflow/models.git
 ```
    
[![web](https://img.shields.io/badge/website-online-green?style=plastic)](http://35.222.141.247/)
