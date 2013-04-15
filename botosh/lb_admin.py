#!/usr/bin/python
import boto
from aws_admin import AWSAdmin
from utils import info, error, prompt, data
from utils import print_table

class LBAdmin(AWSAdmin):

    _lb = None

    def __init__(self):
        AWSAdmin.__init__(self)
        self.conn = boto.connect_elb()
        self.connected_to = ''
        self.region_switcher = boto.ec2.elb.connect_to_region


    def __repr__(self):
        return "lb | %s | %s" % (prompt(self.region),
                                 data(self.connected_to or 'Not connected')
                                 )

    @property
    def _valid_regions(self):
        return sorted(( region.name for region in boto.ec2.elb.regions() ))

    def need_connect(func):
        def is_connected(obj, *args):
            if not obj._lb:
                print error("Not connected to any load balancer. Please use the `connect` command")
            else:
                return func(obj, *args)
        is_connected.__doc__ = func.__doc__
        return is_connected


    def do_ls(self, lb_name):
        """ List all available load balancers
        """
        if not lb_name and not self._lb:
            for lb in self.conn.get_all_load_balancers():
                print info(lb.name)
        else:
            self.do_status(lb_name)

    def do_set_context(self, context=''):
        """ Set/Switch to a different context

        Besides the other available contexts (ie: those listed when you run
        `list_contexts`), you may provide an load balancer name . If you
        provide this you will be `connected` to the load balancer.
        """
        from botosh import available_contexts
        if context in available_contexts:
            super(LBAdmin, self).do_set_context(context)
        else:
            self.do_connect(context)

    def do_connect(self, lb_name):
        """ Connect to a load balancer.

        Execute `ls` to list all available load balancers.
        """
        if not lb_name:
            print error("Please provide a load-balancer name to connect to. "
                        "Execute `ls` to list all available load balancers")
        else:
            for lb in self.conn.get_all_load_balancers():
                if lb.name == lb_name:
                    self._lb = lb
                    self.connected_to = lb_name
                    break
            else:
                print error("Could not connect to `%s`" % info(lb_name))


    def do_disconnect(self, ignored):
        """ Disconnect from the currently connected-to load balancer.
        """
        if self.connected_to:
            self._lb = None
            self.connected_to = ''


    def do_status(self, lb_name):
        """ Shows the status of all the instances in the load balancer
        """
        # XXX get the ec2 context for the cache, if it exits. This is needed to
        # get the instance names.
        from botosh.aws_admin import _context_cache
        from botosh import available_contexts
        if 'ec2' not in _context_cache:
            ec2_context = available_contexts['ec2']()
        else:
            ec2_context = _context_cache['ec2']

        ec2_conn = ec2_context.conn
        lb_name = lb_name if lb_name else self.connected_to

        data = [("Instance Name", "Instance Id", "Status")]
        for instance_state in self.conn.describe_instance_health(lb_name):
            for reservation in ec2_conn.get_all_instances([instance_state.instance_id]):
                for instance in reservation.instances:
                    data.append((instance.tags.get('Name', ''), instance_state.instance_id, instance_state.state))
        print_table(data)


    @need_connect
    def do_add_instance(self, instance_id):
        """ Add an instance to the currently connected load balancer.

        Accepts an instance_id as an argument. You can get a list of available
        instance ids by switching context to `ec2` and executing `ls`
        """
        self._lb.register_instances( [instance_id] )


    @need_connect
    def do_remove_instance(self, instance_id):
        """ Remove an instance from the currently connected load balancer.

        Accepts an instance_id as an argument. You can get a list of available
        instance ids by switching context to `ec2` and executing `ls`
        """
        self._lb.deregister_instances( [instance_id] )
