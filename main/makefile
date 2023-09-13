all: create_env setup download_driver install_driver

PHONY: create_env

DRIVER_URL_LINUX = "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/116.0.5845.96/linux64/chromedriver-linux64.zip"
DRIVER_NAME = "chromedriver.zip"
VENV := .venv

create_env:
	@echo "Creating virtual environment at $(PWD)/$(VENV)"
	@python3 -m venv $(VENV)
	@echo "Virtual environment created."


setup: $(VENV)/bin/activate

$(VENV)/bin/activate:
	test -d $(VENV) || virtualenv $(VENV)
	$(VENV)/bin/pip -U pip
	$(VENV)/bin/pip install -r requirements.txt

download_driver:
	@echo "Downloading driver ..."
	@curl -o $(DRIVER_NAME) $(DRIVER_URL_LINUX)
	@echo "Driver downloaded."
	@echo "Unzipping driver ..."
	@unzip $(DRIVER_NAME)

install_driver:
	@echo "Installing driver ..."
	mv ./chromedriver-linux64/chromedriver ./.venv/bin/
	@echo "Driver installed."