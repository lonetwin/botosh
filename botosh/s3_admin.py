#!/usr/bin/python
import boto
from aws_admin import AWSAdmin

class S3Admin(AWSAdmin):

    def __init__(self):
        AWSAdmin.__init__(self)
        self.s3_conn = boto.connect_s3()
        self.bucket = None

    def __repr__(self):
        return "s3 | %s" % str(self.bucket)

    def do_ls(self, ignored):
        """ List all available buckets
        """
        for bucket in self.s3_conn.get_all_buckets():
            print bucket.name

    def do_set_context(self, context=''):
        """ Set/Switch to a different context

        Besides the other available contexts (ie: those listed when you run
        `list_contexts`), you may provide an bucket name. If you provide a
        bucket name any subsequent commands which expect a bucket name would
        operate on this bucket (unless an argument is explicitly provided).
        """
        from botosh import available_contexts
        if context in available_contexts:
            self.instance_id = None
            super(EC2Admin, self).do_set_context(context)
        else:
            for bucket in self.s3_conn.get_all_buckets():
                if context == bucket.name:
                    self.bucket = bucket.name

