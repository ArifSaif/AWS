#!/Library/Frameworks/Python.framework/Versions/3.11/bin/python3

from logging import getLogger
import boto3
from base import Base
from argparse import ArgumentParser

class sqs(Base):
    sqs=None
    AWS_REGION = 'us-east-1'

    def __init__(self):
        Base.__init__(self)
        self.log=getLogger(self.__class__.__name__)
        self.sqs = boto3.resource('sqs', region_name=self.AWS_REGION)


    def run(self, args):
        if (args.send):
            self.send(args.send[0], args.queue[0])
        else:
            func=getattr(self, args.operation[0])
            func(args.queue[0])
        
    def get(self, qName):
        self.log.debug("Method: Create, Queue Name: %s" % qName)
        retVal=None
        try:
            queue=self.sqs.get_queue_by_name(QueueName=qName)
            print("Queue URL: %s" % queue.url)
            print("Delay in Seconds: %s" %queue.attributes.get('DelaySeconds'))
            retVal=queue.url
        except:
            self.log.error("No queue exists in %s, with name: %s" % (self.AWS_REGION, qName))
            retVal=None
        return retVal

    def create(self, qName):
        self.log.debug("Method: Create, Queue Name: %s" % qName)
        queue = self.sqs.create_queue(QueueName=qName, Attributes={'DelaySeconds': '5'})
        return self.get(qName)

    def delete(self, qName):
        self.log.debug("Method: Delete, Queue Name: %s" % qName)
        sqs_client = boto3.client("sqs", region_name=self.AWS_REGION)
        qUrl=self.get(qName)
        if (qUrl):
            sqs_client.delete_queue(QueueUrl=qUrl)

    def send(self, message, qName):
        queue = self.sqs.get_queue_by_name(QueueName=qName)
        response = queue.send_message(MessageBody=message)

        # The response is NOT a resource, but gives you a message ID and MD5
        print("Message ID: %s" % response.get('MessageId'))

    def consume(self, qName):
        queue = self.sqs.get_queue_by_name(QueueName=qName)
        for message in queue.receive_messages(MessageAttributeNames=['Author']):
            print("Message Received on %s is %s" % (qName, message.body))
            message.delete

if __name__ == '__main__':
    import logutil
    logutil.init()

    parser = ArgumentParser(description=__doc__)
    parser.add_argument('-q', '--queue', nargs=1, action='store', required=True, help='Name of the queue')
    parser.add_argument('-o', '--operation', choices=['create', 'get', 'delete', 'consume'], nargs=1, help="Choose of the operation at queue level")
    parser.add_argument('-s', '--send', nargs=1, action='store', help='Send the following message to the specified queue')

    args = parser.parse_args()
    if (args.send or args.operation):
        runner=sqs()
        runner.run(args)
    else:
        parser.print_help()
        parser.exit()


    