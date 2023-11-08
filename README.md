Make sure the variable `OPENAI_API_KEY` is in the environment.

To run the interface:

```bash
python chat-cli.py [--model <openai-model-name>] [--temperature <float>]
```

Default arguments:

| Arg             | Value         | Comments                           |
| --------------- | ------------- | ---------------------------------- |
| `--model`       | gpt-3.5-turbo | View all options in `pricing.json` |
| `--temperature` | 1.0           | Between 0 and 2                    |

### Docker

(not 100% supported yet, need to do more testing)

Set the environment variable `COMPOSE_PROJECT_NAME` if you want to use custom container names.

```bash
docker compose up -d
docker exec -it <container-name> python chat-cli.py [args]
```
