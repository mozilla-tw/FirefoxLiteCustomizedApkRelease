# Firefox Lite Customized Apk Release Handy Tool
 This script connects [Bitrise](https://app.bitrise.io/app/2bee753c3b6709ca) to trigger customized builds for different stores (e.g.Samsung, Xiaomi...). The generated builds will be automaically uplaoded to [Google Drive : FxLite Releases](https://drive.google.com/drive/u/0/folders/1KP5LzrwVm9jcdcxlcnjKnu-jDjYzaNSR) so that each store's distribution owner can start release. 

## Purpose  
 Since Firefox Lite has a high demand to distribute our product to 5+ stores, each store with a customized Adjust tracker, the release team needs to generate those builds and uploaded on Drive so that the distribution owners can start release.

## Paint Point 
 Originally it a requires a set of manual processes 1) trigger Bitrise to get customized build for all [distribution channels](https://docs.google.com/document/d/15w7ZNYtJkpcPDkh6cfLtVl3O86IiIWljqfFxT_PPv8c/edit), 2) Wait until all build generated 2) download each customized apk from Bitrise, 3)rename those apks locally 4) upload to Google Drive. By using the script, it can reduce repetitive work, prevent human error and human interference, then ultimately contribute to productivity.

## Prerequisition
1. export BITRISE_TOKEN as enviromnent variable. To get BITRISE_TOKEN refer [Bitrise acquiring a Personal Access Token ](https://devcenter.bitrise.io/jp/api/authentication/)
2. export BITRISE_TRIGGER_TOKEN as enviromnent variable. To get BITRISE_TRIGGER_TOKEN, please go to [Fx-Lite Bitrise](https://app.bitrise.io/app/2bee753c3b6709ca) > [Start a Build] > [Advanced]
3. Download client_secrets.json from [Google Cloud Platform Credentials](https://console.cloud.google.com/apis/credentials?project=rocketnightly) ,refer [pyDrive](https://github.com/gsuitedevs/PyDrive)


## Installation

Use the package manager [pip3](https://pip.pypa.io/en/stable/) to install libraries.

```bash
pip3 install -r requirements.txt
```

## Usage

Please check a release tag exists in [Firefox Lite Release Tags](https://github.com/mozilla-tw/FirefoxLite/tags) before using the following commands:

```bash
python3 customizedApkRelease.py --action=trigger --tag=[v2.1.11]
```
When it asks for Google Drive access permission, please choose your Mozilla Account to upload.
## Authors

* **[Daisy Liu](https://github.com/Daisy-pliu)** 
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

