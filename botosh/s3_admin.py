#!/usr/bin/python
import boto
from aws_admin import AWSAdmin
from utils import info, error, prompt, data

class S3Admin(AWSAdmin):

    def __init__(self):
        AWSAdmin.__init__(self)
        self.conn = boto.connect_s3()
        self.bucket = None

    def __repr__(self):
        return "s3 | %s | %s" % (prompt(self.region),
                                 data(self.bucket or 'all instances')
                                 )

    def do_switch_region(self, ignored):
        print error("switching regions is not supported for s3")

    def do_ls(self, bucket_or_pattern=''):
        """
        Without arguments:
            - within the 'all buckets' context, list all available buckets
            - within a bucket's context, list contents of bucket
        With arguments:
            - list all items matching the argument.
              The argument can be either bucket-name or a pattern of the form:
                [<bucket-name>/]prefix
        """
        if not bucket_or_pattern and not self.bucket:
            for bucket in self.conn.get_all_buckets():
                print bucket.name
        else:
            bucket_name = prefix = ''
            if self.bucket:
                bucket_name = self.bucket

            if bucket_or_pattern:
                if '/' in bucket_or_pattern:
                    bucket_name, prefix = bucket_or_pattern.split('/')
                elif bucket_name == '':
                    bucket_name = bucket_or_pattern
                else:
                    prefix = bucket_or_pattern

                for bucket in self.conn.get_all_buckets():
                    if bucket_name == bucket.name:
                        break
                else:
                    print error("No such bucket: %s" % info(bucket))

            bucket = self.conn.get_bucket(bucket_name)
            for item in bucket.list(prefix=prefix):
                print item.key


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
            super(S3Admin, self).do_set_context(context)
        else:
            for bucket in self.conn.get_all_buckets():
                if context == bucket.name:
                    self.bucket = bucket.name

