#!/usr/bin/python
import boto
from aws_admin import AWSAdmin
from utils import error, prompt, data
from utils import print_table

class EC2Admin(AWSAdmin):

    def __init__(self):
        AWSAdmin.__init__(self)
        self.conn = boto.connect_ec2()
        self.instance_id = None
        self.region_switcher = boto.ec2.connect_to_region

    def __repr__(self):
        return "ec2 | %s | %s" % (prompt(self.region),
                                  data(self.instance_id or 'all instances')
                                  )

    @property
    def _valid_regions(self):
        return sorted(( region.name for region in boto.ec2.regions() ))

    def _for_all_instances(self):
        for reservation in self.conn.get_all_instances():
            for instance in reservation.instances:
                yield instance


    def do_ls(self, ignored):
        """ List all available instances
        """
        data = [('Instance ID', 'Instance Name')]
        for instance in self._for_all_instances():
            data.append((instance.id, instance.tags.get('Name', '')))
        print_table(data)


    def do_set_context(self, context=''):
        """ Set/Switch to a different context

        Besides the other available contexts (ie: those listed when you run
        `list_contexts`), you may provide an instance id. If you provide an
        instance id any subsequent commands which expects an instance id
        would operate on this instance (unless an argument is explicitly
        provided).
        """
        from botosh import available_contexts
        if context in available_contexts:
            self.instance_id = None
            super(EC2Admin, self).do_set_context(context)
        else:
            for instance in self._for_all_instances():
                if context == instance.id:
                    self.instance_id = instance.id
                    break
            else:
                print error("Invalid instance id `%s`" % context)


    def check_context(func):
        def in_instance(obj, instance_id, *args):
            if (not instance_id) and obj.instance_id:
                return func(obj, obj.instance_id, *args)
            else:
                return func(obj, instance_id, *args)
        return in_instance


    @check_context
    def get_attr(self, instance_id, attr):
        instances = list(self._for_all_instances())
        instance_ids = [ instance.id for instance in instances ]
        if instance_id and (instance_id not in instance_ids):
            error("Invalid id: %s" % instance_id)
        elif instance_id:
            instance = instances[ instance_ids.index(instance_id) ]
            print getattr(instance, attr)
        else:
            data = [('Instance ID', attr)]
            for instance_id, instance in zip(instance_ids, instances):
                data.append((instance_id, getattr(instance, attr)))
            print_table(data)


    attr_doc = """ Print %(attr)s

        - Without arguments, in an instance context, prints the instance's
          %(attr)s.
        - Without arguments, when not in an instance context, prints the
          %(attr)s for all instances.
        - With an instance id argument, prints the %(attr)s for that
          instance.
        """

    do_internal_ip = lambda obj, instance_id: obj.get_attr(instance_id, 'private_ip_address')
    do_internal_ip.__doc__ = attr_doc % {'attr' : 'internal IP address'}

    do_external_ip = lambda obj, instance_id: obj.get_attr(instance_id, 'ip_address')
    do_external_ip.__doc__ = attr_doc % {'attr' : 'external IP address'}

    do_internal_hostname = lambda obj, instance_id: obj.get_attr(instance_id, 'private_dns_name')
    do_internal_hostname.__doc__ = attr_doc % {'attr' : 'internal hostname'}

    do_external_hostname = lambda obj, instance_id: obj.get_attr(instance_id, 'public_dns_name')
    do_external_hostname.__doc__ = attr_doc % {'attr' : 'external hostname'}

    do_status = lambda obj, instance_id: obj.get_attr(instance_id, 'state')
    do_status.__doc__ = attr_doc % {'attr' : 'status'}
