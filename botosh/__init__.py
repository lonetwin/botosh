from aws_admin import AWSAdmin
from ec2_admin import EC2Admin
from lb_admin import LBAdmin

available_contexts = {'ec2' : EC2Admin,
                      'lb'  : LBAdmin
                      }

