#
# csvHelper.py
#
# Created by Allan Ryan 3/1/22
#

import os
import csv
import releaseInfo


SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
RELEASE_INFO_CSV_FILE = "releng/release_info.csv"

def create_csv_reader_from_data(csv_file_data):
	try:
		csv_string_data = csv_file_data.decode('utf-8')
		lines = csv_string_data.splitlines()
		return csv.reader(lines)
	except:
		print("==== ERROR: Unable to read", __m.RELEASE_INFO_CSV_FILE)
		print("==== Halting Execution)")
		exit(1)

def parse_csv(csv_file_reader, current_release):
	next_release_info = releaseInfo.ReleaseInfo(None, None)
	for row in csv_file_reader:
		if current_release.name == row[0] and current_release.version == row[1]:
			# Current Release found in CSV file. Return name/version for next 
			# release (assuming releases are ordered by version number)
			release = next(csv_file_reader)
			next_release_info.name = release[0]
			next_release_info.version = release[1]
			break

	if next_release_info.name is None or next_release_info.version is None:
		print("==== ERROR: The required data was not found in " +  __m.RELEASE_INFO_CSV_FILE + ".")
		print("==== Halting Execution")
		exit(1)
	else:
		return next_release_info

def get_next_releaseInfo_from_csv(gitHelper_instance, current_release):
	csv_file_data = gitHelper_instance.pull_file(RELEASE_INFO_CSV_FILE)
	csv_reader = create_csv_reader_from_data(csv_file_data)
	return parse_csv(csv_reader, current_release)