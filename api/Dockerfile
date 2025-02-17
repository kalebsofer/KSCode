FROM python:3.9-slim

WORKDIR /app

COPY ./api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./api/app /app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# running container
# docker build -t kscode .
# docker run -v ./models:/models -p 8000:8000 kscode
