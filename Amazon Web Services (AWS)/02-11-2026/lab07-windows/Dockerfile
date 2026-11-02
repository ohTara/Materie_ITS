FROM python:3.12-slim
WORKDIR /app
COPY app.py .
RUN mkdir /data && chown 10001:10001 /data
ENV PYTHONUNBUFFERED=1
USER 10001:10001
EXPOSE 8000
CMD ["python", "app.py"]