FROM python:3.10-slim
WORKDIR /app
COPY backend-server-py/requirements.txt .
RUN python3 -m venv /venv && \
    . /venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

COPY backend-server-py .
EXPOSE 8080
CMD ["/bin/bash", "-c", "source /venv/bin/activate && python3 server.py"]