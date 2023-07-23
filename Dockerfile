FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -U Flask

COPY . .

CMD ["python", "app.py"]