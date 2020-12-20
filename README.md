# PlayStation Stock Checker

Small project to routinely scan main UK PlayStation Merchants. Sends alert text if it finds one in stock. Based on Python, Selenium, Twilio & GitHub Actions.

Current retailers checked are:
- John Lewis
- Amazon UK
- Game
- Argos
- Currys

## Usage

The project is provided as public Docker image hosted on GitHub, you can pull this and use it yourself as follows:

```
docker pull ghcr.io/gowerc/pschecker:latest
docker run --rm \
    --env TWILIO_FROM_NUMBER="<You Twilio phone number" \
    --env TWILIO_TO_NUMBER="<Mobile number to receive notifications" \
    --env TWILIO_ACCOUNT_SID="<Your Tilio account SID>" \
    --env TWILIO_AUTH_TOKEN="<Your Twilio Auth Token>" \
    ghcr.io/gowerc/pschecker:latest
```

Note that you will need to set up a cron job or some other reoccurring process to continuously check for stock
