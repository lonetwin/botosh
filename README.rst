botosh
======

A shell interface to Amazon Web Services based on the boto python interface

``botosh`` was created as a convenience tool for personal use. It is an
interactive commadline interface written using the ``cmd`` module from the
standard python library and uses the boto_
library to access AWS.


Installation
------------
.. TODO
    * Install boto_ (obviously)


A sample session
----------------

::

    [steve@laptop src]$ python botosh/main.py

    Welcome to the AWS admin shell.

    - To execute any useful commands you must first
        * configure boto credentials using the `setup` command, if you haven't
          already got a boto config file (for example, under /etc/boto.cfg or /home/steve/.boto)
        * set a context using the `set_context` command.

    - The currently available contexts are ['lb', 'ec2']

    - The available commands depend on the current context. Use the command `help`
      to list all available commands and `help <command>` to learn how to use a
      specific command.

    - Don't Panic !

     > help

    Documented commands (type help <topic>):
    ========================================
    set_context

    Undocumented commands:
    ======================
    exit  help  list_contexts  quit  setup

     > list_contexts
    Available contexts:
    lb
    ec2
     > set_context ec2
    ec2 > ls
    Instance ID | Instance
    =====================
     i-01234567 | dbserver
     i-f00dcafe | webserver
    ec2 > set_context lb
    lb | Not connected > ls
    loadbalance-webserver
    loadbalance-other
    lb | Not connected > connect loadbalance-webserver
    lb | loadbalance-webserver > status
    Instance Id | Status
    ====================
     i-42424242 | InService
    lb | loadbalance-webserver > add_instance i-01234567
    lb | loadbalance-webserver > quit
    Thanks for using the AWS admin shell !


Currently botosh supports a *very* small subset of actions. However, these are
the actions I use most often. Feel free to contribute/suggest more commands.

Hope you find it useful.

.. _boto: https://github.com/boto/boto
