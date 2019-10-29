FROM python:alpine
ENV NETATMO_CLIENT_ID="" NETATMO_CLIENT_SECRET="" NETATMO_USERNAME="" NETATMO_PASSWORD="" INFLUXDB_HOST="influxdb" \
INFLUXDB_PORT="8086" INFLUXDB_DB="office"
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD python main.py