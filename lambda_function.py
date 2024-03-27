import boto3
import datetime
import pytz
import os
 
def lambda_handler(event, context):
    timezone = 'America/New_York'
     
    rds = boto3.client('rds')
     
    instances = rds.describe_db_instances()
     
    tz = pytz.timezone(timezone)
    current_day = datetime.datetime.now(tz).strftime('%A').lower()
    current_time = datetime.datetime.now(tz).strftime('%H:%M')
     
    print(f"Current day: {current_day}, Current time: {current_time}")
 
    for instance in instances['DBInstances']:
        instance_id = instance['DBInstanceIdentifier']
        instance_state = instance['DBInstanceStatus']
         
        print(f"Processing instance: {instance_id}")
        print(f"Instance state: {instance_state}")
 
        schedule_tag = None
        for tag in instance['TagList']:
            if tag['Key'] == 'Schedule':
                schedule_tag = tag['Value']
                break
 
        if schedule_tag:
            print(f"Checking schedule for instance {instance_id}: {schedule_tag}")
 
            days, time_info = schedule_tag.split(' ')
            days = days.lower().split(',')
 
            if '-' in time_info:
                start_time, end_time = time_info.split('-')
            else:
                start_time = None
                end_time = time_info
 
            if current_day in days:
                if start_time and start_time <= current_time <= end_time:
                    if instance_state == 'stopped':
                        print(f"Starting instance {instance_id}")
                        rds.start_db_instance(DBInstanceIdentifier=instance_id)
                    else:
                        print(f"Instance {instance_id} is already running or starting. Skipping...")
                elif current_time >= end_time:
                    if instance_state == 'available':
                        print(f"Stopping instance {instance_id}")
                        rds.stop_db_instance(DBInstanceIdentifier=instance_id)
                    else:
                        print(f"Instance {instance_id} is already stopped or stopping. Skipping...")
                else:
                    print(f"Instance {instance_id} is not scheduled for action. Skipping...")
            else:
                print(f"Instance {instance_id} is not scheduled for action today. Skipping...")
        else:
            print(f"No schedule tag found for instance {instance_id}. Skipping...")
