#
# gitHelper.py
#
# Created by Allan Ryan 3/01/22
#

import github
import requests
import releaseInfo

class GitHelper:

	__REPO_NAME = "REMOVED-FOR-PRIVACY"
	__DEFAULT_BRANCH= "dev"

	def __init__(self, token):
		github_instance = github.Github(token)
		try:
			self.repo = github_instance.get_repo(self.__REPO_NAME)
		except:
			print("==== ERROR: Invalid Git credentials. Run the script again with a valid auth token.")
			print("==== Halting execution")
			exit(1)


	def pull_file(self, file_path, branch = __DEFAULT_BRANCH):
		print("Pulling", file_path, "from", branch, "...")
		try:
			file = self.repo.get_contents(file_path, ref=branch)
			return file.decoded_content
		except:
			print("==== ERROR: Unable to pull the specifed file:", file_path)
			print("==== Halting execution")
			exit(1)

	def branch_exists(self, branch):
		try:
			self.repo.get_branch(branch)
		except:
			return False

		return True

	def push(self, content, releaseInfo, path, base_branch = __DEFAULT_BRANCH):
		new_release_branch = releaseInfo.name + "/" + releaseInfo.version
		print("Creating new code freeze branch: " + new_release_branch + "...")
		source = self.repo.get_branch(base_branch)

		try:
			self.repo.create_git_ref(ref=f"refs/heads/{new_release_branch}", sha=source.commit.sha)
		except github.GithubException as error:
			if error.status == 422:
				print("==== ERROR: Branch", new_release_branch, "already exists.")
				print("==== Halting execution")
				exit(1)

		contents = self.repo.get_contents(path, ref=new_release_branch)
		message = "Code Freze for release", new_release_branch
		self.repo.update_file(contents.path, "Code Freze for release", content, contents.sha, new_release_branch)
