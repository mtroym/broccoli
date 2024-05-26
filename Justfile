install-deps: # install dependencies
    python3 -m pip install -r requirements.txt


format: # autopep8 reformat code.
    python3 -m autopep8 ./ -r --in-place


run-main: # run entrypoints.
    python3 main.py