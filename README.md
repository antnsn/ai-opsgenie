# Webhook Translator

The Webhook Translator is a Flask application designed to receive webhooks, enrich them with explanations using OpenAI's GPT models, and forward the enriched data to Opsgenie.

## Features

- Receive webhooks with arbitrary data.
- Utilize OpenAI to generate explanations of the received messages.
- Send enriched data to Opsgenie for alerting and monitoring.

## Getting Started

These instructions will get you a copy of the project up and running on your machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

- Docker
- Kubernetes (for deployment)
- Access to OpenAI API
- Access to Opsgenie API


### Using the Docker Image

You can run the pre-built Docker image hosted on Docker Hub:

1. Pull the Docker image from Docker Hub:
   ```bash
   docker pull antnsn/openai-opsgenie
   ```
2. Run the container:
   ```bash
   docker run -p 5000:5000 antnsn/openai-opsgenie
   ```


### Configuration and Deployment


### Configuration

Ensure your deployment environment is configured with the necessary API keys. Set these as environment variables when running the Docker container:

1. Set environment variables for OpenAI and Opsgenie API keys when running the Docker container:
   ```bash
   docker run -p 5000:5000 -e OPENAI_API_KEY='your_openai_api_key' -e OPSGENIE_API_KEY='your_opsgenie_api_key' antnsn/openai-opsgenie
   ```

### Deployment
To deploy this on a live Kubernetes system, use the Kubernetes manifest provided in the deployment.yaml file:

   ```bash
   kubectl apply -f deployment.yaml
   ```


### Additional Information

```markdown
### Built With

- [Flask](http://flask.pocoo.org/) - The web framework used
- [OpenAI API](https://openai.com/api/) - AI platform used for generating explanations
- [Opsgenie API](https://docs.opsgenie.com/) - Used for alert management

## Contributing

Please read [CONTRIBUTING.md](https://github.com/yourusername/webhook-translator/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

