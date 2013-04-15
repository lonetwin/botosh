botosh
======

A shell interface to Amazon Web Services based on the boto python interface

``botosh`` was created as a convenience tool for personal use. It is an
interactive commadline interface written using the ``cmd`` module from the
standard python library and uses the boto_
library to access AWS.


Installation and Invocation
---------------------------

    * Install boto_ (obviously)
    * Create a boto `configuration file`_
    * ``git clone git://github.com/lonetwin/botosh.git``
    * ``$ cd botosh && python main.py``


A sample session
----------------

::

    steve@lonelap ~/s/botosh (master) > python main.py

    Welcome to the AWS admin shell.

    - To execute any useful commands you must first

        * configure boto credentials (for example, under /etc/boto.cfg or /home/steve/.boto or by setting the
          AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables to
          sutiable values)

        * set a context using the `set_context` command.

    - The currently available contexts are ['s3', 'lb', 'ec2']

    - The available commands depend on the current context. Use the command `help`
      to list all available commands and `help <command>` to learn how to use a
      specific command.

    - Don't Panic !

    context not set > list_contexts
    Available contexts:
    s3
    lb
    ec2
    context not set > set_context ec2
    ec2 | all instances > ls
    Instance ID | Instance
    ------------+--------------------------------
    i-ca0cd5aa  | app instance0
    i-0f29ce6a  | app instance1
    i-e110028d  | database instance
    ec2 | all instances > internal_ip i-e110028d
    10.124.159.96
    ec2 | all instances > set_context i-e110028d
    ec2 | i-e110028d > internal_hostname
    ip-10-124-159-96.ec2.internal
    ec2 | i-e110028d > set_context lb
    lb | Not connected > ls
    app0-lb
    app1-lb
    lb | Not connected > connect app0-lb
    lb | app0-lb > status
    Instance Id | Status
    ------------+----------
    i-ca0cd5aa  | InService
    i-0f29ce6a  | InService
    lb | app0-lb > remove_instance i-ca0cd5aa
    lb | app0-lb > add_instance i-ca0cd5aa
    lb | app0-lb >
    Thanks for using the AWS admin shell !
    steve@lonelap ~/s/botosh (master) >


Currently botosh supports a *very* small subset of actions. However, these are
the actions I use most often. Feel free to contribute/suggest more commands.

Hope you find it useful.

TODO:
-----

    * Add more actions
    * Add tests ( explore moto_ )
    * Package it for pypi (?)
    * Explore whether this can be refactored to be generic enough for other
      cloud platforms


FEEDBACK:
---------
    Please report bugs at https://github.com/lonetwin/botosh/issues or mail me
    as botosh at lonetwin.net

.. _boto: https://github.com/boto/boto
.. _configuration file: http://boto.readthedocs.org/en/latest/boto_config_tut.html
.. _moto: https://github.com/spulec/moto/
