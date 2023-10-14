# Jotter Notes

## get started

1. Create a python virtual env named IAVenv so that it matches the .gitignore file.

    - `python -m venv IAVenv`

2. Install the dependencies.

    - `pip install -r requirements.txt`


## two ways to start the app

1. in vscode everything should be ready to run the app by starting the debugger by selecting the "Start Jotter" option in 'run and debug'.

    - You can change the values in the list of the `"args"` key in `.vscode/launch.json` to try out all of the apps functions.

    - Of course you can use this for debugging as well.

2. type in the terminal `python -m jotter <COMMANDS>`