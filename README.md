# qualtricks
qualtricks makes it easy to use large file datasets in Qualtrics surveys. Note: If you don't know me and want to use this, email me at eclfast@gmail.com and I may be able to help.
## How it works
This software allows survey creators to upload files to a server and use them in Qualtrics surveys by pasting a small bit of code into the survey. It keeps track of who has viewed which files in a json file which can be downloaded after the survey is complete.
## Setup
### Create a file dataset
Upload a single zip file to the application. This zip file should contain only the files that you want survey participants to see. The folder structure does not matter. You also need to enter a name for this dataset which will be used in the survey to fetch files.
### Edit the Qualtrics survey
Once you have a dataset, you can set up a Qualtrics survey to use this application by completing the following steps:
- Create a question block
- Turn on "Loop & Merge" with that question block selected.
- Make as many rows in the "Loop & Merge" table as you want by clicking in a cell. Make the table only one column. This will set the number of times that the loop runs for.
- Paste the HTML code found on the server into a text/graphic question, replacing <your_dataset_name> with the correct dataset name.
  
**Important:** Each survey should only have one question block looping and fetching files. If there are multiple, the server will send the SAME EXACT FILES for loop iteration #1, #2, etc. for both loops.
## Usage
Each dataset keeps track of how many views each file has recieved as well as the Qualtrics response id of the respondents. To reset this data for a datset, click the reset button. This is often done right before making a survey go live. Be careful with this, as it DELETES all view data. You may want to download a copy of the results before you reset if you're not sure. You can also delete a dataset by clicking the delete button.
