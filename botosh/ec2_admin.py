#!/usr/bin/python
import boto
from aws_admin import AWSAdmin

class EC2Admin(AWSAdmin):

    def __init__(self):
        AWSAdmin.__init__(self)
        self.ec2_conn = boto.connect_ec2()

    def __repr__(self):
        return "ec2"

    def _for_all_instances(self):
        for reservation in self.ec2_conn.get_all_instances():
            for instance in reservation.instances:
                yield instance

    # def do_set_context(self, context=''):
    #     """ Set/Swith to a different context

    #     Besides the other available contexts (ie: those listed when you run
    #     `list_contexts`), you may provide an instance id. If you provide an
    #     instance id any subsequent commands which expect an instance id
    #     would operate on this instance (unless an argument is explicitly
    #     provided.
    #     """
    #     from botosh import available_contexts
    #     if context in available_contexts:
    #         super(EC2Admin, self).do_set_context(context)
    #     else:
    #         for instance in self._for_all_instances():
    #             instance_id = str(instance).split(':')[1]
    #             if context.startswith(instance_id):
    #                 self.instance_id = instance_id

    def do_internal_ip(self, instance_id):
        """ Print internal IP address

        Without arguments, prints the internal IP addresses for all instances.
        With an instance id argument, prints the internal IP address for that
        instance.
        """
        instances = list(self._for_all_instances())
        instance_ids = [ str(instance).split(':')[1] for instance in instances ]
        if instance_id and (instance_id not in instance_ids):
            print "Invalid id: %s" % instance_id
        elif instance_id:
            instance = instances[ instance_ids.index(instance_id) ]
            print instance.private_ip_address
        else:
            print "Instance ID | IP Address"
            print "======================="
            for instance_id, instance in zip(instance_ids, instances):
                print "%11s | %s" % (instance_id, instance.private_ip_address)


    def do_external_ip(self, instance_id):
        """ Print external IP address

        Without arguments, prints the external IP addresses for all instances.
        With an instance id argument, prints the external IP address for that
        instance.
        """
        instances = list(self._for_all_instances())
        instance_ids = [ str(instance).split(':')[1] for instance in instances ]
        if instance_id and (instance_id not in instance_ids):
            print "Invalid id: %s" % instance_id
        elif instance_id:
            instance = instances[ instance_ids.index(instance_id) ]
            print instance.ip_address
        else:
            print "Instance ID | IP Address"
            print "======================="
            for instance_id, instance in zip(instance_ids, instances):
                print "%11s | %s" % (instance_id, instance.ip_address)

    def do_ls(self, ignored):
        """ List all available instances
        """
        print "Instance ID | Instance"
        print "====================="
        for instance in self._for_all_instances():
            instance_id = str(instance).split(':')[1]
            name = instance.tags['Name']
            print "%11s | %s" % (instance_id, name)
