## Overview
The `rds-scheduler-lambda` AWS Lambda function is designed to automatically start and stop RDS instances based on a schedule defined in their tags. The schedule is set using a tag with the key "Schedule" and a value in the format 'Day1,Day2,Day3 hh:mm-hh:mm' or 'Day1,Day2,Day3 hh:mm', where 'Day1,Day2,Day3' are the days when the instance should be running (e.g., 'Monday,Tuesday,Wednesday'), with no spaces between the days and the commas, and 'hh:mm-hh:mm' is the start and end time (e.g., '09:00-17:00'). If only one time is provided (e.g., '17:00'), it is considered the end time, and the instance has to be started manually.

## Requirements

- Python 3.7
- Boto3 library
- Pytz library

## Setup
1. **IAM Role Creation**: Create an IAM role rds-scheduler-lambda-role with RDS access and Lambda execution policies.
2. **Schedule Tag**: Tag your RDS instances with the Schedule key and value in the format Day1,Day2,Day3 hh:mm-hh:mm.
3. **Deploy Lambda Function**: Upload the lambda_function.py as your Lambda function code.
4. **EventBridge Rule**: Set up an Amazon EventBridge (formerly CloudWatch Events) rule to trigger the Lambda function every 5 minutes using the expression rate(5 minutes).

## Function Execution
To ensure that the Lambda function starts and stops instances according to their schedules, set up a trigger for the Lambda function using Amazon EventBridge (formerly CloudWatch Events). Create a rule with a schedule expression to run the Lambda function periodically (e.g., every 5 minutes: rate(5 minutes)).

## Function Policy and Role
In order for this function to work, it requires an IAM role named "rds-scheduler-lambda-role" with the "RDS-Instance-Start-Stop-Policy" policy attached. The policy grants the role the following permissions:

- rds:DescribeDBInstances - Allows the function to retrieve information about RDS instances with the "Schedule" tag.
- rds:StartDBInstance - Allows the function to start RDS instances.
- rds:StopDBInstance - Allows the function to stop RDS instances.

The role must also have a trust policy that allows AWS Lambda to assume the role.

## Usage
Once set up, the Lambda function will check the tagged RDS instances and start or stop them based on the current day and time matching the Schedule tag.

## Contributing
Feel free to fork the repository and submit pull requests to contribute to the development of this function.

