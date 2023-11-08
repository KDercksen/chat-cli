FROM python:3.11-slim-bookworm
WORKDIR /app/
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "chat-cli.py"]