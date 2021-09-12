# Access For All

This app was created by Slava, Istvan, Ivana, Jack, and Debbie who took part in the Code Institute hackathon in September 2021.  The theme was to create an app for employers to use to increase inclusivity and accessibility for all employees.  Inclusivity and access to work is an important theme for employers to address; people with disabilities make up a very small portion of working employees despite having good skillsets.  Employers miss out on valuable skills that those with disablities have to offer as a result and people with disabilities report that they often find it very difficult to access the work place overall.

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
As a team we met online to discuss how we would design an app that promoted inclusivity in the workplace.  We decided to look at the interviewing and onboarding process with a view to promoting inclusivity within that.  Once the idea was agreed on, balsamiq wireframes were produced.  

### 1.1 Strategy Plane
Stakeholders of the website:
Employers and HR reps of each user organisation.

#### 1.1.1 Goals and Objectives of Stakeholders (users)
|User               |           Goals, Needs, Objectives                 |
|-------------------|----------------------------------------------------|
|Employers          |Goal for an employer is to be able to access        |
|                   |potential candidates for a role using a numerical   |
|                   |system and additional notes so that the interview   |
|                   |process is deemed to be fair to all.  All candidates|
|                   |should be asked the same questions and should be    |
|                   |allowed to answer questions fully in their own time.|
|-------------------|----------------------------------------------------|
|                   |                                                    |
|HR personnel       |To keep a record of interviewee responses and       |
|                   |interviewer notes to ensure that the inteview       |
|                   |was fair to all candidates.                         |
|-------------------|----------------------------------------------------|


### 1.2 Scope plane
- Responsive design is essential so that the app works on desktop and mobile devices.
- User should be able to navigate with ease to each part of the app.
- The logo should take the user back to the home page when clicked on.  There should not be any need for the user to press the back button in order to get to any page of the app.
- Information on the onboarding page and the home page should give the user useful information about onboarding and the app itself.
- Colour schemes on the site should be designed so as to encourage inclusive access to the site for people with visual and neurological disabilites as well as for non disabled people.

### 1.3 User Stories
* As a user I want to be able to enter candidate scores and notes in interviews so I can compare candidates easily to see who is a good fit for the job advertised.
* As a user I want to be able to run the app on a desktop or mobile device.
* As a user I want to have onboarding information on another page on the app so that I can talk to candidates about the onboarding process during the time they have to ask questions about the company.
* As a user I want to have a report summarising all candidates scores produced from my input so that I can compare candidates easily to see who is a good fit for the job advertised.

### 1.4 Structure plane
* As a user I want to be able to enter candidate scores and notes in interviews.
Acceptance criteria:  Entry page for candidates should be clear and easy to use.
Implementation:  I want to go to the page on the app and enter my name as an interviewer, the candidates name and their scores and notes and save this information.

* As a user I want to be able to run the app on a desktop or mobile device.
Acceptance criteria: App should be responsive on desktop and mobile devices.  Team to test this using developer tools.
Implementation: I want the app to display well on all types of devices so that it is easy to interact with it.

* As a user I want to have onboarding information on another page on the app so that I can talk to candidates about the onboarding process during the time they have to ask questions about the company.
Acceptance criteria: Onboarding information should be available to interviewer and make sense.  Page is responsive.
Implementation:  Interviewer clicks on onboarding link to go to page and it displays correctly.

* As a user I want to have a report summarising all candidates scores produced from my input so that I can compare candidates easily to see who is a good fit for the job advertised.
Acceptance criteria: After last candidate has been entered and finished button clicked, report is generated.  Page is responsive.
Implementation: I want the app to display a list of all candidates scores after finish button is submitted.

### 1.5 Skeleton plane
Balsamiq was used to produce wireframes for the app.  Ivana produced these for desktop and mobile applications.   The skeleton of the site was designed to optimise the user experience and make it simple and sleek to use as well as for maximum effect and efficiency.  This was done by careful choice of colour schemes and contrast where needed.

### 1.6 Surface plane
The surface plane consists of elements on the screen.  We decided to use plain text images styled for full inclusivity so that the site was easy to use.  We used a transparent image on the home page with no text overlay so that visual clarity was not impaired.  However a call to action button for the onboarding page was coloured in a contrasting colour - orange - so that it was easily distinguished from the background image on the home page.

## 2. Code design
* utilizing the [Flask](https://flask.palletsprojects.com/) framework for handling REST API calls
  - The `run.py` file contains code related to Flask only, no database or form reference can appear in there.
  - The `db.py` file is a module and contains code related to the database.
* generating web pages from HTML templates with [Jinja](https://jinja.palletsprojects.com/) templating inserts
  - the `base.html` file contains the base HTML structure of all web pages generated in the app
  - the `index.html` extends the `base.html` into the Home page
 
## 3. Features Left to Implement
As the hackathon had a time limit we did not have time to implement the following functionality but in future we could review the app and add the following:
- Use a database to hold interviewers and interviewees details.  This would mean more analysis of the data could be done and the data would persist.
- Build facebook and twitter pages so that the links at the bottom of the page take the user to these for more information on accessible_five and other products they offer to encourage inclusivity in the workplace.


## 4. Technologies and Tools Used
[Flask](https://flask.palletsprojects.com/en/2.0.x/) is a microframework used to build apps.
[Jinja](https://jinja.palletsprojects.com/) is a templating language within flask.
[python](https://www.python.org/)is a programming language widely used on the internet with web frameworks to create apps.
[html](https://devdocs.io/html/)stands for HyperText MarkUp Language and is used to put content and structure on a web page.
[CSS](https://devdocs.io/css/) stands for cascading style sheets and is used to style a webpage.


## 5. Issues
### Issues solved during development
- As a team we had some issues with working with github collaboratively.  These issues were resolved through user team members experience and [github docs](https://docs.github.com/en).
- Issues with pages displaying were resolved using team review and some pair programming when needed.
- Issues with logic and the backend appeared when trying to connect up the json file holding interview questions, interviewer and interviewee details with the questions page.  These were resolved during team discussions and some pair coding.

### Known issues

## 6. Testing
Testing was done by all members of the team.  Automated testing was not done but this is a future area for development.

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
Favicon:

[The favicon for this page was sourced from the this site.](https://www.accessforalluk.com/wp-content/uploads/2017/09/Access-for-all-uk-logo-16px.png)


Onboarding page:

[On boarding blog](https://www.lever.co/blog/a-step-by-step-guide-to-cultivating-diversity-and-inclusion-part-8-after-the-hire/).  This is a step by step blog for creating diversity and inclusion in the workplace. 


[Importance of inclusivity with onboarding](https://medium.com/sarah-cordivano/understanding-and-designing-an-inclusive-onboarding-experience-4be6b5f7c669).   This medium article written by Sarah Cordivano discusses the importance of the onboarding process for all new employees.

[Why it is important to have a level playing field of success for all employees](https://hiringsuccess.com/leveling-the-playing-field-with-an-inclusive-onboarding-process/) 


[Four phases of onboarding](https://www.zoho.com/people/hrknowledgehive/What-are-the-four-phases-of-onboarding.html).  This article takes a 4 phase approach to onboarding.

[How to deliver successful onboarding](https://wavelength.asana.com/inclusive-onboarding-experience/).  This article by Sonja Gittens-Oakley argues that greater diversity in the workplace leads to better creativity and innovation.