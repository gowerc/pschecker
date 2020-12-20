# PlayStation Stock Checker

Small project to routinely to see if a Playstation 5 is available within the UK and send a text alert if it finds one in stock. 

Current retailers checked are:
- John Lewis
- Amazon UK
- Game
- Argos
- Currys

## Usage

The project is provided as public Docker image hosted on GitHub, you can pull this and use it yourself (making sure to edit the Twilio environment variables for your account) by running the following:

```
docker run --rm \
    --env TWILIO_FROM_NUMBER="<Your Twilio phone number"> \
    --env TWILIO_TO_NUMBER="<Mobile number to receive notifications"> \
    --env TWILIO_ACCOUNT_SID="<Your Tilio account SID>" \
    --env TWILIO_AUTH_TOKEN="<Your Twilio Auth Token>" \
    ghcr.io/gowerc/pschecker:latest
```

Note that running the code as shown above only performs a single stock check. If you wish to continuously check for stock you will need to set up a cron job or some other reoccurring process.


## About 

Core code uses Selenium controlled by Python, sends text alerts using Twilio, runs a cron job via GitHub Actions and stores the docker image in the GitHub Container Registry.
