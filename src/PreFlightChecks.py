import json
import os
import os.path
import datetime
from xml.dom import minidom
import sys
import checkMethods
import logging

script = sys.argv[0]
filePath = sys.argv[1]
CFBundleShortVersionString = sys.argv[2]
CFBundleVersion = sys.argv[3]

print (" Script name: " + sys.argv[0] + "\n" + " FilePath: " + sys.argv[1] + "\n" + " CFBundleShortVersionString: " +
       sys.argv[2] + "\n" + " CFBundleVersion: " + sys.argv[3]) + "\n"

rootFolder = filePath + "/Products/Applications/GLA.app/"

logging.basicConfig(filename='errors.log',
                    format='%(asctime)s %(message)s ',
                    datefmt='%I:%M:%S',
                    filemode='w',
                    level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

now = datetime.datetime.now()

logging.info(now.strftime("%Y-%m-%d") + ' - Start iOS Preflight checks\n')


def initialcheck():
    '''
    First and vital check
    '''
    if (filePath + "/GLARelease*"):

        logging.info("1st condition satisfied - x.archive prefixed with 'GLARelease'")
        logging.info("")
    else:
        logging.info("Error - STOP! Don't go any further")
        sys.exit(1)


def check1():
    '''
    check1 - Locate the "ADBMobileConfig.json" file
    '''

    logging.info("Check 1: Locate the 'ADBMobileConfig.json'")
    logging.info("")

    fileName = rootFolder + "ADBMobileConfig.json"

    checkMethods.checkFileExists(fileName)

    try:
        with open(fileName) as data_file:
            checkData1 = json.load(data_file)

        rsids = checkData1["analytics"]["rsids"]
        server = checkData1["analytics"]["server"]

        checkMethods.checkValue("analytics.rsids", "guardiangu-globalapps-prod", rsids)
        checkMethods.checkValue("analytics.server", "hits-secure.theguardian.com", server)
        logging.info("")
    except IOError:
        logging.error("ERROR file missing: " + fileName)
        sys.exit(1)


def check2():
    '''
    check2 Locate all images prefixed with "AppIcon" and check that these are in fact valid app icon images)
    '''
    logging.info("Check 2: AppIcon's")
    logging.info("MANUAL check is needed - Goto: " + rootFolder)


def check3():
    '''
    check3 - Locate the "archived-expanded-entitlements.xcent)
    '''
    logging.info('\n')
    logging.info("Check 3: Locate the 'archived-expanded-entitlements.xcent'")

    fileName = rootFolder + "archived-expanded-entitlements.xcent"

    checkMethods.checkFileExists(fileName)

    try:
        data = checkMethods.loadPlist(fileName)

        checkMethods.checkListAny(
                "com.apple.developer.associated-domains",
                ["activitycontinuation:www.theguardian.com", "applinks:www.theguardian.com"],
                data["com.apple.developer.associated-domains"]
        )

        checkMethods.checkValue(
                "com.apple.security.application-groups",
                ["group.uk.co.guardian.iphone2"],
                data["com.apple.security.application-groups"]
        )

        checkMethods.checkValue(
                "keychain-access-groups",
                ["U9LTYR56M6.uk.co.guardian.SharedKeychain"],
                data["keychain-access-groups"]
        )
        logging.info('\n')
    except IOError:
        logging.error("ERROR file missing: " + fileName)
        sys.exit(1)


def check4():
    '''
    check4 - Locate the "embedded.mobileprovision)
    '''

    logging.info("Check 4: Locate the 'embedded.mobileprovision'")

    fileName = rootFolder + "embedded.mobileprovision"

    checkMethods.checkFileExists(fileName)

    try:
        with open(fileName, "r") as the_file:
            xml_string = checkMethods.xmlSnippet(the_file.read())

            xmldoc = minidom.parseString(xml_string)

            keyElems = xmldoc.getElementsByTagName("key")

            checkMethods.checkXMLValue(
                    keyElems,
                    "ApplicationIdentifierPrefix",
                    "U9LTYR56M6"
            )

            checkMethods.checkXMLValue(
                    keyElems,
                    "application-identifier",
                    "U9LTYR56M6.uk.co.guardian.iphone2"
            )

            checkMethods.checkXMLValue(
                    keyElems,
                    "aps-environment",
                    "production"
            )

            checkMethods.checkXMLValueTrue(
                    keyElems,
                    "beta-reports-active"
            )

            checkMethods.checkXMLValue(
                    keyElems,
                    "com.apple.developer.associated-domains",
                    "*"
            )

            checkMethods.checkXMLValue(
                    keyElems,
                    "com.apple.developer.team-identifier",
                    "998P9U5NGJ"
            )

            checkMethods.checkXMLValue(
                    keyElems,
                    "com.apple.security.application-groups",
                    "group.uk.co.guardian.iphone2"
            )

            checkMethods.checkXMLValueFalse(
                    keyElems,
                    "get-task-allow"
            )

            checkMethods.checkXMLValue(
                    keyElems,
                    "keychain-access-groups",
                    "U9LTYR56M6.*"
            )

            checkMethods.checkXMLValue(
                    keyElems,
                    "Name",
                    "Guardian Live App Store"
            )

            checkMethods.checkXMLValue(
                    keyElems,
                    "TeamName",
                    "Guardian News & Media Ltd"
            )
        logging.info('\n')
    except IOError:
        logging.error("ERROR file missing: " + fileName)
        sys.exit(1)


def check5():
    '''
    check5 - Locate the "GLA.entitlements"
    '''

    logging.info("Check 5: Locate the 'GLA.entitlements'")

    fileName = rootFolder + "GLA.entitlements"

    checkMethods.checkFileExists(fileName)

    try:
        with open(fileName, "r") as the_file:
            xml_string = checkMethods.xmlSnippet(the_file.read())

            xmldoc = minidom.parseString(xml_string)

            keyElems = xmldoc.getElementsByTagName("key")

            checkMethods.checkXMLValue(
                    keyElems,
                    "com.apple.developer.associated-domains",
                    "activitycontinuation:www.theguardian.com"
            )

            checkMethods.checkXMLValue(
                    keyElems,
                    "com.apple.security.application-groups",
                    "group.uk.co.guardian.iphone2"
            )

            checkMethods.checkXMLValueTrue(
                    keyElems,
                    "beta-reports-active"
            )

            checkMethods.checkXMLValue(
                    keyElems,
                    "keychain-access-groups",
                    "$(AppIdentifierPrefix)uk.co.guardian.SharedKeychain"
            )
        logging.info('\n')
    except IOError:
        logging.error("ERROR file missing: " + fileName)
        sys.exit(1)


def check6():
    '''
    check6 - Locate the "Info.plist"
    '''

    logging.info("Check 6: Locate the 'Info.plist'")

    fileName = rootFolder + "Info.plist"

    checkMethods.checkFileExists(fileName)

    try:
        data = checkMethods.loadPlist(fileName)

        checkMethods.checkValue(
                "BuildTier",
                "release",
                data["BuildTier"]
        )

        checkMethods.checkValue(
                "CFBundleIdentifier",
                "uk.co.guardian.iphone2",
                data["CFBundleIdentifier"]
        )

        checkMethods.checkValue(
                "CFBundleShortVersionString",
                CFBundleShortVersionString,
                data["CFBundleShortVersionString"]
        )

        checkMethods.checkValue(
                "CFBundleVersion",
                CFBundleVersion,
                data["CFBundleVersion"]
        )

        checkMethods.checkListAny(
                "UIDeviceFamily",
                [1, 2],
                data["UIDeviceFamily"]
        )
    except IOError:
        logging.error("ERROR file missing: " + fileName)
        sys.exit(1)


def check7():
    '''check7 - Locate the "templates-3.x.zip" file, the version number must match the "CFBundleShortVersionString"
    '''

    logging.info("Check 7: GLA.app - templates-3.x.zip")
    logging.info('\n')

    fileName = rootFolder + "templates-" + CFBundleShortVersionString + ".zip"

    checkMethods.checkFileExists(fileName)

    if os.path.exists(fileName):
        pass
        # logging.info("PASSED - " + templatesFileName)
    else:
        logging.info("ERROR: - " + fileName)
        sys.exit(1)


# Locate to the "Watch" folder and "Show Package Contents" for GLAWatchApp2


def check8():
    '''
    check8 - Locate the "archived-expanded-entitlements.xcent"
    '''

    logging.info("Check 8: Locate the 'archived-expanded-entitlements.xcent'")

    fileName = rootFolder + "/Watch/GLAWatchApp2.app/archived-expanded-entitlements.xcent"

    checkMethods.checkFileExists(fileName)

    try:
        data = checkMethods.loadPlist(fileName)

        checkMethods.checkValue(
                "application-identifier",
                "U9LTYR56M6.uk.co.guardian.iphone2.watchapp",
                data["application-identifier"]
        )

        checkMethods.checkValue(
                "keychain-access-groups",
                ["U9LTYR56M6.uk.co.guardian.iphone2.watchapp"],
                data["keychain-access-groups"]
        )
        logging.info('\n')
    except IOError:
        logging.error("ERROR file missing: " + fileName)
        sys.exit(1)


def check9():
    '''
    check9 - Locate the "embedded.mobileprovision"
    '''

    logging.info("Check 9: Locate the 'embedded.mobileprovision'")

    fileName = rootFolder + "Watch/GLAWatchApp2.app/embedded.mobileprovision"

    checkMethods.checkFileExists(fileName)

    try:
        with open(fileName, "r") as the_file:
            xml_string = checkMethods.xmlSnippet(the_file.read())

            xmldoc = minidom.parseString(xml_string)

            keyElems = xmldoc.getElementsByTagName("key")

            checkMethods.checkXMLValue(
                    keyElems,
                    "ApplicationIdentifierPrefix",
                    "U9LTYR56M6"
            )

            checkMethods.checkXMLValue(
                    keyElems,
                    "application-identifier",
                    "U9LTYR56M6.uk.co.guardian.iphone2.watchapp"
            )

            checkMethods.checkXMLValueTrue(
                    keyElems,
                    "beta-reports-active"
            )

            checkMethods.checkXMLValue(
                    keyElems,
                    "com.apple.developer.team-identifier",
                    "998P9U5NGJ"
            )

            checkMethods.checkXMLValueFalse(
                    keyElems,
                    "get-task-allow"
            )

            checkMethods.checkXMLValue(
                    keyElems,
                    "keychain-access-groups",
                    "U9LTYR56M6.*"
            )

            checkMethods.checkXMLValue(
                    keyElems,
                    "Name",
                    "Guardian Live WatchApp App Store"
            )

            checkMethods.checkXMLValue(
                    keyElems,
                    "TeamName",
                    "Guardian News & Media Ltd"
            )
        logging.info('\n')
    except IOError:
        logging.error("ERROR file missing: " + fileName)
        sys.exit(1)


def check10():
    '''
    check10 - Locate the "Info.plist"
    '''

    logging.info("Check 10: Locate the 'Info.plist'")

    fileName = rootFolder + "Watch/GLAWatchApp2.app/Info.plist"

    checkMethods.checkFileExists(fileName)

    try:
        data = checkMethods.loadPlist(fileName)

        checkMethods.checkValue(
                "CFBundleIdentifier",
                "uk.co.guardian.iphone2.watchapp",
                data["CFBundleIdentifier"]
        )

        checkMethods.checkValue(
                "CFBundleShortVersionString",
                CFBundleShortVersionString,
                data["CFBundleShortVersionString"]
        )

        checkMethods.checkValue(
                "CFBundleVersion",
                CFBundleVersion,
                data["CFBundleVersion"]
        )

        checkMethods.checkValue(
                "WKCompanionAppBundleIdentifier",
                "uk.co.guardian.iphone2",
                data["WKCompanionAppBundleIdentifier"]
        )

        checkMethods.checkValue(
                "UIDeviceFamily",
                [4],
                data["UIDeviceFamily"]
        )
        logging.info('\n')
    except IOError:
        logging.error("ERROR file missing: " + fileName)
        sys.exit(1)


def check11():
    '''
    check11 - Locate the "archived-expanded-entitlements.xcent"
    '''

    logging.info("Check 11: Locate the 'archived-expanded-entitlements.xcent'")

    fileName = rootFolder + "Watch/GLAWatchApp2.app/PlugIns/GLAExtensionWatchKit2.appex/archived-expanded-entitlements.xcent"

    checkMethods.checkFileExists(fileName)

    try:
        data = checkMethods.loadPlist(fileName)

        checkMethods.checkValue(
                "com.apple.security.application-groups",
                ["group.uk.co.guardian.iphone2"],
                data["com.apple.security.application-groups"]
        )

        checkMethods.checkValue(
                "keychain-access-groups",
                ["U9LTYR56M6.uk.co.guardian.SharedKeychain"],
                data["keychain-access-groups"]
        )
        logging.info('\n')
    except IOError:
        logging.error("ERROR file missing: " + fileName)
        sys.exit(1)


def check12():
    '''
    check12 - Locate the "embedded.mobileprovision"
    '''

    logging.info("Check 12: Locate the 'embedded.mobileprovision'")

    fileName = rootFolder + "Watch/GLAWatchApp2.app/PlugIns/GLAExtensionWatchKit2.appex/embedded.mobileprovision"

    checkMethods.checkFileExists(fileName)

    try:
        with open(fileName, "r") as the_file:
            xml_string = checkMethods.xmlSnippet(the_file.read())

            xmldoc = minidom.parseString(xml_string)

            keyElems = xmldoc.getElementsByTagName("key")

            checkMethods.checkXMLValue(
                    keyElems,
                    "ApplicationIdentifierPrefix",
                    "U9LTYR56M6"
            )

            checkMethods.checkXMLValue(
                    keyElems,
                    "application-identifier",
                    "U9LTYR56M6.uk.co.guardian.iphone2.watchapp.extw"
            )

            checkMethods.checkXMLValueTrue(
                    keyElems,
                    "beta-reports-active"
            )

            checkMethods.checkXMLValue(
                    keyElems,
                    "com.apple.developer.team-identifier",
                    "998P9U5NGJ"
            )

            checkMethods.checkXMLValue(
                    keyElems,
                    "com.apple.security.application-groups",
                    "group.uk.co.guardian.iphone2"
            )

            checkMethods.checkXMLValueFalse(
                    keyElems,
                    "get-task-allow"
            )

            checkMethods.checkXMLValue(
                    keyElems,
                    "keychain-access-groups",
                    "U9LTYR56M6.*"
            )

            checkMethods.checkXMLValue(
                    keyElems,
                    "Name",
                    "Guardian Live Extension WatchKit2 App Store"
            )

            checkMethods.checkXMLValue(
                    keyElems,
                    "TeamName",
                    "Guardian News & Media Ltd"
            )
        logging.info('\n')
    except IOError:
        logging.error("ERROR file missing: " + fileName)
        sys.exit(1)


def check13():
    '''
    check13: - Locate the 'Info.plist
    :return:
    '''

    logging.info("Check 13: Locate the 'Info.plist'")

    fileName = rootFolder + "Watch/GLAWatchApp2.app/PlugIns/GLAExtensionWatchKit2.appex/Info.plist"

    checkMethods.checkFileExists(fileName)

    try:
        data = checkMethods.loadPlist(fileName)

        checkMethods.checkValue("CFBundleIdentifier",
                                "uk.co.guardian.iphone2.watchapp.extw",
                                data["CFBundleIdentifier"]
                                )

        checkMethods.checkValue("CFBundleShortVersionString",
                                CFBundleShortVersionString,
                                data["CFBundleShortVersionString"]
                                )

        checkMethods.checkValue("CFBundleVersion",
                                CFBundleVersion,
                                data["CFBundleVersion"]
                                )

        application_groups = data["NSExtension"]["NSExtensionAttributes"]["WKAppBundleIdentifier"]
        checkMethods.checkValue(
                "WKAppBundleIdentifier",
                "uk.co.guardian.iphone2.watchapp",
                application_groups
        )

        checkMethods.checkValue(
                "UIDeviceFamily",
                [4],
                data["UIDeviceFamily"]
        )
        logging.info('\n')
    except IOError:
        logging.error("ERROR file missing: " + fileName)
        sys.exit(1)


def check14():
    '''
    check14 - Locate the "ADBMobileConfig.json" file
    '''

    logging.info("Check 14: Locate the 'ADBMobileConfig.json'")

    fileName = rootFolder + "PlugIns/GLAExtensionToday.appex/ADBMobileConfig.json"

    checkMethods.checkFileExists(fileName)

    try:
        with open(fileName) as data_file:
            checkData1 = json.load(data_file)

        rsids = checkData1["analytics"]["rsids"]
        server = checkData1["analytics"]["server"]

        checkMethods.checkValue("analytics.rsids", "guardiangu-globalapps-prod", rsids)
        checkMethods.checkValue("analytics.server", "hits-secure.theguardian.com", server)

        logging.info('\n')
    except IOError:
        logging.error("ERROR file missing: " + fileName)
        sys.exit(1)


def check15():
    '''
    check15 - Locate the "archived-expanded-entitlements.xcent"
    '''

    logging.info("Check 15: Locate the 'archived-expanded-entitlements.xcent'")

    fileName = rootFolder + "PlugIns/GLAExtensionToday.appex/archived-expanded-entitlements.xcent"

    checkMethods.checkFileExists(fileName)

    try:

        data = checkMethods.loadPlist(fileName)

        checkMethods.checkValue(
                "com.apple.security.application-groups",
                ["group.uk.co.guardian.iphone2"],
                data["com.apple.security.application-groups"]
        )

        checkMethods.checkValue(
                "keychain-access-groups",
                ["U9LTYR56M6.uk.co.guardian.SharedKeychain"],
                data["keychain-access-groups"]
        )
        logging.info('\n')
    except IOError:
        logging.error("ERROR file missing: " + fileName)
        sys.exit(1)


def check16():
    '''
    check16 - Locate the "embedded.mobileprovision"
    '''

    logging.info("Check 16: Locate the 'embedded.mobileprovision'")

    fileName = rootFolder + "PlugIns/GLAExtensionToday.appex/embedded.mobileprovision"

    checkMethods.checkFileExists(fileName)

    try:
        with open(fileName, "r") as the_file:
            xml_string = checkMethods.xmlSnippet(the_file.read())

            xmldoc = minidom.parseString(xml_string)

            keyElems = xmldoc.getElementsByTagName("key")

            checkMethods.checkXMLValue(
                    keyElems,
                    "ApplicationIdentifierPrefix",
                    "U9LTYR56M6"
            )

            checkMethods.checkXMLValue(
                    keyElems,
                    "application-identifier",
                    "U9LTYR56M6.uk.co.guardian.iphone2.extt"
            )

            checkMethods.checkXMLValueTrue(
                    keyElems,
                    "beta-reports-active"
            )

            checkMethods.checkXMLValue(
                    keyElems,
                    "com.apple.developer.team-identifier",
                    "998P9U5NGJ"
            )

            checkMethods.checkXMLValue(
                    keyElems,
                    "com.apple.security.application-groups",
                    "group.uk.co.guardian.iphone2"
            )

            checkMethods.checkXMLValueFalse(
                    keyElems,
                    "get-task-allow"
            )

            checkMethods.checkXMLValue(
                    keyElems,
                    "keychain-access-groups",
                    "U9LTYR56M6.*"
            )

            checkMethods.checkXMLValue(
                    keyElems,
                    "Name",
                    "Guardian Live Extension Today App Store"
            )

            checkMethods.checkXMLValue(
                    keyElems,
                    "TeamName",
                    "Guardian News & Media Ltd"
            )
        logging.info('\n')
    except IOError:
        logging.error("ERROR file missing: " + fileName)
        sys.exit(1)


def check17():
    '''
    check17 - Locate the "Info.plist"
    '''

    logging.info("Check 17: Locate the 'Info.plist'")

    fileName = rootFolder + "PlugIns/GLAExtensionToday.appex/Info.plist"

    checkMethods.checkFileExists(fileName)

    try:

        data = checkMethods.loadPlist(fileName)

        checkMethods.checkValue(
                "CFBundleIdentifier",
                "uk.co.guardian.iphone2.extt",
                data["CFBundleIdentifier"]
        )

        checkMethods.checkValue(
                "CFBundleShortVersionString",
                CFBundleShortVersionString,
                data["CFBundleShortVersionString"]
        )

        checkMethods.checkValue(
                "CFBundleVersion",
                CFBundleVersion,
                data["CFBundleVersion"]
        )

        checkMethods.checkListAny(
                "UIDeviceFamily",
                [1, 2],
                data["UIDeviceFamily"]
        )
        logging.info('\n')
    except IOError:
        logging.error("ERROR file missing: " + fileName)
        sys.exit(1)


def check18():
    '''
    check18 - Locate the "archived-expanded-entitlements.xcent"
    :return:
    '''

    logging.info("Check 18: Locate the 'archived-expanded-entitlements.xcent'")

    fileName = rootFolder + "PlugIns/GLAExtensionWatchKit.appex/archived-expanded-entitlements.xcent"

    checkMethods.checkFileExists(fileName)

    try:
        data = checkMethods.loadPlist(fileName)

        checkMethods.checkValue(
                "com.apple.security.application-groups",
                ["group.uk.co.guardian.iphone2"],
                data["com.apple.security.application-groups"]
        )

        checkMethods.checkValue(
                "keychain-access-groups",
                ["U9LTYR56M6.uk.co.guardian.SharedKeychain"],
                data["keychain-access-groups"]
        )
        logging.info('\n')
    except IOError:
        logging.error("ERROR file missing: " + fileName)
        sys.exit(1)


def check19():
    '''
    check19 - Locate the "embedded.mobileprovision"
    '''

    logging.info("Check 19: Locate the 'embedded.mobileprovision'")

    fileName = rootFolder + "PlugIns/GLAExtensionWatchKit.appex/embedded.mobileprovision"

    checkMethods.checkFileExists(fileName)

    try:
        with open(fileName, "r") as the_file:
            xml_string = checkMethods.xmlSnippet(the_file.read())

            xmldoc = minidom.parseString(xml_string)

            keyElems = xmldoc.getElementsByTagName("key")

            checkMethods.checkXMLValue(
                    keyElems,
                    "ApplicationIdentifierPrefix",
                    "U9LTYR56M6"
            )

            checkMethods.checkXMLValue(
                    keyElems,
                    "application-identifier",
                    "U9LTYR56M6.uk.co.guardian.iphone2.extw"
            )

            checkMethods.checkXMLValueTrue(
                    keyElems,
                    "beta-reports-active"
            )

            checkMethods.checkXMLValue(
                    keyElems,
                    "com.apple.developer.team-identifier",
                    "998P9U5NGJ"
            )

            checkMethods.checkXMLValue(
                    keyElems,
                    "com.apple.security.application-groups",
                    "group.uk.co.guardian.iphone2"
            )

            checkMethods.checkXMLValueFalse(
                    keyElems,
                    "get-task-allow"
            )

            checkMethods.checkXMLValue(
                    keyElems,
                    "keychain-access-groups",
                    "U9LTYR56M6.*"
            )

            checkMethods.checkXMLValue(
                    keyElems,
                    "Name",
                    "Guardian Live Extension WatchKit App Store"
            )

            checkMethods.checkXMLValue(
                    keyElems,
                    "TeamName",
                    "Guardian News & Media Ltd"
            )
        logging.info('\n')
    except IOError:
        logging.error("ERROR file missing: " + fileName)
        sys.exit(1)


def check20():
    '''
    check20 - Locate the "Info.plist"
    '''

    logging.info("Check 20: Locate the 'Info.plist'")

    fileName = rootFolder + "PlugIns/GLAExtensionWatchKit.appex/Info.plist"

    checkMethods.checkFileExists(fileName)

    try:
        data = checkMethods.loadPlist(fileName)

        checkMethods.checkValue(
                "CFBundleIdentifier",
                "uk.co.guardian.iphone2.extw",
                data["CFBundleIdentifier"]
        )

        checkMethods.checkValue(
                "CFBundleShortVersionString",
                CFBundleShortVersionString,
                data["CFBundleShortVersionString"]
        )

        checkMethods.checkValue(
                "CFBundleVersion",
                CFBundleVersion,
                data["CFBundleVersion"]
        )

        application_groups = data["NSExtension"]["NSExtensionAttributes"]["WKAppBundleIdentifier"]
        checkMethods.checkValue(
                "WKAppBundleIdentifier",
                "uk.co.guardian.iphone2.watchapp",
                application_groups
        )

        checkMethods.checkListAny(
                "UIDeviceFamily",
                [1],
                data["UIDeviceFamily"]
        )
        logging.info('\n')
    except IOError:
        logging.error("ERROR file missing: " + fileName)
        sys.exit(1)


def check21():
    '''
    check21 - Locate the "archived-expanded-entitlements.xcent"
    :return:
    '''

    logging.info("Check 21: Locate the 'archived-expanded-entitlements.xcent'")

    fileName = rootFolder + "PlugIns/GLAExtensionWatchKit.appex/GLAWatchApp.app/archived-expanded-entitlements.xcent"

    checkMethods.checkFileExists(fileName)

    try:
        data = checkMethods.loadPlist(fileName)

        checkMethods.checkValue(
                "application-identifier",
                "U9LTYR56M6.uk.co.guardian.iphone2.watchapp",
                data["application-identifier"]
        )

        checkMethods.checkValue(
                "keychain-access-groups",
                ["U9LTYR56M6.uk.co.guardian.iphone2.watchapp"],
                data["keychain-access-groups"]
        )
        logging.info('\n')
    except IOError:
        logging.error("ERROR file missing: " + fileName)
        sys.exit(1)


def check22():
    '''
    check22 - Locate the "embedded.mobileprovision"
    '''

    logging.info("Check 22: Locate the 'embedded.mobileprovision'")

    fileName = rootFolder + "PlugIns/GLAExtensionWatchKit.appex/GLAWatchApp.app/embedded.mobileprovision"

    checkMethods.checkFileExists(fileName)

    try:
        with open(fileName, "r") as the_file:
            xml_string = checkMethods.xmlSnippet(the_file.read())

            xmldoc = minidom.parseString(xml_string)

            keyElems = xmldoc.getElementsByTagName("key")

            checkMethods.checkXMLValue(
                    keyElems,
                    "ApplicationIdentifierPrefix",
                    "U9LTYR56M6"
            )

            checkMethods.checkXMLValue(
                    keyElems,
                    "application-identifier",
                    "U9LTYR56M6.uk.co.guardian.iphone2.watchapp"
            )

            checkMethods.checkXMLValueTrue(
                    keyElems,
                    "beta-reports-active"
            )

            checkMethods.checkXMLValue(
                    keyElems,
                    "com.apple.developer.team-identifier",
                    "998P9U5NGJ"
            )

            checkMethods.checkXMLValueFalse(
                    keyElems,
                    "get-task-allow"
            )

            checkMethods.checkXMLValue(
                    keyElems,
                    "keychain-access-groups",
                    "U9LTYR56M6.*"
            )

            checkMethods.checkXMLValue(
                    keyElems,
                    "Name",
                    "Guardian Live WatchApp App Store"
            )

            checkMethods.checkXMLValue(
                    keyElems,
                    "TeamName",
                    "Guardian News & Media Ltd"
            )
        logging.info('\n')
    except IOError:
        logging.error("ERROR file missing: " + fileName)
        sys.exit(1)


def check23():
    '''
    check23 - Locate the "Info.plist"
    '''

    logging.info("Check 23: Locate the 'Info.plist'")

    fileName = rootFolder + "PlugIns/GLAExtensionWatchKit.appex/GLAWatchApp.app/Info.plist"

    checkMethods.checkFileExists(fileName)

    try:
        data = checkMethods.loadPlist(fileName)

        checkMethods.checkValue(
                "CFBundleIdentifier",
                "uk.co.guardian.iphone2.watchapp",
                data["CFBundleIdentifier"]
        )

        checkMethods.checkValue(
                "CFBundleShortVersionString",
                CFBundleShortVersionString,
                data["CFBundleShortVersionString"]
        )

        checkMethods.checkValue(
                "CFBundleVersion",
                CFBundleVersion,
                data["CFBundleVersion"]
        )

        checkMethods.checkValue(
                "WKCompanionAppBundleIdentifier",
                "uk.co.guardian.iphone2",
                data["WKCompanionAppBundleIdentifier"]
        )

        checkMethods.checkListAny(
                "UIDeviceFamily",
                [4],
                data["UIDeviceFamily"]
        )
        logging.info('\n')
    except IOError:
        logging.error("ERROR file missing: " + fileName).upper()
        sys.exit(1)


# Go through the Checks
initialcheck(),
check1(), check2(), check3(), check4(), check5(),
check6(), check7(), check8(), check9(), check10(),
check11(), check12(), check13(), check14(), check15(),
check16(), check17(), check18(), check19(), check20(),
check21(), check22(), check23()

logging.info(now.strftime("%Y-%m-%d %H:%M") + 'Finished iOS Preflight Checks\n')
