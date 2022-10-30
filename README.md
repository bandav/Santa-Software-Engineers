# Santa-Software-Engineers
## 348 Group Project
Link to project drive: https://drive.google.com/drive/folders/1BzgpXEAnBL_EVPqr-ravAbfB80vOINdp
## Running this Project
1. Create a fresh directory on your local system for Santa's Software Engineers.
2. Clone this repository
3. Step into the 348-Project directory (this is the local copy we worked on for Stage 2)
4. Create a virtual environment: 

    python3 -m venv venv

5. Activate your virtual environment:
    
    cd venv
    
    source bin/activate
    
    cd ..
4. Step through each of files, and pip install the dependencies onto your venv.
5. If you're on Mac, run:

    export FLASK_APP="\_\_init\_\_.py"
    
    export FLASK_ENV="development"
    
    If that doesn't work, try export FLASK_APP="app.py" instead.
6. If you're on Windows, ~get a mac~ search up the equivalent for export.
7. Make sure you're still in the 348Project directory. Run "flask run".
8. Open the localhost URL, and you're all set :)
