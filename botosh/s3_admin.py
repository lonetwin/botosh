#!/usr/bin/python
import boto
from aws_admin import AWSAdmin

class S3Admin(AWSAdmin):

    def __init__(self):
        AWSAdmin.__init__(self)
        self.s3_conn = boto.connect_s3()

    def __repr__(self):
        return "s3"

    def do_ls(self, ignored):
        """ List all available buckets
        """
        for bucket in self.s3_conn.get_all_buckets():
            print bucket.name
