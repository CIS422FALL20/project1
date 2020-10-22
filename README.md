####**Overview**
This project is a simple Web App that takes gpx data as an input and returns a list of directions,
otherise known as a cue sheet, based on that data. The data typically comes from a road biker, however
it is compatible with any street, so the data will work if a hiker, car or pedestrian of any kind sticks
to the main roads.

This project is compatible with any machine that is running Docker version 19.03.8 (the most recent version), and docker-compose version 1.25.0.
If you install Docker Desktop on Windows or MacOS, docker-compose is included as a package.

This project has not been tested on other docker versions, as we recommend updating docker to its most recent version.

Our only dependency is that your machine can install and run docker on any of the following operating systems:



####**Getting Started:**

###**For Installing Docker, if requirement is not already satisfied:**

##For macOS version 10.14 or newer:
You can download docker with the following command:
$ brew cask install docker

or you can follow the instructions at https://docs.docker.com/docker-for-mac/install/

##For Linux
Depending on your Linux Distribution, you can follow the instructions at the follow locations:

**CentOS:** https://docs.docker.com/engine/install/centos/
**Debian:** https://docs.docker.com/engine/install/debian/
**Fedora:** https://docs.docker.com/engine/install/fedora/
**Raspbian:** https://docs.docker.com/engine/install/debian/
**Ubuntu:** https://docs.docker.com/engine/install/ubuntu/

##For Windows 10:
https://docs.docker.com/docker-for-windows/install/

**You can test if docker installed by running

$ docker -v

If this returns a version of docker, you have correctly installed docker** 

###**After Docker is installed:**

#Clone the project from our GitHub Repository:

$ git clone https://github.com/CIS422FALL20/project1

#Build the Project
You can do this with our run.sh file after setting its permissions, by running the following commands in the command line

$ chmod 777 run.sh
$ cd project1
$ ./run.sh

The run.sh file contains the following command

$ docker-compose up --build

This will run the webserver, which you can view in localhost:5000 in a browser


####**Using The Application:**

###**If you are an end user:**
1. Run the server with the ./run.sh file
2. Once the server is running, open a browser and navigate to <servername>:5000
	- Most likely this is localhost:5000, but also could be testium.cs.uoregon.edu:5000
3. Input your chosen gpx file
4. Wait for the program to compute the directions based on the gpx file chosen
**(!-- MAYBE: --!)** 5. You will recieve a text from us with your directions!

If you are looking to develop/maintain our project, look at the architecture of our project for more information

###**Architecture:**
The only file that exists outside of the **src** directory is our docker-compose.yml, which is the top-level of our
project. This file is responsible for running and hosting the server on a specific port (5000), and running the 
Dockerfile, which takes care of dependencies, requirements and runs the flask server through app.py.

All of our source files otherwise, exist within the **src** directory of the project. The main file that does the backend work
is the flask python file named **app.py**. app.py imports functions from the other python files, and runs them within the flask 
functions so it can eventually serve the output to the user in the browser. These other files include **( !--- include files 
and functionality here ---! )**. **app.py** also serves the html files in the sub-directory **templates**.

We have seperated the flask file and the files that calculate the turns for ease of building something from the independent parts.
Our turn calculation files are already completely independent, and simply take any arbitrary gpx file to work. **app.py** and its subsequent
html templates act as a good starting point for a project that needs to take file input from the user. Simply replacing the currently 
imported functions with other developed functions can seamlessly create a project with an entirely new functionality. This seperation 
of files makes it easy for further development, as shown here.

###**Module Interface**
The interface for the web app is extremely simple.
The opening page mirrors this overall simplicity. There is only one place to input a file, and once you have selected your prefered gpx
file, simply hit submit. The file will then be processed while a loading icon is shown, and your directions will eventually pop up.

   




















# -- End
