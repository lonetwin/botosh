#!/usr/bin/python
import sys
import boto

from botosh import AWSAdmin
from botosh import available_contexts
from botosh.utils import info, error

if __name__ == '__main__':
    aws_sh = AWSAdmin()
    debug = 'debug' in sys.argv
    pdb = 'pdb' in sys.argv
    try:
        aws_sh.cmdloop(
            info("""
Welcome to the AWS admin shell.

- To execute any useful commands you must first

    * configure boto credentials (for example, under %s or by setting the
      AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables to
      sutiable values)

    * set a context using the `set_context` command.

- The currently available contexts are %s

- The available commands depend on the current context. Use the command `help`
  to list all available commands and `help <command>` to learn how to use a
  specific command.

- Don't Panic !
""" % (' or '.join(boto.BotoConfigLocations), available_contexts.keys())
                )
            )

    except (SystemExit, KeyboardInterrupt):
        print info("\nThanks for using the AWS admin shell !")
        sys.exit(0)
    except:
        if debug:
            import traceback
            traceback.print_exc()
        elif pdb:
            import pdb
            pdb.post_mortem(sys.exc_info()[-1])
        else:
            print error("""
Oops ! You found a bug. If possible, could you please re-run the shell with the
`debug` parameter, recreate the bug and copy/paste the traceback into a bug
report here:
    https://github.com/lonetwin/botosh/issues
""")
