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
    def region(self):
        return self.context.conn.region.name if getattr(self.context.conn, 'region', None) else 'global'

    @property
    def prompt(self):
        return prompt('%s > ' % (
            error('boto not configured') if not self._ready
                                         else self.context or error('context not set'))
                )

    def do_set_context(self, context):
        """ Set/Switch to a different context """
        from botosh import available_contexts
        available_contexts_str = green(', '.join(available_contexts.keys()))

        if not self._ready:
            print error("boto has not been configured with sufficient credentials. "
                        "Please configure boto first")
        if not context or not self._ready:
            print error('No context provided. Please `set_context` to one of: %s' % available_contexts_str)
        elif context in available_contexts:
            if context not in _context_cache:
                old_region = self.context.region if self.context else None
                new_context = available_contexts[context]()
                _context_cache[context] = new_context
                new_context.context = new_context
                if old_region and old_region in new_context._valid_regions:
                    new_context.conn = new_context.region_switcher(old_region)
            _context_cache[context].cmdloop()
        else:
            print error('Invalid context `%s`. Please `set_context` to one of: %s' % (context, available_contexts_str))


    def do_switch_region(self, region):
        """ Switch to a different region """
        from botosh import available_contexts

        if not self._ready:
            print error("boto has not been configured with sufficient credentials. "
                        "Please configure boto first")

        if not region:
            print error('No region provided.')

        if self.context is None:
            print error('No context provided. Please `set_context` to one of: %s' % green(', '.join(available_contexts.keys())))
        else:
            if self.context.region == region:
                return
            regions = self.context._valid_regions
            if region not in regions:
                print error('Invalid region `%s`. Please `switch_region` to one of: %s' %
                            (region, green(', '.join(regions))))
            else:
                self.context.conn = self.context.region_switcher(region)


    def do_quit(self, ignored):
        sys.exit(0)

    def do_list_contexts(self, ignored):
        """ List all available contexts """
        from botosh import available_contexts
        print "Available contexts:\n%s" % green('\n'.join(available_contexts.keys()))

    do_exit = do_quit
