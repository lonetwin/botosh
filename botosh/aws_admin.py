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
    def _ready(self):
        return os.environ.get('AWS_ACCESS_KEY_ID', boto.config.get('Credentials', 'AWS_ACCESS_KEY_ID'))

    @property
    def prompt(self):
        return prompt('%s > ' % (
            error('boto not configured') if not self._ready
                                         else self.context or error('context not set'))
                )

    def do_set_context(self, context):
        """ Set/Switch to a different context """
        from botosh import available_contexts

        if not self._ready:
            print error("boto has not been configured with sufficient credentials. "
                        "Please configure boto first")
        if not context or not self._ready:
            print error('No context provided. Please `set_context` to one of: %s' % green(', '.join(available_contexts.keys())))
        elif context in available_contexts:
            if context not in _context_cache:
                new_context = available_contexts[context]()
                _context_cache[context] = new_context
                new_context.context = new_context
            _context_cache[context].cmdloop()
        else:
            print error('Invalid context')

    def do_quit(self, ignored):
        sys.exit(0)

    def do_list_contexts(self, ignored):
        """ List all available contexts """
        from botosh import available_contexts
        print "Available contexts:\n%s" % green('\n'.join(available_contexts.keys()))

    do_exit = do_quit
