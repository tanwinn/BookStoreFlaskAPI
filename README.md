# Book Store API
Powered by Python3 and Flask

## Run the application
### Dependencies
```sh
# Either use pipenv
pipenv lock  # Generating pipfile.lock
pipenv sync

# Or pip & venv of your choice
pip install -r requirements.txt
```

### Run the Flask app
More options at [Flask Official Docs](https://flask.palletsprojects.com/en/1.1.x/quickstart/)

Add config to `.env` at root project
```
FLASK_APP=src/app.py
```
then 
```sh
python -m run flask  # Windows
python3 -m run flask  # Linux
```


## Deveploment
### Setup

```sh
git clone git@github.com:tanwinn/BookStoreFlaskAPI.git
cd BookStoreFlaskAPI
```

Either using __pipenv__:
```sh
pipenv sync --dev  # install dependencies with dev packages
pipenv shell  # activate the venv
# do dev stuff
exit # Exit the venv
```

Or __pip__ & your choice of venv tool:
```sh
pip install -r requirements-dev.txt
```


### Testing
```sh
pytest
```
