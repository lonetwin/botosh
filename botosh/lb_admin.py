#!/usr/bin/python
import boto
from aws_admin import AWSAdmin

class LBAdmin(AWSAdmin):

    _lb = None

    def __init__(self):
        AWSAdmin.__init__(self)
        self.elb_conn = boto.connect_elb()
        self.connected_to = 'Not connected'


    def __repr__(self):
        return "lb | %s" % self.connected_to


    def need_connect(func):
        def is_connected(obj, args):
            if not obj._lb:
                print "Not connected to any load balancer. Please use the `connect` command"
            else:
                return func(obj, args)
        return is_connected


    def do_ls(self, ignored):
        """ List all available load balancers
        """
        for lb in self.elb_conn.get_all_load_balancers():
            print str(lb).split(':')[1]


    def do_connect(self, lb_name):
        """ Connect to a load balancer.

        Execute `ls` to list all available load balancers.
        """
        if not lb_name:
            print "Please provide a load-balancer name to connect to. Execute `ls` to list all available load balancers"
        else:
            lb = self.elb_conn.get_all_load_balancers( load_balancer_names=[ lb_name ] )
            if lb:
                self._lb = lb[0]
                self.connected_to = lb_name
            else:
                print "Could not connect to `%s`" % lb_name


    @need_connect
    def do_status(self, lb_name):
        """ Shows the status of all the instances in the load balancer
        """
        print "Instance Id | Status"
        print "===================="
        for instance_state in self.elb_conn.describe_instance_health(self.connected_to):
            print "%11s | %s" % (instance_state.instance_id, instance_state.state)


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

