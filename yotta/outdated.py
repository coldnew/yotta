# Copyright 2015 ARM Limited
#
# Licensed under the Apache License, Version 2.0
# See LICENSE file for details.

# colorama, BSD 3-Clause license, cross-platform terminal colours, pip install colorama 
import colorama

# validate, , validate things, internal
from .lib import validate
# access, , get components, internal
from .lib import access

def addOptions(parser):
    pass

def execCommand(args, following_args):
    c = validate.currentDirectoryModule()
    if not c:
        return 1

    target, errors = c.satisfyTarget(args.target)
    if errors:
        for error in errors:
            logging.error(error)
        return 1

    dependencies = c.getDependenciesRecursive(
                      target = target,
        available_components = [(c.getName(), c)],
                        test = True
    )

    displayOutdated(dependencies, use_colours=(not args.plain))

def displayOutdated(modules, use_colours):
    if use_colours:
        DIM    = colorama.Style.DIM
        BRIGHT = colorama.Style.BRIGHT
        YELLOW = colorama.Fore.YELLOW
        RED    = colorama.Fore.RED
        GREEN  = colorama.Fore.GREEN
        RESET  = colorama.Style.RESET_ALL
    else:
        DIM = BRIGHT = YELLOW = RED = RESET = u''

    for name, m in modules.items():
        if m.isTestDependency():
            continue
        latest_v = access.latestSuitableVersion(name, '*', registry='modules', quiet=True)
        if not m:
            m_version = u' ' + RESET + BRIGHT + RED + u"missing" + RESET
        else:
            m_version = DIM + u'@%s' % (m.version)
        if not latest_v:
            print(u'%s%s%s not available from the registry%s' % (RED, name, m_version, RESET))
            continue
        elif not m or m.version < latest_v:
            if m:
                if m.version.major() < latest_v.major():
                    # major versions being outdated might be deliberate, so not
                    # that bad:
                    colour = GREEN
                elif m.version.minor() < latest_v.minor():
                    # minor outdated versions is moderately bad
                    colour = YELLOW
                else:
                    # patch-outdated versions is really bad, because there should
                    # be no reason not to update:
                    colour = RED
            else:
                colour = RED
            print(u'%s%s%s latest: %s%s%s' % (name, m_version, RESET, colour, latest_v.version, RESET))


