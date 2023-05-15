from parse import compile
from parse import with_pattern
import datetime as dt
import pandas as pd
import json

def create_log_list(log_file):
    logs = open(log_file)
    lines  = logs.readlines()
    log_list = []
    log = ''
    for line in lines:
        if line[:11] == "2014/Oct/24":
            log_list.append(log)
            log = line
        else:
            log += line

    log_list = log_list[1:]
    return log_list

log_list = create_log_list('WCG100140020.txt')

def portevent_filter(log_list):
    portevent_log_list = []
    file = open('porteventlogs.txt', 'w')
    for log in log_list:
        if "PORTEVENT" in log:
            log_line = log.replace('\n', '')
            portevent_log_list.append(log_line)
            file.write(log_line)
    return portevent_log_list

portevent_log_list  = portevent_filter(log_list)

def sending_message_filter(log_list):
    sending_log_list = []
    for log in log_list:
        if "Sent on" in log:
            sending_log_list.append(log)
    return sending_log_list

sending_log_list = sending_message_filter(log_list)

@with_pattern(r"\d\d\d\d/\d\d/\d\d \d\d:\d\d:\d\d.\d\d\d\d\d\d")
def date_format(date_time_str):
    return dt.datetime.strptime(date_time_str, '%Y/%b/%d %H:%M:%S.%f')

port_opening = compile("{date:27} {user_name} {eventtype} {unknown_part} Port {portname} was started.")
port_stopping = compile("{date:27} {user_name} {eventtype} {unknown_part} Port {portname} was stopped.")
port_connexion_waiting = compile("{date:27} {message_receiver} {eventtype} {unknown_part} Port {message_receiver_portname} is waiting for connection from {message_sender_portname} on {communication_type} pathname {pathname}.")
port_connexion_establishment = compile("{date:27} {message_sender} {eventtype} {unknown_part} Port {message_sender_portname} has established the connection with {message_receiver_portname} using transport type {communication_type}.")
port_connexion_acceptance = compile("{date:27} {message_receiver} {eventtype} {unknown_part} Port {message_receiver_portname} has accepted the connection from {message_sender_portname}.")
port_mapping = compile("{date:27} {message_sender} {eventtype} {unknown_part} Port {message_sender_portname} was mapped to {message_receiver_portname}.")
message_sending = compile("{date:27} {message_sender} {eventtype} {unknown_part} Sent on {message_sender_portname} to {message_receiver} {message_type} : {message_content:0}")
message_enqueuing = compile("{date:27} {message_receiver} {eventtype} {unknown_part} Message enqueued on {message_receiver_portname} from {message_sender} {message_type} : {message_content:0} id {message_id_number}")
message_reception = compile("{date:27} {message_receiver} {eventtype} {unknown_part} Receive operation on port {message_receiver_portname} succeeded, message from {message_sender}: {message_type} : {message_content:0} id {message_id_number}")
message_extraction = compile("{date:27} {message_receiver} {eventtype} {unknown_part} Message with id {message_id_number} was extracted from the queue of {message_receiver_portname}.")

def create_log_sending_message_dataframe(sending_log_list):
    parsed_sending_log_dico = {'date': [], 'message_sender': [], 'eventtype': [], 'unknown_part': [], 'message_sender_portname': [], 
                            'message_receiver': [], 'message_type': [], 'message_content': []}
    for sending_log in sending_log_list:
        parsed_log = message_sending.parse(sending_log).named
        for k in parsed_log.keys():
            parsed_sending_log_dico[k].append(parsed_log[k])
    df = pd.DataFrame(parsed_sending_log_dico)
    return df

df = create_log_sending_message_dataframe(sending_log_list)

def log_format_to_json(string):

    #decompose the all string into lines and then words to check patterns and modify it to a json string 
    lines = string.split('\n')
    edited_message = ''
    for line in lines: 
        decompose_line = line.split(' ')
        edited_line = ''

        #study patterns of the line to make the appropriate modification to turn it into a json valid line
        for i in range(len(decompose_line)):

            if decompose_line[i] != '':

                #add quote around keys
                if decompose_line[i] == ':=':
                    decompose_line[i-1] = '"' + decompose_line[i-1] + '"'

                    #add quote around all the values which are not dictionaries so it is easier to reach a json format
                    if decompose_line[i+1] != '{':
                        if '"' == decompose_line[i+1][0]:
                            break
                        else:
                            if i + 1 == len(decompose_line) - 1:
                                if ',' == decompose_line[i+1][-1]:
                                    decompose_line[i+1] = '"' + decompose_line[i+1].replace(',','') + '",'
                                else:
                                    decompose_line[i+1] = '"' + decompose_line[i+1] + '"'
                            else:
                                if ',' == decompose_line[-1][-1]:
                                    decompose_line[i+1] = '"' + decompose_line[i+1]
                                    decompose_line[-1] =  decompose_line[-1].replace(',','') + '",'
                                    break
                                else:
                                    decompose_line[i+1] = '"' + decompose_line[i+1]
                                    decompose_line[-1] =  decompose_line[-1] + '"'
                                    break

        #recreate the all string from the decomposed lines which has been modified
        for e in decompose_line:
            if e == '':
                edited_line += ' '
            if e == ':=':
                edited_line += ' ' + e + ' '
            else:
                edited_line += e
        edited_message += edited_line + '\n'
    
    #modify the all string again to transform unappropriate inside dictionaries into list which are easier handled by json 
    edited_message = edited_message.split(' ')
    open = 0
    ind = []
    for i in range(len(edited_message)):

        #change open braces ('{') into open square bracelets ('[')
        if '{' in edited_message[i]:
            if edited_message[i].count('}') > 1:
                for y in range(edited_message[i].count('}')):
                    open += 1
            else:
                open += 1
                f = list(filter(('').__ne__, edited_message[i:]))
                if len(f) > 0:
                    if '{' in f[1]:
                        edited_message[i] = edited_message[i].replace('{', '[',-1)
                        ind.append(open)
                    if '"' == f[1][0] and f[2] != ':=':
                        edited_message[i] = edited_message[i].replace('{', '[',-1)
                        ind.append(open)

        #change closing braces ('}') into closing square bracelets (']')
        if '}' in edited_message[i]:
            if edited_message[i].count('}') > 1:
                for y in range(edited_message[i].count('}')):
                    if len(ind) != 0 and open == ind[-1]:
                        s = ""
                        dico_i_split = edited_message[i].split('}')
                        for l in range(len(dico_i_split) - 1):
                            if l == y:
                                s += dico_i_split[l] + ']'
                            else:
                                s += dico_i_split[l] + '}'
                        s += dico_i_split[-1]
                        edited_message[i] = s
                        ind.pop(-1)
                    open -= 1
            else:
                if len(ind) != 0 and open == ind[-1]:
                    edited_message[i] = edited_message[i].replace('}',']',1)
                    ind.pop(-1)
                open -= 1

    #recreate the json string from the decomposed one that we created to transform dictionaries into lists
    for i in range(len(edited_message)):
        if edited_message[i] == '':
            edited_message[i] = ' '
    
    json_string = ""
    for i in range(len(edited_message)):
        json_string += edited_message[i]
    json_string = json_string.replace('=', '')
    
    return json_string

def json_string_to_dict(string):
    dict_json = json.loads(string)
    return dict_json

def message_to_dict(message):
    return json_string_to_dict(log_format_to_json(message))

