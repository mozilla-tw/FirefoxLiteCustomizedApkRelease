# Firefox Lite Customized Apk Release Handy Tool

 This script can be used to trigger [Bitrise](https://app.bitrise.io/app/2bee753c3b6709ca) to get customized build and then uplaod to [Google Drive : FxLite Releases](https://drive.google.com/drive/u/0/folders/1KP5LzrwVm9jcdcxlcnjKnu-jDjYzaNSR)

## Purpose
 To eliminate the toils of triggering Bitrise customized build manually for all [distribution channels](https://docs.google.com/document/d/15w7ZNYtJkpcPDkh6cfLtVl3O86IiIWljqfFxT_PPv8c/edit), download apks, rename apks and then upload to Google Drive. By using the script, it can reduce repetitive work, prevent human error and human interference, then ultimately boost team's productivity.

## Prerequisition
1. export BITRISE_TOKEN as enviromnent variable. To get BITRISE_TOKEN refer [Bitrise acquiring a Personal Access Token ](https://devcenter.bitrise.io/jp/api/authentication/)
2. export BITRISE_TRIGGER_TOKEN as enviromnent variable. To get BITRISE_TRIGGER_TOKEN, please go to [Fx-Lite Bitrise](https://app.bitrise.io/app/2bee753c3b6709ca) > [Start a Build] > [Advanced]
3. Download client_secrets.json from [Google Cloud Platform Credentials](https://console.cloud.google.com/apis/credentials?project=rocketnightly) ,refer [pyDrive](https://github.com/gsuitedevs/PyDrive)


## Installation

Use the package manager [pip3](https://pip.pypa.io/en/stable/) to install libraries.

```bash
pip3 install requirements.txt
```

## Usage
 
Please use the following commands:

```bash
python3 customizedApkRelease.py 

```
## Authors

* **[Daisy Liu](https://github.com/Daisy-pliu)** 
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

