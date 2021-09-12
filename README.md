# Access For All

This app was created by Debbie, Ivana, Jack, Slava and Istvan who took part in the Code Institute hackathon in September 2021.  The theme was to create an app for employers to use to increase inclusivity and accessibility for all employees.  Inclusivity and access to work is an important theme for employers to address; people with disabilities make up a very small portion of working employees despite having good skillsets.  Employers miss out on valuable skills that those with disablities have to offer as a result and people with disabilities report that they often find it very difficult to access the work place overall.

 In line with this theme we decided to create an app for an interviewer to use which gave them the facility to record their scores  and notes from a group of questions for each applicant and also helped them see how candidates were ranked.   Questions were designed to be inclusive so that all applicants were able to  Onboarding information would also be provided so that candidates queries about onboarding should they be successful at interview could be answered quickly.

## Contents
- [1. User experience design](#1-user-experience-design "1. UX design")
  - [1.1 Strategy Plane](#11-strategy-plane "1.1 Strategy Plane")
  - [1.2 Scope plane](#12-scope-plane "1.2 Scope plane")
  - [1.3 User Stories](#13-user-stories "1.3 User Stories")
  - [1.4 Structure plane](#14-structure-plane "1.4 Structure plane")
  - [1.5 Skeleton plane](#15-skeleton-plane "1.5 Skeleton plane")
  - [1.6 Surface plane](#16-surface-plane "1.6 Surface plane")
- [2. Code design](#2-code-design "2. Code design")
- [3. Features Left to Implement](#3-features-left-to-implement "3. Features Left to Implement")
- [4. Technologies and Tools Used](#4-technologies-and-tools-used "4. Technologies and Tools Used")
- [5. Issues](#5-issues "5. Solved and Known issues")
- [6. Testing](#6-testing "6. Testing")
- [7. Deployment](#7-deployment "7. Deployment")
- [8. Credits](#8-credits "8 Credits")

## 1. User Experience design
### 1.1 Strategy Plane
Stakeholders of the website:
Coders in the hackathon:  Istvan, Slava, Jack, Ivana and Debbie.
CI organisers and their guests from SODA.

#### 1.1.1 Goals and Objectives of Stakeholders (users)
|User|Goals, Needs, Objectives|
|----|------------------------|

### 1.2 Scope plane

### 1.3 User Stories
* As a user I want to be able to enter candidate scores and notes in interviews so I can compare candidates easily to see who is a good fit for the job advertised.
* As a user I want to be able to run the app on a desktop or mobile device.
* As a user I want to have onboarding information on another page on the app so that I can talk to candidates about the onboarding process during the time they have to ask questions about the company.
* As a user I want to have a report summarising all candidates scores produced from my input so that I can compare candidates easily to see who is a good fit for the job advertised.

### 1.4 Structure plane
* As a user I want to be able to enter candidate scores and notes in interviews.
Acceptance criteria:  Entry page for candidates should be clear and easy to use.
Implementation:  I want to go to the page on the app and enter my name as an interviewer, the candidates name and their scores and notes and save this information.


### 1.5 Skeleton plane


### 1.6 Surface plane

## 2. Code design
* utilizing the [Flask](https://flask.palletsprojects.com/) framework for handling REST API calls
  - The `run.py` file contains code related to Flask only, no database or form reference can appear in there.
  - The `db.py` file is a module and contains code related to the database.
* generating web pages from HTML templates with [Jinja](https://jinja.palletsprojects.com/) templating inserts
  - the `base.html` file contains the base HTML structure of all web pages generated in the app
  - the `index.html` extends the `base.html` into the Home page
 
## 3. Features Left to Implement

## 4. Technologies and Tools Used

## 5. Issues
### Issues solved during development
### Known issues

## 6. Testing

## 7. Deployment
 
### Deployment in development environment

#### 7.1 Python and Git
Make sure, that [Python](https://www.python.org/downloads/) and [Git](https://git-scm.com/downloads) are installed on your computer

#### 7.2 Clone the project's GitHub repository

1. Locate the repository here https://github.com/ruszkipista/access4all
2. Click the 'Code' dropdown above the file list
3. Copy the URL for the repository (https://github.com/ruszkipista/access4all.git)
4. Open a terminal on your computer
5. Change the current working directory to the one where the cloned folder will be located
6. Clone the repo onto your machine with the following terminal command
```
git clone https://github.com/ruszkipista/access4all.git
```

#### 7.3 Create local files for environment variables
Change working directory to the cloned folder and start your code editor
```
cd access4all
code .
```
Create file `envWS.py` with the following content into the root of the project folder
```
import os
os.environ.setdefault("FLASK_SECRET_KEY", "<secret key>")
os.environ.setdefault("FLASK_IP",         "127.0.0.1")
os.environ.setdefault("PORT",             "5500")
os.environ.setdefault("FLASK_DEBUG",      "True")
```
The `<secret key>` can be any random character string from your keyboard.
 
#### 7.4 Set up the Python environment
In your development environment, upgrade `pip` if needed
```
pip install --upgrade pip
```
Install `virtualenv`:
```
pip install virtualenv
```
Open a terminal in the project root directory and run:
```
virtualenv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```
#### 7.5 Start the web server:
```
python run.py
```

### Deployment on Heroku
[Heroku](https://www.heroku.com/) is a PaaS cloud service, you can deploy this project for free on it.

#### 7.6 Prerequisites:
- you forked or copied this project into your repository on GitHub.
- Heroku requires these files to deploy successfully, they are both in the root folder of the project:
- `requirements.txt`
- `Procfile`
- you already have a Heroku account, or you need to register one.

#### 7.7 Create a Heroku App
Follow these steps to deploy the app from GitHub to Heroku:
- In Heroku, Create New App, give it a platform-unique name, choose region, click on `Create App` button
- On the app/Deployment page select GitHub as Deployment method, underneath click on `Connect GitHub` button
- In the GitHub authorization popup window login into GitHub with your GitHub username and click on `Authorize Heroku` button
- Type in your repo name and click `search`. It lists your repos. Choose the one and click on `connect` next to it.
- either enable automatic deployment on every push to the chosen branch or stick to manual deployment
- go to app/Settings page, click on `Reveal Config Vars` and enter the following variables and their values from the `envWS.py` file:
  * FLASK_SECRET_KEY

## 8. Credits