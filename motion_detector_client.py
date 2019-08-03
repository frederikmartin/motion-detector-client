import motion_detector
import helpers

import sys
import argparse
from datetime import datetime, timedelta

def detect_motion(bridge, user, motion_sensor, logger):
    logger.info('Request motion sensor')
    hue_client = motion_detector.HueClient(base_url=bridge, user=user, motion_sensor=motion_sensor, logger=logger)
    motion_detected, last_updated = hue_client.query_sensor_data()
    logger.info('Motion detected: {}'.format(motion_detected))
    logger.info('Last updated: {}'.format(last_updated))
    return motion_detected, last_updated

def notify_user(notify_hook, logger):
    logger.info('Request notification hook')
    lambda_client = motion_detector.LambdaClient(base_url=notify_hook, logger=logger)
    response = lambda_client.notify_user()
    logger.info('Notification: {}'.format(response['status']))

def main(args):
    logger = helpers.Logger(True, args.log_path)

    motion_detected, last_updated = detect_motion(
        bridge=args.hue_bridge,
        user=args.hue_user,
        motion_sensor=args.hue_motion_sensor,
        logger=logger
    )
    curr_timestamp = datetime.utcnow()
    if motion_detected or (curr_timestamp - last_updated) < timedelta(minutes=1):
        logger.info('Motion alert triggered')
        notify_user(args.notify_hook, logger=logger)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('hue_bridge', help='IP address for Philips Hue bridge')
    parser.add_argument('hue_user', help='User id for Philips Hue bridge')
    parser.add_argument('hue_motion_sensor', help='Motion sensor id')
    parser.add_argument('notify_hook', help='URL for notification request')
    parser.add_argument('--log_path', help='Filepath for logging', default='/tmp/logs/motion_detector_client.log')
    args = parser.parse_args()
    main(args)
