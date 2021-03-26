import re
import os
import numpy as np
from django.core.files import File
from django.conf import settings
from bokeh.plotting import figure, show
from bokeh.embed import components


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


def can_plot(asc_file):
    p = figure(title="Simple line example", x_axis_label='time', y_axis_label='data')
    # Regex expression is as follows
    #   (\d+.\d+)   Group 1 TIMESTAMP
    #   \s+
    #   (\d)        Group 2 CHANNEL
    #   \s+
    #   (\w+)       Group 3 ID HEX
    #   \s+Rx\s+d\s+
    #   (\d)        Group 4 DATA LENGTH
    #   \s
    #   (.+)        Group 5 DATA
    #   \s\sL.+=\s
    #   (\d+)       Group 6 ID DEC
    #
    # (\d+.\d+)\s+(\d)\s+(\w+)\s+Rx\s+d\s+(\d)\s(.+)\s\sL.+=\s(\d+)
    regex = '(\d+.\d+)\s+(\d)\s+(\w+)\s+Rx\s+d\s+(\d)\s(.+)\s\sL.+=\s(\d+)'

    data_dictionary = {}
    for encoded_line in asc_file:
        decoded_line = encoded_line.decode('UTF-8')
        message = re.search(regex, decoded_line)
        if message:
            can_id = int(message.group(3), 16)
            timestamp = float(message.group(1))
            data = [timestamp]
            for byte in message.group(5).split(' '):
                data.append(int(byte, 16))
            if can_id not in data_dictionary:
                data_dictionary[can_id] = [data]
            else:
                data_dictionary[can_id].append(data)




    ''' This creates only one single plot
        The challenge is to create however many plots we want to see
        Mayb edo what Joe did and show INTERESTING data?
        I dunno, let's find out...'''
    p = figure(title="my example", x_axis_label='time', y_axis_label='dunno')
    np_data = np.array(data_dictionary[145])
    time = np_data[:,0]
    trace1 = np_data[:,5]


    p.line(time, trace1, legend_label="trace1", line_width=2)
    script, div = components(p)

    my_keys = sorted(data_dictionary.keys())
    print(type(my_keys))
    print(my_keys)

    # for key in my_keys:
    #   print(key, data_dictionary[key])

    print(len(my_keys))
    ''' '''

    return script, div




