# Motion Detector Client

The motion detector client requests a [Philips Hue Motion Sensor](https://www2.meethue.com/en-us/p/hue-motion-sensor/046677473389) and sends motion notifications to an AWS Lambda for home automation purposes.

The client can e.g. be called within a cronjob using `crontab` to frequently check for motion:

```bash
# Motion Detector, runs every minute
* * * * * LAMBDA_API_KEY=<LAMBDA_API_KEY> python3 /<PATH_TO_PROJECT>/motion-detector-client/motion_detector_client.py <HUE_BRIDGE_IP> <HUE_USER_ID> <HUE_MOTION_SENSOR_ID> <AWS_LAMBDA_NOTIFICATION_WEBHOOK_URL>
```

## Requirements

Python >= 3.5 is required.

## Usage

```bash
usage: motion_detector_client.py [-h] [--log_path LOG_PATH]
                                 hue_bridge hue_user hue_motion_sensor
                                 notify_hook

positional arguments:
  hue_bridge           IP address for Philips Hue bridge
  hue_user             User id for Philips Hue bridge
  hue_motion_sensor    Motion sensor id
  notify_hook          URL for notification request

optional arguments:
  -h, --help           show this help message and exit
  --log_path LOG_PATH  Filepath for logging
```

## AWS LAMBDA

The lambda function is requested using the POST method. Additionally an API key is send within the header of the request object to secure the access of the endpoint.

## Licence

See [LICENCE](./LICENCE) file.