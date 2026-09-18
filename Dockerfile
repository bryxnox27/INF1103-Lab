FROM python:3.13.14

WORKDIR /app

COPY auditor.py .

CMD ["python", "auditor.py"]