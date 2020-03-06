import json
import urllib.request

def lambda_handler(event, context):
    r = urllib.request.urlopen(
        'http://quickhire-data-dev.j535vysrhe.us-east-1.elasticbeanstalk.com/start-models'
    )
    res = json.loads(r.read())
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': '/start-models called',
            'result': 'success',
            'response': res
        })
    }
