#!/usr/bin/python
import os
import sys
import cmd
import boto

from utils import info, error, prompt
from utils import green

_context_cache = {}

class AWSAdmin(object, cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.context = None

    @property
    def prompt(self):
        return prompt('%s > ' % (self.context or error('context not set')))

    def do_set_context(self, context=''):
        """ Set/Switch to a different context """
        from botosh import available_contexts

        if not os.environ.get('AWS_ACCESS_KEY_ID', boto.config.get('Credentials', 'AWS_ACCESS_KEY_ID')):
            print error("boto has not been configured with sufficient credentials. Please use the `setup` command")
        if not context:
            print error('No context provided. Please `set_context` to one of: %s' % green(', '.join(available_contexts.keys())))
        elif context in available_contexts:
            if context not in _context_cache:
                new_context = available_contexts[context]()
                _context_cache[context] = new_context
                new_context.context = new_context
            _context_cache[context].cmdloop()
        else:
            print error('Invalid context')

    def precmd(self, command):
        if self.context or command.startswith('list_contexts'):
            return command
        elif not command.startswith('set_context') and \
           not command.startswith('setup'):
            return 'set_context'
        return command

    def do_setup(self, ignored):
        """ Configure credentials for AWS access """
        for key in ('AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY'):
            os.environ[key] = raw_input("%s : " % key)
        _context_cache.clear()

    def do_quit(self, ignored):
        sys.exit(0)

    def do_list_contexts(self, ignored):
        """ List all available contexts """
        from botosh import available_contexts
        print "Available contexts:\n%s" % green('\n'.join(available_contexts.keys()))

    do_exit = do_quit
