# 835-final-project
Shuli Jones and Emily Caragay's 6.835 final project: Picture Hanging Helper

## Instructions for running

This app requires that the user's computer has any version of python 3, the Google Chrome browser, and npm. To run the app, clone or otherwise download the code. On a command line instance, navigate to the code's folder (`835-final-project`) and run `npm install`. Open a second command line instance. On one, go to the frontend folder and run `npm run serve`. On the other, go to the backend folder and run `python app.py`. (Note: if your computer has both python 3 and 2 installed, you may need to run `python3 app.py`.) To see the app, open Google Chrome and go to the localhost port that the frontend is running, which should be `http://localhost:8080/`. (Note: the code expects the frontend to be running on port 8080 and the backend to be running on port 5000. If this is not the case by default on your comptuer, you may need to alter the run commands to ensure that this is the case.)

## List of files

* backend/app.py: This file contains the entire backend, to which the frontend makes requests. It does all of the OpenCV image processing for rectangle identification and color tracking, as well as the math for nail placement, and sends the final images or placement information to the frontend upon request.
* frontend/confetti.js: This is not original code. It's copied from https://www.cssscript.com/confetti-falling-animation/ and used under the MIT creative license. It creates confetti on the screen when called.
* frontend/index.html: This file contains the entire frontend, including everything the user sees. It has all the instructions, the code to display video and images to the users, and the code to send requests to the backend based on which step or button the user clicks.
* All the other files in the frontend folder are boilerplate that are used to run the server. Some are auto-generated; most are written by us, but identical to many other files available on the Internet which run Flask/Express/Vue servers.
* color_tracking.py and frame_finder.py: These are test files used to try out improvements to the color tracking and rectangle identification. The final versions of the code here are in frontend/index.html. 
