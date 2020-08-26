from azure.cli.core import get_default_cli
from typing import Dict, Union
import os
import shutil
import csv
import argparse
import sys

def azure_cli_run(cmd: str) -> Union[Dict, bool]:
    """Run Azure CLI command
    
    Returns
    -------
    cli.result
        stout of Azure CLI command
    
    Raises
    ------
    cli.result.error
        If sterror occurs due to azure CLI command
        TODO: this type is highly variable, should we add some checks?
    """

    args = cmd.split()
    cli = get_default_cli()
    cli.invoke(args)
    if cli.result.result:
        print("az {0}...".format(cmd))
        return cli.result.result
    elif cli.result.error:
        raise cli.result.error
    return True

class AcrBuild:
    def __init__(
        self,
        image_name: str,
        image_version: str,
        registry: str,
        platform: str = None,
        docker_path: str = ".",
        *args,
        **kwargs,
    ):
        """Build Docker image on Azure Container Registry.
        
        Parameters
        ----------
        image_name : str
            Name of image
        image_version : str
            Version of image
        registry : str
            Name of ACR Repository
        platform : str
            Platform for Image (Windows, Ubuntu)
        """

        self.image_name = image_name
        self.image_version = image_version
        self.registry = registry
        if platform:
            self.platform = platform
        else:
            docker_file = open("/".join([docker_path, "Dockerfile"]))
            docker_lines = docker_file.readlines()
            if "windows" in docker_lines[0]:
                self.platform = "windows"
            else:
                self.platform = "linux"
        self.docker_path = docker_path

        return super().__init__(*args, **kwargs)

    def build_image_acr(
        self, extra_build_args: Union[str, None], filename: str = "Dockerfile"
    ):

        if extra_build_args:
            buildargs = " --build-arg {0}".format(extra_build_args)
        else:
            buildargs = ""
        azure_cli_run(
            "acr build --image {0}:{1} --registry {2} --file {3}/{4} {3} --platform {5} {6}".format(
                self.image_name,
                self.image_version,
                self.registry,
                self.docker_path,
                filename,
                self.platform,
                buildargs,
            )
        )

def write_linux_python_dfile(sim_path, main_name):
    with open(sim_path+"/Dockerfile", 'w') as docker_fname:
        docker_fname.write('FROM python:3.7.4\n')
        docker_fname.write('RUN apt-get update && apt-get install -y --no-install-recommends && rm -rf /var/lib/apt/lists/*\n')
        docker_fname.write('WORKDIR /src\n')
        docker_fname.write('COPY . /src\n')
        docker_fname.write('RUN pip3 install setuptools wheel\n')
        docker_fname.write('RUN pip3 install -r requirements.txt\n')
        docker_fname.write('CMD ["python3", "{}"]\n'.format(main_name))

def write_windows_python_dfile(sim_path, main_name):
    with open(sim_path+"/Dockerfile", 'w') as docker_fname:
        docker_fname.write('FROM mcr.microsoft.com/windows:10.0.17763.1040\n')
        docker_fname.write('SHELL' + ' ["powershell", "-Command", "$ErrorActionPreference = ' + "'Stop'" + "; $ProgressPreference = 'SilentlyContinue';" '"]\n')
        docker_fname.write('ENV PYTHON_VERSION 3.7.6rc1\n')
        docker_fname.write('ENV PYTHON_RELEASE 3.7.6\n')
        docker_fname.write("RUN $url = ('https://www.python.org/ftp/python/{0}/python-{1}-amd64.exe' -f $env:PYTHON_RELEASE, $env:PYTHON_VERSION); Write-Host ('Downloading {0} ...' -f $url); [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri $url -OutFile 'python.exe'; Write-Host 'Installing ...'; Start-Process python.exe -Wait -ArgumentList @('/quiet', 'InstallAllUsers=1', 'TargetDir=C:\\Python', 'PrependPath=1', 'Shortcuts=0', 'Include_doc=0', 'Include_pip=0','Include_test=0'); $env:PATH = [Environment]::GetEnvironmentVariable('PATH', [EnvironmentVariableTarget]::Machine); Write-Host 'Verifying install ...'; Write-Host '  python --version'; python --version; Write-Host 'Removing ...'; Remove-Item python.exe -Force; Write-Host 'Complete.'\n")
        docker_fname.write('ENV PYTHON_PIP_VERSION 19.2.1\n')
        docker_fname.write('ENV PYTHON_GET_PIP_URL https://github.com/pypa/get-pip/raw/404c9418e33c5031b1a9ab623168b3e8a2ed8c88/get-pip.py\n')
        docker_fname.write('ENV PYTHON_GET_PIP_SHA256 56bb63d3cf54e7444351256f72a60f575f6d8c7f1faacffae33167afc8e7609d\n')
        docker_fname.write("RUN Write-Host ('Downloading get-pip.py ({0}) ...' -f $env:PYTHON_GET_PIP_URL); \ \n")
        docker_fname.write("    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; \ \n")
        docker_fname.write("    Invoke-WebRequest -Uri $env:PYTHON_GET_PIP_URL -OutFile 'get-pip.py'; \ \n")
        docker_fname.write("    Write-Host ('Verifying sha256 ({0}) ...' -f $env:PYTHON_GET_PIP_SHA256); \ \n")
        docker_fname.write("    if ((Get-FileHash 'get-pip.py' -Algorithm sha256).Hash -ne $env:PYTHON_GET_PIP_SHA256) { \ \n")
        docker_fname.write("        Write-Host 'FAILED!'; \ \n")
        docker_fname.write('        exit 1; \ \n')
        docker_fname.write('    }; \ \n')
        docker_fname.write("    Write-Host ('Installing pip=={0} ...' -f $env:PYTHON_PIP_VERSION); \ \n")
        docker_fname.write("    python get-pip.py --disable-pip-version-check --no-cache-dir ('pip=={0}' -f $env:PYTHON_PIP_VERSION) ; \ \n")
        docker_fname.write('    Remove-Item get-pip.py -Force; \ \n')
        docker_fname.write("    Write-Host 'Verifying pip install ...'; \ \n")
        docker_fname.write('    pip --version; \ \n')
        docker_fname.write("    Write-Host 'Complete.'\n")
        docker_fname.write('WORKDIR /src\n')
        docker_fname.write('COPY . /src\n')
        docker_fname.write('RUN pip3 install setuptools wheel\n')
        docker_fname.write('RUN pip3 install -r requirements.txt\n')
        docker_fname.write('CMD ["python", "{}"]\n'.format(main_name))

def main():
    parser = argparse.ArgumentParser(
        description='Run the application by using `sim-pack <language_api>` in a CLI to package the simulators for scaling using the Bonsai Service. The <language_api> modes can be switched by using: \n\n    python_api\n    java_api\n    C#_api\n\n Follow the requested prompts. Make sure to create a requirements.txt file with pinned versions of dependencies of the simulator.\n\n requirements.txt\n    numpy==1.16.4\n    matplotlib==3.0.3\n    ...\n',
        allow_abbrev=False,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        'language', 
        help='Provide a Microsoft Bonsai API mode (e.g., python_api, java_api, C#_api)'
    )
    parser.add_argument(
        '--platform',
        type=str, 
        help='Type the platform the simulator must run on, (e.g., windows or linux)',
    )
    args = parser.parse_args()

    if args.platform:
        platform = args.platform
    else:
        platform = input('Is windows or linux required to run Simulator?: ')

    sim_path = input("Directory of Simulator integration files: ")
    main_name = input("What is the name of the file with microsoft bonsai api? (e.g., __main__.py): ")
    
    if args.language == 'python_api':
        if platform == 'windows':
            write_windows_python_dfile(sim_path, main_name)
        elif platform == 'linux':
            write_linux_python_dfile(sim_path, main_name)
        else:
            print('Please type in correct OS type')
            exit()
        req_path = input("Directory of requirements.txt: ")
        if not os.path.isfile(req_path+'/requirements.txt'):
            shutil.copy(req_path+'/requirements.txt', sim_path)
    elif args.language == 'java_api':
        print('This path has not been programmed yet...')
        exit()
    elif args.language == 'C#_api':
        language = 'C#'
        print('This path has not been programmed yet...')
        exit()
    else:
        print('Please choose one the modes (e.g., python_api, java_api, C#_api)')
        exit()

    img_name = input("Image Name (No underscores): ")
    registry_name = input("Name of the ACR (without azurecr.io: ")

    acr_build_image = AcrBuild(
        image_name=img_name,
        image_version='latest',
        registry=registry_name,
        platform=platform,
        docker_path=sim_path,
    )
    
    acr_build_image.build_image_acr(
        filename='Dockerfile', extra_build_args=None
    )

if __name__ == '__main__':
    main()