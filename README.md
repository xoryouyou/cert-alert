# cert-alert

Checks the expiry of TLS certificates and returns an error code when a given threshold is reached.

The program was born out of necessity to regularly check for internally deployed TLS certificates and their CAs.

I know calenders exists but a broken pipeline / alert is more noticeable 😅

## Usage

Create a `config.yml` 

```yaml
certificates:
    - my_certificate:
        name: "my homelab CA certificate"
        file: "./files/my_homelab_ca.pem"
        threshold: 10
```

Run `cert-alert`

```
2025-03-07 13:08:50 win-box cert_alert.config_loader[4581] INFO Reading config from config.yml.example
2025-03-07 13:08:50 win-box cert_alert.config_loader[4581] INFO ✅ Config read successfully
2025-03-07 13:08:50 win-box cert_alert.cert_alert[4581] INFO Started
2025-03-07 13:08:50 win-box cert_alert.cert_alert[4581] WARNING ⚠ Certificate my homelab CA certificate has reaches the expiry threshold
```

The results are written to `report.json` by default.

It is possible to check for HTTPS certificates using `ssl` and `urllib` like this 

```yaml
certificates:
  - remote_test:
    name: "github public endpoint"
    url: "github.com"
    threshold: 100
```


## Docker

via docker run
```bash
docker pull xoryouyou/cert-alert 
docker run -v $(pwd)/your_certificates:/certificates xoryouyou/cert-alert --your_config.yml
```

via docker compose

```yml
name: cert-alert
services:
    cert-alert:
        volumes:
            - ./your_certificates:/certificates
            - ./your_config.yml:/config.yml
            - ./reports:/reports
        image: xoryouyou/cert-alert

```
then run `docker compose run cert-alert --config config.yml --output /reports/report.json`
