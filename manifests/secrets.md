```bash
kubectl create secret generic openai-secret --from-literal=api_key='your_openai_api_key' -n webhook-test
kubectl create secret generic opsgenie-secret --from-literal=api_key='your_opsgenie_api_key' -n webhook-test
kubectl create secret generic api-key-secret --from-literal=api-key='your-api-key' -n webhook-test
```