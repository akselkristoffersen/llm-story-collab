FROM python:3.10-slim
WORKDIR /app
COPY backend-server-py/requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
COPY backend-server-py .
EXPOSE 8080
CMD ["python3", "server.py"]