install-deps:
    python3 -m pip install -r requirements.txt


format:
    python3 -m autopep8 ./ -r --in-place