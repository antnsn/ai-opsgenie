```bash
kubectl create secret generic openai-secret --from-literal=api_key='your_openai_api_key'
kubectl create secret generic opsgenie-secret --from-literal=api_key='your_opsgenie_api_key'
```