import json
import os
import subprocess
import datetime
import calendar


def vnstat_this_month_usage(interface_name):
    stdout = subprocess.getoutput(f"vnstat -s -i {interface_name} --json m")
    # with open('vnstat_output.json', 'r') as f:
    #     stdout = f.read()
    j = json.loads(stdout)
    interface = j['interfaces'][0]
    interface_name = interface['name']
    month = j['interfaces'][0]['traffic']['month'][-1]
    rx = month['rx']
    tx = month['tx']
    total = month['rx'] + month['tx']
    month_name = calendar.month_name[month['date']['month']]
    return interface_name, rx, tx, total, month_name


def human_bytes(B):
    """Return the given bytes as a human friendly KB, MB, GB, or TB string."""
    B = float(B)
    KB = float(1024)
    MB = float(KB ** 2)  # 1,048,576
    GB = float(KB ** 3)  # 1,073,741,824
    TB = float(KB ** 4)  # 1,099,511,627,776

    if B < KB:
        return '{0} {1}'.format(B,'Bytes' if 0 == B > 1 else 'Byte')
    elif KB <= B < MB:
        return '{0:.2f} KB'.format(B / KB)
    elif MB <= B < GB:
        return '{0:.2f} MB'.format(B / MB)
    elif GB <= B < TB:
        return '{0:.2f} GB'.format(B / GB)
    elif TB <= B:
        return '{0:.2f} TB'.format(B / TB)