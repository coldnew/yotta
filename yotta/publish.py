# Copyright 2014-2015 ARM Limited
#
# Licensed under the Apache License, Version 2.0
# See LICENSE file for details.

# standard library modules, , ,
import logging

# validate, , validate things, internal
from .lib import validate

def addOptions(parser):
    # no options
    pass

def execCommand(args, following_args):
    p = validate.currentDirectoryModuleOrTarget()
    if not p:
        return 1

    if not p.vcsIsClean():
        logging.error('The working directory is not clean. Commit before publishing!')
        return 1

    if p.description.get('bin', None) is not None:
        logging.warning(
            'This is an executable application, not a re-usable library module. Other modules will not be able to depend on it!'
        )
        # python 2 + 3 compatibility
        try:
            global input
            input = raw_input
        except NameError:
            pass
        raw_input("If you still want to publish it, press [enter] to continue.")

    error = p.publish(args.registry)
    if error:
        logging.error(error)
        return 1

    # tag the version published as 'latest'
    # !!! can't do this, as can't move tags in git?
    #p.commitVCS(tag='latest')
    logging.info('published latest version: %s', p.getVersion())
    return 0
