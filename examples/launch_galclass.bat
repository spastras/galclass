% Set the PYTHONPATH environment variable %
set PYTHONPATH="C:\Programme\galclass"

% Activate anaconda %
call "C:\Programme\anaconda3\Scripts\activate.bat" "C:\Programme\anaconda3"

% Activate the galclass environment %
call conda activate galclass_env

% Launch galclass %
python -m galclass --graphical-only

% Prevent the terminal from exiting %
pause