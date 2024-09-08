# gke-cicd-pipeline
This repository contains code and resources for implementing a robust Continuous Integration/Continuous Deployment (CI/CD) pipeline for deploying applications on Google Kubernetes Engine (GKE). The pipeline leverages Google Cloud Build and Cloud Deploy services to automate the deployment processes.

*Dockerfile* that describes how to build and run the application.

*cloudbuild.yaml* file that describes the best practices for CI steps.

*skaffold.yaml* file that describes the deployment steps.

The cloudbuild.yaml and skaffold.yaml files in these repositories store the best practices for running CI and CD respectively on the platform. 

https://cloud.google.com/kubernetes-engine/docs/tutorials/modern-cicd-gke-reference-architecture#operator_repositories

Go to GitHub and pull up the repositories under your organization. There is a new repository with the name sample. This repository hosts the source code and steps to build containers in Dockerfile, kustomize configs that describe needed configurations of the application and skaffold.yaml that defines the deployment steps to be used by Cloud Deploy for CD.

https://cloud.google.com/kubernetes-engine/docs/tutorials/modern-cicd-gke-developer-workflow#application_repository 