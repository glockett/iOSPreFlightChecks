import plistlib
import tempfile
import subprocess
import os
import os.path
from xml.dom import Node
import logging

import sys


def next_element(node):
    '''
    Function to find the next node in a jSon file
    :param elem: the element to check for true or false
    :return: next
    '''
    next = node.nextSibling
    while (next is not None) and (next.nodeType is not Node.ELEMENT_NODE):
        next = next.nextSibling
    return next


def all_strings(elem):
    '''
    Function to get all the  elements in th file (elem may be a <string> or an <array>)
    :param elem:
    :return:
    '''
    # elem may be a <string> or an <array> containing strings
    result = []
    if elem.tagName == "string":
        result.append(elem.firstChild.data)
    elif elem.tagName == "array":
        for string_elem in elem.getElementsByTagName("string"):
            result.append(string_elem.firstChild.data)
    return result


def boolean_from_element(elem):
    '''
    Function to convert <true/> and <false/> XML elements to Python True and False booleans
    :param elem: the element to check for true or false
    :return: proper python True or False value
    '''
    if elem.tagName == "true":
        return True
    elif elem.tagName == "false":
        return False
    else:
        raise ValueError("Element is not <true/> or <false/>")


def fileCheck(filePath):
    '''
    Function to check the file exosts
    :param filePath:
    :return boolean:
    '''
    if os.path.exits(filePath):
        return
    else:
        logging.error("Error - STOP! File cannot be found")
        logging.info('\n')
        quit()
    return


def xmlSnippet(all_contents):
    '''
    Function to generate a snippet of XML using Begin and End tag
    :param all_contents:
    :return: snippet
    '''
    begin_tag = "<?xml"
    end_tag = "</plist>"
    begin_index = all_contents.index(begin_tag)
    end_index = all_contents.rfind(end_tag) + len(end_tag)
    snippet = all_contents[begin_index:end_index]
    return snippet


def loadPlist(file):
    '''
    Function to create a dictionary list from a plist file
    :param file:
    :return: plist
    '''
    with tempfile.NamedTemporaryFile() as xml_plist:
        subprocess.check_call([
            "plutil",
            "-convert",
            "xml1",
            "-o", xml_plist.name,
            file
        ])

        plist = plistlib.readPlistFromString(xml_plist.read())

    return plist



def checkValue(key, requiredVal, actualVal):
    if requiredVal == actualVal:
        pass
        logging.info("PASSED - " + key + ": " + str(actualVal))
    else:
        logging.error("ERROR - " + key + ": " + str(actualVal))


def checkListAny(key, possibleValues, actualVal):
    for possibleValue in possibleValues:
        if (possibleValue in actualVal):
            pass
            logging.info("PASSED - " + key + ": " + str(actualVal))
            return
    logging.error("ERROR - " + key + ": " + actualVal)


def checkXMLValue(keyElems, key, requiredVal):
    for elem in keyElems:
        elemkey = elem.firstChild.data

        if elemkey == key:
            next_elem = next_element(elem)
            strings = all_strings(next_elem)

            if requiredVal in strings:
                pass
                logging.info("PASSED - " + key + ": " + str(strings))
                return
            else:
                logging.error("ERROR - " + key + ": " + str(strings))
                return
    logging.error("ERROR - " + key + ": element is missing!")


def checkXMLValueTrue(keyElems, key):
    for elem in keyElems:
        elemkey = elem.firstChild.data

        if elemkey == key:
            next_elem = next_element(elem)
            strings = all_strings(next_elem)

            if boolean_from_element(next_elem):
                pass
                logging.info("PASSED - " + key + ": " + str(strings))
                return
            else:
                logging.error("ERROR - " + key + ": " + str(strings))
                return
    logging.error("ERROR - " + key + ": element is missing!")


def checkXMLValueFalse(keyElems, key):
    for elem in keyElems:
        elemkey = elem.firstChild.data

        if elemkey == key:
            next_elem = next_element(elem)
            strings = all_strings(next_elem)

            if boolean_from_element(next_elem):
                logging.error("ERROR - " + key + ": " + str(strings))
                return
            else:
                pass
                logging.info("PASSED - " + key + ": " + str(strings))
                return
    logging.error("ERROR - " + key + ": element is missing!")


def checkFileExists(fileName):

    if os.path.isfile(fileName) and os.access(fileName, os.R_OK):
         pass
    else:
        logging.error("ERROR file missing: " + fileName)
        sys.exit(1)

