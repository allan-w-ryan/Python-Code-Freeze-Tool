## This project will not run
This project was ment to run agains a very specifc repo and git setup. I've removed the git repo this was pointing to and any credentials/token associatd with that repo. I am providing this code simply as an additional code sample. Some details of the project have been been altered.

The point of this project was to automate a manual code freeze process a hypothetical company would go through prior to a relese. The idea was to peform the following:

- Update a `release.plist` file with release name/version for the next release. Releases were logged in a csv file.
- Performing the code freeze by cutting a new branch with from the base branch with name `release_name/release_version` e.g. `Some_Feature/1.3`. 
- Generating a Feature Flag report which is a diff between the current and the previous release of `FF.csv`

## Original README supplied to Assessors
### Prereqs
 1. Personal Access Token:
 	The scirpt will prompt the user to enter their Personal Access Token. The Personal Access Token is required for the script to access the GitHub repo. If you don't already have one available you can create one in GitHub through Settings > Developer Settings > Personal Access Tokens.
 2. Python 3 and PyGithub need to be installed.
 	Because the README in the GitProject specified that using the GitHub Api was encouraged I built the scipt using PyGithub (under the assumption that any machines running this will have PyGithub installed already). Since the script requires PyGithub to run you'll need to install it if you haven't already. It can be installed by running `pip3 install PyGithub requests` in the terminal. You also might need to install Python3. I was having some difficulty with PyGithub using the regular python command. I was unsure if it was an actual issue or an environemnt issue with my machine.

 NOTE:
 I experienced a bug when parsing the `release.plist` file using plistlib. The error was due to the `release.plist` file in master having an empty line at the top of the file. I removed the line and pushed the updated file my `dev` branch. For this reason the script currently only works when `dev` is used as the base branch, not master.

### Running the script
To run the script open a terminal window in the directory containing the CodeFreeze.py file. In the terminal window type: `python3 CodeFreeze.py`. The script will prompt you for your git access token (see the `Prereqs` section above for how to generate one). After entering the access token the script will pull the `release.plist` and `releng/release_info.csv` files. The pulled files will will be parsed for the required data, then the `release.plist` will be updated. After the plist file is updated it will be pushed to the new code freeze branch. Once all that is done, the Feature Flag report will be generated using the `FF.csv` files from the previous and new code freeze branches. The Feature Flag report is written `release-tools/diff/FF.csv.diff` (or rather a diff directory is created whereever you run `python3 CodeFreeze.py` from.)

### Unit Testing
Unfortunatly I was unable to get unit tests up for this assignment however, if give the opportunity I would add unit test for the following:
- Tests for pulling the plist/csv files
	- mocking file locations to test happy path
	- injecting bad file locations to verify correct error messages are thrown
	- verify error flow when specified branches are or aren't found
	- verify the script is able to start up the github library successfully
- Tests for parsing the plist/csv files
	- verifying that the files can be parsed correctly
	- proper errors appear when they aren't able to be parse
	- able to extract the required data from the plist and csv files
	- correct errors are thrown when the required data can't be extracted
- Tests verifying that the plist file is upated correctly before it gets pushed
- Tests verifing the Feature Floag report is generated correctly
	- verifying the diff is generated correclty files
	- verifying that if the current freeze branch is missing the 


### Potential Future Improvements
- Allow for more user inputs (or pulling inputs from a config file)
	- Right now the user is only able to enter their Personal Access Token, however the scipt would benefit greatly from allowing more user/custom input. Being able to specify branches or file location would allow the script to be more genric and useful in other repositories.
- Turning the script into an exe
- Project structure/Code Quality refactor
	- I feel like I kind of shot myself in the foot by choosing to write in python, a language I haven't used in about 7 years. I imagine a python veteran would have some great ideas on how to improve the project's strucure and quality.
- Better/more robust error handling
- Better messaging to the user
- Improved formatting for current output
- Debug logging
- Reading the personal access token from an environment/config location (not sure exactly where the best place to pull it from is, but having to copy it all the time isn't ideal)
- Having the script create a pull request for the new branch
