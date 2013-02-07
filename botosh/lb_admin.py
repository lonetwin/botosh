#!/usr/bin/python
import boto
from aws_admin import AWSAdmin
from utils import info, error, context
from utils import print_table

class LBAdmin(AWSAdmin):

    _lb = None

    def __init__(self):
        AWSAdmin.__init__(self)
        self.elb_conn = boto.connect_elb()
        self.connected_to = 'Not connected'


    def __repr__(self):
        return "lb | %s" % context(self.connected_to)


    def need_connect(func):
        def is_connected(obj, *args):
            if not obj._lb:
                print error("Not connected to any load balancer. Please use the `connect` command")
            else:
                return func(obj, *args)
        is_connected.__doc__ = func.__doc__
        return is_connected


    def do_ls(self, ignored):
        """ List all available load balancers
        """
        for lb in self.elb_conn.get_all_load_balancers():
            print info(lb.name)


    def do_connect(self, lb_name):
        """ Connect to a load balancer.

        Execute `ls` to list all available load balancers.
        """
        if not lb_name:
            print error("Please provide a load-balancer name to connect to. "
                        "Execute `ls` to list all available load balancers")
        else:
            for lb in self.elb_conn.get_all_load_balancers():
                if lb.name == lb_name:
                    self._lb = lb
                    self.connected_to = lb_name
                    break
            else:
                print error("Could not connect to `%s`" % info(lb_name))


    @need_connect
    def do_status(self, lb_name):
        """ Shows the status of all the instances in the load balancer
        """
        data = [("Instance Id", "Status")]
        for instance_state in self.elb_conn.describe_instance_health(self.connected_to):
            data.append((instance_state.instance_id, instance_state.state))
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
