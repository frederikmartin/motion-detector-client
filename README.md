# Motion Detector Client

The motion detector client requests a [Philips Hue Motion Sensor](https://www2.meethue.com/en-us/p/hue-motion-sensor/046677473389) and sends motion notifications to an AWS Lambda for home automation purposes.

The client can e.g. be called within a cronjob using `crontab` to frequently check for motion:

```bash
# Motion Detector, runs every minute
* * * * * LAMBDA_API_KEY=<LAMBDA_API_KEY> python3 /<PATH_TO_PROJECT>/motion-detector-client/motion_detector_client.py <HUE_BRIDGE_IP> <HUE_USER_ID> <HUE_MOTION_SENSOR_ID> <AWS_LAMBDA_NOTIFICATION_WEBHOOK_URL>
```

If there is motion detected within the last minute, the AWS LAMBDA webhook is notified.

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

## Philips Hue API

The Philips Hue products offer a REST API for accessing and manipulating their behaviour (see [Philips Hue developer documentation](https://developers.meethue.com/)). Requesting the sensors endpoint returns something like the following:

```bash
{
    "state": {
        "presence": false,
        "lastupdated": "2019-08-03T11:58:54"
    },
    "swupdate": {
        "state": "noupdates",
        "lastinstall": "2019-08-01T22:19:12"
    },
    "config": {
        "on": true,
        "battery": 54,
        "reachable": true,
        "alert": "lselect",
        "sensitivity": 2,
        "sensitivitymax": 2,
        "ledindication": false,
        "usertest": false,
        "pending": []
    },
    "name": "<CONFIGURED_SENSOR_NAME>",
    "type": "ZLLPresence",
    "modelid": "SML001",
    "manufacturername": "Philips",
    "productname": "Hue motion sensor",
    "swversion": "6.1.1.27575",
    "uniqueid": "00:17:88:01:02:01:7f:a9-02-0406",
    "capabilities": {
        "certified": true,
        "primary": true
    }
}
```

Most important is the `state` property in the response JSON. It holds the information needed to recognize motion. Once motion is detected by the sensor, the `presence` flag turns to `true` and stays that way for at least 10 seconds. The `lastupdated` field is updated every time the `presence` flag toggles. This implementation checks whether the `presence` flag is active or the `lastupdated` flag got toggled within the last minute.

## AWS LAMBDA

The lambda function is requested using the POST method. Additionally an API key is send within the header of the request object to secure the access of the endpoint.

## Licence

See [LICENCE](./LICENCE) file.