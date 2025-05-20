# sber_kube

- [imgs](./imgs/)

`kubectl port-forward service/app-service 5000:80`

```sh
# "Для проверки метрик приложения:"
echo "curl http://localhost:5000/metrics"
# "Для доступа к Prometheus выполните:"
echo "kubectl port-forward -n journal-system svc/prometheus 5050:5050"
# "Затем откройте в браузере http://localhost:5050"
# "Проверьте метрики приложения в Prometheus, выполнив запрос:"
# "journal_log_requests_total"
# "Также доступны метрики Istio, например:"
# "istio_requests_total"
```