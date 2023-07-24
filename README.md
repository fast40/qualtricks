# qualtricks (README is currently a work in progress!!!)
qualtricks makes it easy to use large file datasets in Qualtrics surveys. Note: If you don't know me and want to use this, email me at eclfast@gmail.com and I may be able to help.
## How it works
This software runs a server that is not part of Qualtrics at all. Survey creators upload files, paste a small bit of HTML code into a survey, and the server will randomly select files to send over.


This application works by creating datasets and requests.

This software allows survey creators to paste an HTML tag into their survey which will be displayed to respondents


## Setup
### Create a file dataset
Upload a single zip file to the application. This zip file should contain only the files that you want survey participants to see. The folder structure does not matter. You also need to enter a name for this dataset which will be used in the survey to fetch files.
### Edit the Qualtrics survey
Once you have a dataset, you can set up a Qualtrics survey to use this application.

- Create a loop
- Create a question within the loop
- Switch to html editor
- Paste the following html into it, replacing <hostname> and <dataset> with the correct values.
## Usage
Each dataset keeps track of how many views each file has recieved as well as the Qualtrics response id of the respondents