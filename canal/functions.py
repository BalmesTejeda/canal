import re
import os
from django.core.files import File
from django.conf import settings

def dbc_sorter(my_file):
    # first get rid of the encoding from the upload
    encoded_lines = my_file.readlines()
    lines = []
    for line in encoded_lines:
        my_line = line.decode('UTF-8').replace('\r', '')
        # my_line = line.decode('UTF-8').rstrip()
        lines.append(my_line)
    # everything is now in lines
    new_lines = lines
    sg_signal_start = []
    sg_signal_end = []

    message_started = False

    for i, line in enumerate(lines):
        if line.startswith('BO'):
            message_started = True
        if line.startswith(' SG') and message_started:
            sg_signal_start.append(i)
            message_started = False
        if line == '\n' and lines[i-1].startswith(' SG'):
            sg_signal_end.append(i-1)

    for index, _ in enumerate(sg_signal_start):
        myList = []

        for i in range(sg_signal_start[index], sg_signal_end[index] + 1):
            myLine = lines[i]
            start_bit = int(re.findall(': (\d+)', myLine)[0])
            myList.append([start_bit, myLine])

        myList.sort()

        for i, j in enumerate(range(sg_signal_start[index], sg_signal_end[index] + 1)):
            new_lines[j] = myList[i][1]

    filepath = os.path.join(settings.MEDIA_ROOT, 'sorted.dbc')
    new_file = open(filepath, 'w')
    new_file.writelines(new_lines)
    new_file.close()

    return filepath




