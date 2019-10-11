import boto3
import json
import datetime

import requests
from datetime import datetime
from bs4 import BeautifulSoup
from config import SQS_QUEUE_URL


def get_number_updates_last_month(updates):
    return len(list(filter(
        lambda x: datetime.strptime(x.contents[0], '%H:%M, %d %B %Y').month == datetime.now().month, updates)))


def endpoint(event, context):
    title = 'Washington,_D.C.'
    
    if event and event['queryStringParameters'] and 'title' in event['queryStringParameters']:
        title = event['queryStringParameters']['title']
        
    r = requests.get(f'https://en.wikipedia.org/w/index.php?title={title}&action=history')
    soup = BeautifulSoup(r.text, 'html.parser')
    updates = soup.findAll("a", {"class": "mw-changeslist-date"})

    output = {
        'latest_update_time': datetime.strptime(updates[0].contents[0], '%H:%M, %d %B %Y').isoformat(),
        'number_updates_last_month': get_number_updates_last_month(updates)
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(output)
    }
    send_to_sqs(data=response)
    return response


def send_to_sqs(data):
    """
    Send message to SQS
    """
    # Create SQS client
    sqs = boto3.client('sqs')
    
    # Send message to SQS queue
    sqs_response = sqs.send_message(
        QueueUrl=SQS_QUEUE_URL,
        DelaySeconds=1,
        MessageAttributes={
            'Title': {
                'DataType': 'String',
                'StringValue': 'wikiInfo'
            },
            'Author': {
                'DataType': 'String',
                'StringValue': 'serhii'
            },
            'WeeksOn': {
                'DataType': 'Number',
                'StringValue': '6'
            }
        },
        MessageBody=json.dumps(data)
    )
    
    print(sqs_response['MessageId'])

