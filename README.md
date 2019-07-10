# Luigi examples with Kubernetes

This is Luigi and Kubernetes demo presented at Europython 2019 in Basel.

Luigi pipeline can be easily triggered from Kubernetes cronjob. 
By doing so, one can get all the benefits of model container orchestration system like flexible deployment, horizontal scaling and easier maintenance.   


## Run

Luigi example on local

`pipenv run python -m luigi --module example SalesReport --date=2019-07-11 --local-scheduler`

Luigi example on Kubernetes (minikube)

Minikube:

- Start minikube: `minikube start --memory 4096`
- Open K8S dashboard: `minikube dashboard`

Luigid:

- Deploy luigid: `mkctl apply -f luigid/deployment.yaml && mkctl apply -f luigid/service.yaml`
- Open Luigi UI: `minikube service luigid-service`

Luigi task:

- Deploy as cronjob: `mkctl apply -f cronjob.yaml`
- Run: `kubecron run luigi-example`


## Docker 

Docker images used in above deployments are available in Docker Hub https://hub.docker.com/u/chhantyal
