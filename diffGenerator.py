#
# diffGenerator
#
# Created by Allan Ryan
#
import difflib
import os

FEATURE_FLAG_PATH = "featureflags/FF.csv"
DIF_FILE_PATH = "diff/FF.csv.diff"

def write_dif_file(diff):
	filename = DIF_FILE_PATH
	os.makedirs(os.path.dirname(filename), exist_ok=True)
	with open(filename, "w") as file:
		for line in diff:
			file.write(line + "\n")
		file.close()

def generate_feature_flag_report(gitHelper_instance, current_release, next_release):
	current_release_branch = current_release.name + "/" + current_release.version
	next_release_branch = next_release.name + "/" + next_release.version

	if gitHelper_instance.branch_exists(current_release_branch) == False:
		current_release_branch_does_not_exist(gitHelper_instance, next_release_branch)
		return

	current_release_feature_flag_data = gitHelper_instance.pull_file(FEATURE_FLAG_PATH, current_release_branch)
	next_release_feature_flag_data = gitHelper_instance.pull_file(FEATURE_FLAG_PATH, next_release_branch)

	print("Generating diff of FF.csv...")

	current_release_FF_text = current_release_feature_flag_data.decode('utf-8').splitlines()
	next_release_FF_text = next_release_feature_flag_data.decode('utf-8').splitlines()
	current_release_file = "{current_release_branch} / {feature_flag_file_path}"
	next_release_file = "{next_release_branch} / {next_release_branch}"

	diff = difflib.context_diff(current_release_FF_text, next_release_FF_text, fromfile=current_release_file, tofile=next_release_file)
	write_dif_file(diff)

def current_release_branch_does_not_exist(gitHelper_instance, next_release_branch):
	next_release_feature_flag_data = gitHelper_instance.pull_file(FEATURE_FLAG_PATH, next_release_branch)
	next_release_FF_text = next_release_feature_flag_data.decode('utf-8').splitlines()
	write_dif_file(next_release_FF_text)

