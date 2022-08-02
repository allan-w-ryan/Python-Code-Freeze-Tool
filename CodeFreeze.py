#
# ReleaseFreeze_FullyAutomated.py
#
# Created by Allan Ryan on 2/28/22
#

import github 
import gitHelper
import plistHelper
import csvHelper
import releaseInfo
import errors
import diffGenerator


access_token = input("Please enter your GitHub access token: ")
gitHelper_instance = gitHelper.GitHelper(access_token)

current_release = plistHelper.get_current_release_info_from_plist(gitHelper_instance)
next_release = csvHelper.get_next_releaseInfo_from_csv(gitHelper_instance, current_release)
plistHelper.update_plist_for_next_release(gitHelper_instance, next_release)
diffGenerator.generate_feature_flag_report(gitHelper_instance, current_release, next_release)

