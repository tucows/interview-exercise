# interview-exercise c# project
Tucows Interview Exercise


## Intro

- This project is developed using .net 5 on visual studio 2019 editor.
- The TucowsInterviewExerciseApp solution contains two projects; the console app (TucowsInterviewExerciseApp), and the web app (TucowsInterviewExerciseWebApp).

## Running and Testing the project (2 Ways)

### 1- Using visual studio
- Open the TucowsInterviewExerciseApp solution using visual studio 2019 editor after clonning or downloaing it.

#### The console app
- Set The console app (TucowsInterviewExerciseApp) as the startup project (right click the project from the solution explorer then choose Set as Startup Project Option).
- Run the project by clicking f5 or the green play icon in the tools bar.
- The command line app will start by showing a random quote and openning a random picture on the photos viewer app (the program will save the picture in the project directory then will open it using the viewer app).
- For different results enter your choice following the menu directions.

#### The web app
- Set the web app (TucowsInterviewExerciseWebApp) as the startup project (right click the project from the solution explorer then choose Set as Startup Project Option).
- Run the project by clicking f5 or the green play icon in the tools bar.
- The web page will start by showing a random quote and a random picture.
- For differnt results use the (Get a qoute) button in the bottom. 
- There are options for grayscale image and specific quote key.

### 2- Without using visual studio
- Download the project folder.
- Download and install the Hosting Bundle under ASP.NET Core Runtime 5.0.17 from this link https://dotnet.microsoft.com/en-us/download/dotnet/5.0

#### The console app
- Open the project folder (TucowsInterviewExerciseApp).
- Then open TucowsInterviewExerciseApp -> bin -> Release -> net5.0
- Run the TucowsInterviewExerciseApp.exe
- The command line app will start by showing a random quote and openning a random picture on the photos viewer app (the program will save the picture in the project directory then will open it using the viewer app).
- For different results enter your choice following the menu directions.

#### The web app
- Open the project folder (TucowsInterviewExerciseApp).
- Then open TucowsInterviewExerciseWebApp -> bin -> Release -> net5.0
- Run the TucowsInterviewExerciseWebApp.exe it will open a cmd window.
- Copy the link (beside Now listening on) for example http://localhost:5000 and open it in the browser.
- The web page will start by showing a random quote and a random picture. (it will be basic page without CSS style)
- For differnt results use the (Get a qoute) button in the bottom. 
- There are options for grayscale image and specific quote key.

