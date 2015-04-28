#!/usr/bin/env python2
import binascii
import sys
import datetime

IMEI = '864595027992746'

if len(sys.argv) <= 1:
    print('Usage: ' + sys.argv[0] + ' <sqlite SQL dump>')
    sys.exit(1)

try:
    f = open(sys.argv[1])
except:
    print('File ' + sys.argv[1] + ' does not exist')
    sys.exit(1)

def extract_fields(line):
    content = line[ line.find('(') + 1 : line.rfind(')') ]
    fieldmap = dict()
    fieldcnt = 0
    for field in content.split(','):
        if field.find('(') != -1: # if subclause in column, it is end of columns statement
            break
        fieldmap[field.split(' ')[0]] = fieldcnt
        fieldcnt += 1
    return [ fieldmap, fieldcnt ]

def decrypt_msg(encmsg_bin):
    key = IMEI
    key_len = len(key)
    encmsg_len = len(encmsg_bin)
    decmsg = ''
    for i in range(0, encmsg_len):
        decmsg += chr(ord(encmsg_bin[i]) ^ ord(key[i % key_len]))
    return decmsg

def decrypt_hex(encmsg_hex):
    encmsg_bin = binascii.unhexlify(encmsg_hex)
    return decrypt_msg(encmsg_bin)

def extract_username(line):
    namepart = line[0 : line.find('_New')]
    userhash = namepart[namepart.rfind('_') + 1 : ]
    return userhash


friend_fieldmap = dict()
friend_fieldcnt = 0
fieldmap = dict()
fieldcnt = 0

for line in f:
    if line.startswith('CREATE TABLE mr_friend_'):
        friend_fieldmap, friend_fieldcnt = extract_fields(line)

    if line.startswith('CREATE TABLE mr_discusssion_'):
        fieldmap, fieldcnt = extract_fields(line)

    if line.startswith('INSERT INTO "mr_discusssion_'):
        username = extract_username(line)
        content = line[ line.find('(') + 1 : line.rfind(')') ]
        fields = content.split(',')
        if len(fields) != fieldcnt:
            continue
        msgData = fields[fieldmap['msgData']]
        if msgData.startswith("X'"):
            decmsg = decrypt_hex(msgData[2:-1])
        else:
            decmsg = ''
        self_id = decrypt_msg(fields[fieldmap['selfuin']][1:-1])
        sender_id = decrypt_msg(fields[fieldmap['senderuin']][1:-1])
        timestamp = fields[fieldmap['time']]
        time_str = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
        print('\t'.join([username, time_str, self_id, sender_id, decmsg]))

