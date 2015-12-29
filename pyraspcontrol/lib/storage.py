#!/usr/bin/env python
# -*- coding: utf-8 -*-
import shlex
import subprocess
from subprocess import Popen

from pyraspcontrol.lib import constants

_DISK_USAGE_DANGER_THRESHOLD = 90
_DISK_USAGE_WARNING_THRESHOLD = 70


def get_disks():
    """Retrieves all physical and virtual disks on the Raspberry Pi.

    Disk information is retrieved via the `df` command. `df` provides the following
    information: Filesystem, Size, Used, Available, Usage %, Mounted on.

    Returns:
        list: A list of dictionaries where each dictionary contains a collection
            of related information for the ith disk found via `df`.

    """
    # df -h | sed 's/  */ /g' | tail -n +2
    ps = Popen(['df', '-h'], stdout=subprocess.PIPE)
    ps = Popen(['sed', 's/  */ /g'], stdin=ps.stdout, stdout=subprocess.PIPE)
    ps = Popen(['tail', '-n', '+2'], stdin=ps.stdout, stdout=subprocess.PIPE)
    disks = ps.communicate()[0].strip('\n').split('\n')

    data = []
    for disk_info in disks:
        info = shlex.split(disk_info)
        fs, size, used, available, usage, mount = info
        disk_data = {
            'file_system': fs,
            'size': size,
            'used': used,
            'available': available,
            'percentage': int(usage.replace('%', '')),
            'mount': mount,
            'alert': constants.SUCCESS,
        }
        if disk_data['percentage'] > _DISK_USAGE_DANGER_THRESHOLD:
            disk_data['alert'] = constants.DANGER
        if disk_data['percentage'] > _DISK_USAGE_WARNING_THRESHOLD:
            disk_data['alert'] = constants.WARNING
    return data
