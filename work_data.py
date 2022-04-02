import xml.etree.ElementTree as ET
from xml.etree import ElementTree
from datetime import datetime, timedelta
from pytz import timezone
import json
import pandas as pd
import numpy as np


datetime_now = datetime.now()
ts = datetime_now.strftime('%Y%m%d::%H%M%S')


def set_file_content(tree):
    with open('{}_test_payload1.xml'.format(ts), 'wb') as f:
        f.write(tree)
        f.flush()


def set_xml_content(X, Y):
    '''
    1. Create a python method that takes arguments int X and int Y,
     and updates DEPART and RETURN fields
    :param xml_string:
    :param X:
    :param Y:
    :return:
    '''
    with open('test_payload1.xml') as xml_file:
        time_delta_x = timedelta(days=X)
        time_delta_y = timedelta(days=Y)
        tree = ET.fromstring(xml_file.read())
        for elem in tree.iter():
            if elem.tag in 'DEPART':
                depart_time = datetime_now + time_delta_x
                elem.text = depart_time.strftime('%Y%m%d')
            elif elem.tag in 'RETURN':
                return_time = datetime_now + time_delta_y
                elem.text = return_time.strftime('%Y%m%d')
    xmlstr = ElementTree.tostring(tree, encoding='utf8', method='xml')
    set_file_content(xmlstr)


def remove_json_element(elements):
    '''
    2. Create a python method that takes a json element
    as an argument, and removes that element from test_payload.json.

    Please verify that the method can remove either nested or non-nested elements
    (try removing "outParams" and "appdate").
    :return:
    '''
    def nested_del(dic, keys):
        for key in keys[:-1]:
            dic = dic.setdefault(key, {})
        del dic[keys[-1]]

    with open('test_payload.json') as json_file:
        json_data = json.load(json_file)
        nested_del(json_data, elements)

    fh = open("{}_test_payload.json".format(ts), "w")
    fh.write(json.dumps(json_data, indent=4))
    fh.close()


def parse_jmeter_file(file_name):
    '''
    3. label, response code, response message, failure message,
    and the time of non-200 response
    :param file_name:
    :return:
    '''

    def convert_string_to_pst(time_string):
        readable = datetime.fromtimestamp(round(int(time_string) / 1000)).isoformat()
        pacific_timezone = timezone('US/Pacific')
        temp = datetime.strptime(readable, '%Y-%m-%dT%H:%M:%S')
        pst_time = pacific_timezone.localize(temp)
        return pst_time.strftime("%Y-%m-%d %H:%M:%S %Z%z")

    df = pd.read_csv(file_name)
    data_points = np.where(df['responseCode'] != 200)

    for it in data_points[0].tolist():
        el = df.loc[it]
        print_msg = "label: {label}, responseCode: {responseCode}, " \
                    "responseMessage: {responseMessage}, failureMessage: {failureMessage}" \
                    "time: {time}".format(
            label=el['label'], responseCode=el['responseCode'], responseMessage=el['responseMessage'],
            failureMessage=el['failureMessage'], time=convert_string_to_pst(el['timeStamp'])
        )
        print(print_msg)


if __name__ == "__main__":
    # calling main function
    # task 1
    set_xml_content(5, 10)
    # task 2
    remove_json_element(['inParams', 'planselect_1'])
    # task 3
    parse_jmeter_file('Jmeter_log1.jtl')

