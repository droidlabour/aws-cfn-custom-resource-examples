import os
import urllib

import boto3


def handler(event, context):
    print(event)

    testfile = urllib.URLopener()
    testfile.retrieve("https://gist.githubusercontent.com/droidlabour/84f81002bcbd188e824ab92c67d3c395/raw/ee28df4468f9806c5ecd284899ac71b9ec73ca0f/mysql", "/tmp/mysql")
    os.environ['PATH'] += os.pathsep + '/tmp'
    os.system("chmod 777 /tmp/mysql")

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    s3 = boto3.resource('s3')
    s3.meta.client.download_file(bucket, key, '/tmp/sql.sql')

    os.system('mysql -u' + os.getenv('RDSMasterUserName') + ' -p' + os.getenv('RDSMasterPassword') + ' -h' + os.getenv('RDSHostname') + ' ' + os.getenv('RDSDBName') + ' < /tmp/sql.sql')
