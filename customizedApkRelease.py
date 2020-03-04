import requests
import io ,os ,time


RELEASE_TAG = "v2.1.10"
PROJECT_NAME = "Firefox Lite"

TARGET_ARTIFACT_TITLE = "app-focus-webkit-release-signed-aligned.apk"

BUILD_TRIGGER_TOKEN = os.getenv('BUILD_TRIGGER_TOKEN') 
BITRISE_TOKEN = os.getenv('BITRISE_TOKEN')
BITRISE_HOSTNAME = "https://api.bitrise.io/"
GET_APPS_URL = BITRISE_HOSTNAME + "v0.1/apps"

headers = {
    'Authorization': BITRISE_TOKEN
    }


CHANNEL_DIC={   "MozNext2GooglePlay" : "t5cdv3e",
                # "MozNext2APKDownload" : "qd2shkv,
                # "Github" : "8wvdqfc",
                # "SamsungStore" : "bc7t7hv",
                # "XiaomiStore" : "2bzwbyc" 
                }

FXLITE_RELEASES_FID = "1KP5LzrwVm9jcdcxlcnjKnu-jDjYzaNSR"

def build_customized_apk(): 
    """Trigger Bitrise to build customized apk
    Returns:
        dic: biuld_slugs. The returned dictionary contains build info.
    """

    START_BUILD_URL = "https://app.bitrise.io/app/{}/build/start.json".format(FXLITE_APP_SLUG)
    
    build_slugs={}

    for channel, tracker in CHANNEL_DIC.items():
        json = {"hook_info":
            {"type":"bitrise",
            "build_trigger_token":BUILD_TRIGGER_TOKEN
            },
                "build_params":{
                    "commit_message": channel + "_" + RELEASE_TAG + ".apk",
                    "workflow_id":"release_sideload_tracking","tag":RELEASE_TAG,
                    "environments":
                        [
                            {"mapped_to":"ADJUST_SIDELOAD_TRACKER","value": tracker ,"is_expand":True}
                            ]
                            },
                            "triggered_by":"Customized Apk Python Script"
                    }


        resp = requests.post(START_BUILD_URL, json=json)
        print("customized_apk_resp.status_code", resp.status_code)

        if resp.status_code == 200 or 201 :
            build_slugs[ channel ] = { "build_slug" : resp.json()['build_slug'], "build_no" : resp.json()['build_number'] }
            print('build is triggered, you can go to Bitrise to check and wait it finished.')
            return build_slugs
        else :
            print('Unable to tigger build')
            print(resp.text)

def get_app_slug():
    """Get project's app_slug
    """

    global FXLITE_APP_SLUG

    resp = requests.get(GET_APPS_URL, headers=headers)
    if  resp.status_code == 200:
        all_apps=resp.json()['data']
        for app in all_apps:
            if app['title'] == PROJECT_NAME:
                FXLITE_APP_SLUG = app['slug']
                print('Retrieved app slug {} for {}'.format(FXLITE_APP_SLUG,PROJECT_NAME))
    else:
        print('Unable to get app slug')
        print(resp.text)
        
def get_signed_apk_artifact_slug(build_slug):
    """Get artifact_slug of signed apk
    Args:
        str : build_slug. A build_slug for a generated Bitrise build
    Returns:
        str : artifact_slug. A artifact_slug of the signed apk
    """

    GET_ARTIFACTS_URL = BITRISE_HOSTNAME + "v0.1/apps/" + FXLITE_APP_SLUG + "/builds/" + build_slug + "/artifacts"

    resp = requests.get(GET_ARTIFACTS_URL, headers=headers)
    if resp.status_code == 200 or 201:
        all_artifacts = resp.json()['data']
        for artifact in all_artifacts:
            if artifact['title'] == TARGET_ARTIFACT_TITLE:
                artifact_slug = artifact['slug']
                print('Retrieved artifact slug {} '.format(artifact_slug))
                return  artifact_slug
    else:
        print('Unable to get artifact slug')
        print(resp.text)

def get_download_url(build_slug , artifact_slug):
    """Get customized APK Download link
    Args:
        str : build_slug. A build_slug for a generated Bitrise build
        str : artifact_slug. A build_slug for a generated Bitrise build
    Returns:
        str : downnload_url. It is used to download apk. 
    """
    GET_ARTIFACT_URL = BITRISE_HOSTNAME + "v0.1/apps/" + FXLITE_APP_SLUG + "/builds/" + build_slug + "/artifacts/" + artifact_slug
    
    resp = requests.get(GET_ARTIFACT_URL, headers=headers)
    if resp.status_code == 200:
        downnload_url = resp.json()['data']['expiring_download_url']
        print('Retrieved download url: {} '.format(downnload_url))
        return  downnload_url
    else:
        print('Unable to get donwnload url')
        print(resp.text)


def download_customized_apk( channel , build_no , download_url):
    """Download customized apk
    Args:
        str : channel. It is the channel name 
        int : build_no. It is the build_no for the channel  
        str : download_url. It is the download_url for the channel  
    Returns:
        file : apkfileName. An APK file.
    """
    resp = requests.get(download_url, allow_redirects= True )
    if resp.status_code == 200:
        apk_file_name = '{}_{}_({}).apk'.format( channel ,RELEASE_TAG , build_no)
        open(apk_file_name, 'wb').write(resp.content)
        print('Retrieved customized apk file has been written to {}'.format(apk_file_name))
        return apk_file_name
    else:
        print('Unable to download customized apk')
        print(resp.text)

def upload_to_drive(apk_file_name):
    from pydrive.auth import GoogleAuth
    from pydrive.drive import GoogleDrive

    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    apk_file = drive.CreateFile(
        {"mimeType": "application/vnd.android.package-archive",
        "parents": [ {"kind": "drive#fileLink", "id": FXLITE_RELEASES_FID} ] } )
    apk_file.SetContentFile( apk_file_name )
    apk_file.Upload()
    print('Created file {} with mimeType {}'.format(apk_file['title'], apk_file['mimeType']))  


def main():
    get_app_slug()
    build_slugs = build_customized_apk()
    print('Show channel\'s build_slug information {}'.format(build_slugs))

    """
    Need to wait around 15 min to get generated build artifact . The hard code waiting time will improve in the future.
    """
    time.sleep(15 * 60)
    
    """
    itertate each channel build-slug info to download apks
    """
    for channel, slug_info in build_slugs.items():
        build_slug , build_no = slug_info["build_slug"], slug_info["build_no"]
        artifact_slug = get_signed_apk_artifact_slug( build_slug)
        download_url = get_download_url( build_slug, artifact_slug)
        apkfileName = download_customized_apk( channel, build_no, download_url)
        upload_to_drive(apkfileName)

if __name__ == '__main__':
    main()
    
    """
    Testcase_1: 
        global FXLITE_APP_SLUG 
        FXLITE_APP_SLUG = "2bee753c3b6709ca"
        build_slugs = {'MozNext2GooglePlay': {'build_slug': '1b41a8e4312baf2c', 'build_no': 18844}}
    """
