#
# plistHelper.py
#
# Created by Allan Ryan 3/2/22
#

import os
import plistlib
import releaseInfo


class plistHelper:
	pass

__m = plistHelper()
__m.SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
__m.RELEASE_PLIST_FILE = "release.plist"
__m.RELEASE_NAME_KEY = "SLKReleaseName"
__m.RELEASE_VERSION_KEY = "CFBundleShortVersionString"
__m.plist = None

def parse_plist_if_readable(plist_file):
	try:
		return plistlib.loads(plist_file)
	except:
		print("==== ERROR: Unable to read", __m.RELEASE_PLIST_FILE)
		print("==== Halting Execution)")
		exit(1)


def update_plist_for_next_release(gitHelper_instance, next_release):
	__m.plist[__m.RELEASE_NAME_KEY] = next_release.name
	__m.plist[__m.RELEASE_VERSION_KEY] = next_release.version
	plist_data = plistlib.writePlistToBytes(__m.plist)
	gitHelper_instance.push(plist_data, next_release, __m.RELEASE_PLIST_FILE)

def get_current_release_info_from_plist(gitHelper_instance):
	plist_file_data = gitHelper_instance.pull_file(__m.RELEASE_PLIST_FILE)
	__m.plist = parse_plist_if_readable(plist_file_data)
	next_release_info = releaseInfo.ReleaseInfo(__m.plist.get(__m.RELEASE_NAME_KEY, None), __m.plist.get(__m.RELEASE_VERSION_KEY, None))

	if next_release_info.name is None or next_release_info.version is None:
		print("==== ERROR: The required data was not found in " +  __m.RELEASE_PLIST_FILE + ".")
		print("==== Pleese check the plist for " + __m.RELEASE_PLIST_FILE + " and " + __m.RELEASE_VERSION_KEY)
		print("==== Halting Execution")
		exit(1)
	else:
		return next_release_info

