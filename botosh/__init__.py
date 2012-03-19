from aws_admin import AWSAdmin
from ec2_admin import EC2Admin
from s3_admin import S3Admin
from lb_admin import LBAdmin

available_contexts = {'ec2' : EC2Admin,
                      'lb'  : LBAdmin,
                      's3'  : S3Admin
                      }

