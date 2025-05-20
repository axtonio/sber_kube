#!/bin/bash

export DOCKER_HOST=unix:///var/run/docker.sock

istioctl install --set profile=demo -y
docker build -t custom-app:latest .
minikube image load custom-app:latest
kubectl label namespace journal istio-injection=enabled --overwrite
kubectl apply -f kubernetes/prometheus.yaml
kubectl apply -f kubernetes/configmap.yml
kubectl apply -f kubernetes/pod.yml
kubectl wait --for=condition=Ready pod/app-pod --timeout=60s
kubectl exec app-pod -- curl -s http://localhost:5000/status
kubectl apply -f kubernetes/deployment.yml
kubectl wait --for=condition=Available deployment/app-deployment --timeout=60s
kubectl apply -f kubernetes/service.yml
kubectl apply -f kubernetes/pv.yml
kubectl apply -f kubernetes/pvc.yml
kubectl apply -f kubernetes/daemonset.yml
kubectl apply -f kubernetes/cronjob.yml
kubectl apply -f kubernetes/istio-gw.yaml
kubectl apply -f kubernetes/istio-vs.yaml
kubectl apply -f kubernetes/istio-dest.yaml
kubectl wait --namespace=journal --for=condition=Available deployment/prometheus --timeout=60s