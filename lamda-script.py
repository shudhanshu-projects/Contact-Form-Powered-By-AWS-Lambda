import boto3
from base64 import b64decode
from urllib.parse import parse_qs

# Replace your email address here
send_to = 'your_email_address_here'

def lambda_handler(event, context):
    # We receive our data through POST requests. API gateway
    # sends the POST data as a Base64 encoded string in
    # event['body'], so we must decode it.
    data = parse_qs(b64decode(event['body']).decode())

    subject = 'You got a message from %s' % data['email'][0]
    text = '\n'.join([
        'Name: %s' % data['name'][0],
        'Email: %s' % data['email'][0],
        'Message %s' % data['message'][0]
    ])

    # Send an email through SES with the SendEmail API
    client = boto3.client('ses', region_name='us-east-1')
    client.send_email(
        Source=send_to,
        Destination={'ToAddresses': [send_to]},
        Message={
            'Subject': {'Data': subject},
            'Body': {'Text': {'Data': text}}
        },
        ReplyToAddresses=[data['email'][0]]
    )

    # This is the response that'll be sent out through the
    # API gateway to the browser.
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': '"Success"' # jquery expects a JSON response
    }
