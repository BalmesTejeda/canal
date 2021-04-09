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


''' for any functions that use regex to extract data from a .asc file
    Regex expression is as follows:
    (\d+.\d+)   Group 1 TIMESTAMP
    \s+
    (\d)        Group 2 CHANNEL
    \s+
    (\w+)       Group 3 ID HEX
    \s+Rx\s+d\s+
    (\d)        Group 4 DATA LENGTH
    \s
    (.+)        Group 5 DATA
    \s\sL.+=\s
    (\d+)       Group 6 ID DEC
    (\d+.\d+)\s+(\d)\s+(\w+)\s+Rx\s+d\s+(\d)\s(.+)\s\sL.+=\s(\d+)
'''


def get_asc_info(asc_file):
    regex = '(\d+.\d+)\s+(\d)\s+(\w+)\s+Rx\s+d\s+(\d)\s(.+)\s\sL.+=\s(\d+)'
    ch1_messages_dict = {}
    ch2_messages_dict = {}
    for encoded_line in asc_file:
        decoded_line = encoded_line.decode('UTF-8')
        message = re.search(regex, decoded_line)
        if message:
            channel = int(message.group(2))
            can_id_dec = int(message.group(3), 16)
            can_id_hex = message.group(3)
            byte_length = int(message.group(4))
            timestamp = float(message.group(1))
            if channel == 1:
                if can_id_hex not in ch1_messages_dict:
                    ch1_messages_dict[can_id_hex] = byte_length
            if channel == 2:
                if can_id_hex not in ch2_messages_dict:
                    ch2_messages_dict[can_id_hex] = byte_length
    return sorted(ch1_messages_dict.items()), sorted(ch2_messages_dict.items())


def get_plots(asc_file, hex_id):
    regex = '(\d+.\d+)\s+(\d)\s+' + hex_id.upper() + '\s+Rx\s+d\s+(\d)\s(.+)\s\sL.+=\s(\d+)'
    data = []
    for encoded_line in asc_file:
        decoded_line = encoded_line.decode('UTF-8')
        message = re.search(regex, decoded_line)
        if message:
            timestamp = float(message.group(1))
            message_bytes = int(message.group(3))
            message_data = [timestamp, message_bytes]
            for byte in message.group(4).split(' '):
                message_data.append(int(byte, 16))
            message_data.extend([0] * (8 - message_bytes))
            data.append(message_data)

    np_data = np.array(data)
    p1 = figure(title="Byte 1", x_axis_label='time', y_axis_label='dunno')
    p2 = figure(title="Byte 2", x_axis_label='time', y_axis_label='dunno')
    p3 = figure(title="Byte 3", x_axis_label='time', y_axis_label='dunno')
    p4 = figure(title="Byte 4", x_axis_label='time', y_axis_label='dunno')
    p5 = figure(title="Byte 5", x_axis_label='time', y_axis_label='dunno')
    p6 = figure(title="Byte 6", x_axis_label='time', y_axis_label='dunno')
    p7 = figure(title="Byte 7", x_axis_label='time', y_axis_label='dunno')
    p8 = figure(title="Byte 8", x_axis_label='time', y_axis_label='dunno')
    time = np_data[:,0]
    trace1 = np_data[:,2]
    trace2 = np_data[:,3]
    trace3 = np_data[:,4]
    trace4 = np_data[:,5]
    trace5 = np_data[:,6]
    trace6 = np_data[:,7]
    trace7 = np_data[:,8]
    trace8 = np_data[:,9]
    # Ok this looks good. Time to make some pretty plots!!!

    p1.line(time, trace1, legend_label="Byte 1", line_width=2)
    p2.line(time, trace2, legend_label="Byte 2", line_width=2)
    p3.line(time, trace3, legend_label="Byte 3", line_width=2)
    p4.line(time, trace4, legend_label="Byte 4", line_width=2)
    p5.line(time, trace5, legend_label="Byte 5", line_width=2)
    p6.line(time, trace6, legend_label="Byte 6", line_width=2)
    p7.line(time, trace7, legend_label="Byte 7", line_width=2)
    p8.line(time, trace8, legend_label="Byte 8", line_width=2)

    script1, div1 = components(p1)
    script2, div2 = components(p2)
    script3, div3 = components(p3)
    script4, div4 = components(p4)
    script5, div5 = components(p5)
    script6, div6 = components(p6)
    script7, div7 = components(p7)
    script8, div8 = components(p8)

    scripts = [script1, script2, script3, script4, script5, script6, script7, script8]
    divs = [div1, div2, div3, div4, div5, div6, div7, div8]

    return scripts, divs


def get_plots_bitwise(asc_file, hex_id, instructions):
    regex = '(\d+.\d+)\s+(\d)\s+' + hex_id.upper() + '\s+Rx\s+d\s+(\d)\s(.+)\s\sL.+=\s(\d+)'
    starts_stops = []
    data = []
    first_message = True
    data_length_changes = False
    first_byte_length = None
    instruction_list = [x.strip() for x in instructions.split(',')]
    for item in instruction_list:
        split_item = item.split('-')
        start = int(split_item[0])
        stop = start + 1
        try:
            stop = int(split_item[1])
        except IndexError:
            pass
        starts_stops.append((start, stop))

    for encoded_line in asc_file:
        decoded_line = encoded_line.decode('UTF-8')
        message = re.search(regex, decoded_line)
        if message:
            message_bytes = int(message.group(3))
            if first_message:
                first_byte_length = message_bytes
                first_message = False
            else:
                if first_byte_length == message_bytes:
                    pass
                else:
                    data_length_changes = True

            timestamp = float(message.group(1))
            line_data = [timestamp]
            bin_string = ""
            for byte in message.group(4).split(' '):
                bin_string += format(int(byte, 16), '08b')
            bin_string = bin_string.ljust(64, '0')
            for start, stop in starts_stops:
                line_data.append(int(bin_string[start:stop], 2))
            data.append(line_data)

    np_data = np.array(data)
    scripts = []
    divs = []

    rows, cols = np_data.shape
    for item in range(cols-1):

        start, stop = starts_stops[item]
        if stop-start > 1:
            title = "Bits " + str(start) + '-' + str(stop)
        else:
            title = "Bit " + str(start)

        my_plot = figure(title=title, x_axis_label='time', y_axis_label='Value')
        time = np_data[:, 0]
        trace = np_data[:, item+1]
        my_plot.line(time, trace, legend_label=title, line_width=2)
        script, div = components(my_plot)
        scripts.append(script)
        divs.append(div)

    return scripts, divs, data_length_changes


