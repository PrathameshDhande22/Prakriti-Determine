@echo off

REM Activate the Python virtual environment
call project\Scripts\activate

REM Run botmodel.py
python Training\botmodel.py

REM Run prakritimodel.py
python Training\prakritimodel.py

REM Run app.py
python app.py

REM Deactivate the virtual environment
deactivate

REM Pause to keep the console window open
pause
