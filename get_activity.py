import subprocess


def get_foreground_activity():
    output = subprocess.check_output('adb shell dumpsys activity activities | findstr mResumedActivity', shell=True)
    if output:
        activity_info = output.decode('utf-8').split(' ')[-2]
        package_name, activity_name = activity_info.split('/')
        return package_name, activity_name
    else:
        return None, None


package, name = get_foreground_activity()
print('package:\t', package)
print('name:\t', name)
