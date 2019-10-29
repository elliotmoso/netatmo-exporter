# Netatmo Exporter to InfluxDB
Needs environment variables:  

| ENV |  DEFAULT VALUE |  Description |
|----------|:-------------:|:------|
| INFLUXDB_HOST |  influxdb | InfluxDB host to send metrics |
| INFLUXDB_PORT | 8086 |   InfluxDB port |
| INFLUXDB_DB | office | InfluxDB Database, you can append a retention policy like office.retention |
| NETATMO_USERNAME | - | Netatmo username (email) |
| NETATMO_PASSWORD | - | Netatmo password |
| NETATMO_CLIENT_ID| - | Netatmo OAuth2 Client ID |
| NETATMO_CLIENT_SECRET | -| Netatmo OAuth2 Client Secret |

## Geting OAuth2 Client ID and Secret
You must create a netatmo developer account at: https://dev.netatmo.com
In there, you will have to create an application with `CREATE YOUR APP` Link.
Once you have created the app, Client ID and Client Secret will appear in your app configuration.

#### PR are welcome, I know that this code sucks... but it works

### Thanks
Based on: https://github.com/teamvirtue/dataPolling/blob/7988d5a357ef1696cef5e874d7c514f594c955b9/Modules/Netatmo.py
