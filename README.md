# TextSplitter

THIS CODE IS IN ACTIVE DEVELOPMENT!  The user ID is super not-stable and is being fixed! Feel feel to fork, but do so at your own peril.  I hope to get a more user friendly version of the code up by March 2013.  Rem.

TextSplitter is a WebApp written in python, html, and javascript that allows humans to select regions of non-ocr-ed scanned text.  These selections are then stored in an online database and the results can then be used to split the documents into coherent pieces that are easily OCRed and so amenable for statistical analysis.

The web app uses Google App Engine to host the "brains" of the app and Amazon Web Services to host the images that will be selected over.

The app follows standard GAE conventions using the jinja template engine.  The app uses the canvas element and so requires HTML5.  It has been tested in Chrome, workes in Safari/Firefox, and I have no idea about IE.

## Brief file descriptions:
- *app.yaml* controls GAE settings
- *bulkloader.yaml* sets preferences for downloading the GAE database, use the bash command:
	appcfg.py download_data --config_file=bulkloader.yaml --filename=selections.csv --kind=Selection --url=http://textsplitter.appspot.com/_ah/remote_api --application=s~textsplitter
- *image_list.py* contains a list of images used to keep track of what documents have been coded and the AWS url
- *javascript/turk_split_text.js* tells the webpage how to draw the selection rectangle
- *templates/split_text.html* contains the HTML layout template for the app
- *templates/turk_split_text.html* contains a reference HTML layout template for the app if you wanted to convert it to work with mechanical turk.  Not live, not tested.
- *textsplitter.py* contains the backend code for the app keeping track of users, submissions, and what documents have been coded.

