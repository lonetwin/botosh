#!/usr/bin/python
import os
import sys
import cmd
import boto

_context_cache = {}

class AWSAdmin(object, cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.context = ''

    @property
    def prompt(self):
        return '%s > ' % self.context

    def do_set_context(self, context=''):
        """ Set/Switch to a different context """
        from botosh import available_contexts

        if not os.environ.get('AWS_ACCESS_KEY_ID', boto.config.get('Credentials', 'AWS_ACCESS_KEY_ID')):
            print "boto has not been configured with sufficient credentials. Please using the `setup` command"
        if not context:
            print 'No context provided. Please set context to one of %s' % available_contexts.keys()
        elif context in available_contexts:
            if context not in _context_cache:
                new_context = available_contexts[context]()
                _context_cache[context] = new_context
                new_context.context = new_context
            _context_cache[context].cmdloop()
        else:
            print 'Invalid context'

    def precmd(self, command):
        if not self.context and \
           not command.startswith('set_context') and \
           not command.startswith('setup'):
            return 'set_context'
        return command

    def do_setup(self, ignored):
        for key in ('AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY'):
            os.environ[key] = raw_input("%s : " % key)

    def do_quit(self, ignored):
        sys.exit(0)

    def do_list_contexts(self, ignored):
        from botosh import available_contexts
        print "Available contexts:\n%s" % '\n'.join(available_contexts)

    do_exit = do_quit
