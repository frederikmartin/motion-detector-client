import motion_detector
import helpers

import sys
import argparse
from datetime import datetime, timedelta

logger = helpers.Logger(True, '/tmp/logs/motion_detector_client.log')

def detect_motion(bridge, user, motion_sensor):
    logger.info('Request motion sensor')
    hue_client = motion_detector.HueClient(base_url=bridge, user=user, motion_sensor=motion_sensor, logger=logger)
    motion_detected, last_updated = hue_client.query_sensor_data()
    logger.info('Motion detected: {}'.format(motion_detected))
    logger.info('Last updated: {}'.format(last_updated))
    return motion_detected, last_updated

def notify_user(notify_hook):
    logger.info('Request notification hook')
    lambda_client = motion_detector.LambdaClient(base_url=notify_hook, logger=logger)
    response = lambda_client.notify_user()
    logger.info('Notification: {}'.format(response['status']))

def main(args):
    motion_detected, last_updated = detect_motion(
        bridge=args.hue_bridge,
        user=args.hue_user,
        motion_sensor=args.hue_motion_sensor
    )
    curr_timestamp = datetime.utcnow()
    if motion_detected or (curr_timestamp - last_updated) < timedelta(minutes=1):
        logger.info('Motion alert triggered')
        notify_user(args.notify_hook)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--hue_bridge', help='IP address for Philips Hue bridge', required=True)
    parser.add_argument('-u', '--hue_user', help='User id for Philips Hue bridge', required=True)
    parser.add_argument('-i', '--hue_motion_sensor', help='Motion sensor id', required=True)
    parser.add_argument('-n', '--notify_hook', help='URL for notification request', required=True)
    args = parser.parse_args()
    main(args)
