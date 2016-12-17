This repository contains files to automatically download information from TheNeedleDrop's YouTube channel about recent album reviews, as well as update an ongoing Google Doc spreadsheet containing all previous reviews.

In order for this repository to function, you'll need to use Google OAuth 2.0 to make a developer account, then download the json key file, place it in the repository folder, and name it googleoauth.json.

There are multiple .py files in the repository that represent previous methods of accomplishing the task. They're still useful to look at the basic components of the procedure (download, sort, organize), and the txt files are useful examples of how the outputs of the scripts look.

The only script you actually need to run to accomplish the entire task of finding, organizing, and uploading new NeedleDrop review scores is fantanoauto.py, since it contains all of the required steps with no user input.
