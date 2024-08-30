# Cross-persistence
This repository hosts the Python server that runs in each worker cluster that can create a PV and PVC for the purpose of cross-cluster checkpoint and restore with Karmada. This repo also includes the yaml files you can apply in order to deploy the server and the service, along with ClusterRoles (to give permission to create the PV, PVC) into the worker cluster. Note that the services exposed are NodePorts. When deploying the service, you must modify the name of the service to include the name of the member cluster - this is done by editing the file app.yaml. This is important because it allows the Karmada scheduler to recognize which cluster the service belongs to after fetching the service with karmada-search. 

## Building the Image
`docker build -t <dockerhub-username>/cross-persistence:latest .`

`docker push <dockerhub-username>/cross-persistence:latest`
