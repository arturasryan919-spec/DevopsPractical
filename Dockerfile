FROM python:3.12
WORKDIR /app
RUN apt-get update && apt-get install -y curl
COPY app/ .
RUN pip install -r requirements.txt 
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=5s CMD curl -f localhost:5000/health || exit 1
CMD ["python","app.py"]
