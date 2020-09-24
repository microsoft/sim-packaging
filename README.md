# Sim Packaging
Tooling to abstract away docker building of simulators that cannot be zip file dropped into the Bonsai Service as the status quo. It is a CLI tool which prompts for simulator dependencies, OS requirements, authenticates with ACR, builds, and pushes for you.

>🚩 Disclaimer: This is not an official Microsoft product. This application is considered an experimental addition to Microsoft Project Bonsai's software toolchain. It's primary goal is to reduce barriers of entry to use Project Bonsai's core Machine Teaching. Pull requests for fixes and small enhancements are welcome, but we do expect this to be replaced by out-of-the-box features of Project Bonsai in the near future.

## Requirements
- Python 3.7+
- Azure command line tools
- Azure permissions to ACR
- amd64 based host
- simulator that can reset, step using the following languages:
    - Python
    - Java
    - C#

## Installation
```bash
pip install -e .
```

## Running
If one is unsure how to use the application, be sure to use the help flag.
```bash
sim-pack --help
```

### 1. Azure login
Make sure you have an active Azure login session.
(Note that this only needs to be run periodically).

```bash
az login
```

### 2. ACR Login
Make sure you have an active login credential to the ACR created by your managed resource from the Bonsai workspace. 
(Note that this only needs to be run periodically)

```bash
az acr login -n <ACR_NAME>
```

### 3. Create a requirements.txt
Create a file with dependencies for the simulator. For python, select pypi pinned versions like the following:

```javascript
numpy==1.16.4
matplotlib==3.0.3
pandas==0.25.1
scipy==1.3.0
microsoft-bonsai-api==0.1.2
bonsai-cli==1.0.1
```

### 4. Run the Script

Run `sim-pack <LANGUAGE_API>` where the `<LANGUAGE_API>` mode can consist of:
- python_api
- java_api
- C#_api

> Note: Only the python path is functional.

For example, the python route will look like the following.

```bash
sim-pack python_api
```

The application will prompt you for responses, an example may look like the following.

```bash
Is windows or linux required to run Simulator?: windows
Directory of Simulator integration files: sample/
What is the name of the file with microsoft bonsai api? (e.g., main.py): main.py
Directory of requirements.txt: .
Image Name (No underscores): my-first-sim
Name of the ACR (without azurecr.io): mydemo
```

### Optional flags

If one desires to specify their base image for complex scenarios, use the `--base-img` flag and enter a string of the base image. This may be helpful in scenarios where the simulator is dependent on another base image other than the following: `python:3.7.4`for Linux and `mcr.microsoft.com/windows:10.0.17763.1040` for Windows. This can also be particularly useful when a base image is used with previously installed dependencies. When using a base image that cannot be downloadable without credentials, be sure the base image exists in the desired ACR.

```bash
sim-pack python_api --base-img <BASE_IMG>
```

>Example: sim-pack python_api --base-img mydemo.azurecr.io/sample-base:latest

## Contribute Code
This project welcomes contributions and suggestions. Most contributions require you to
agree to a Contributor License Agreement (CLA) declaring that you have the right to,
and actually do, grant us the rights to use your contribution. For details, visit
https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether you need
to provide a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the
instructions provided by the bot. You will only need to do this once across all repositories using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/)
or contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Telemetry
The software may collect information about you and your use of the software and send it to Microsoft. Microsoft may use this information to provide services and improve our products and services. You may turn off the telemetry as described in the repository. There are also some features in the software that may enable you and Microsoft to collect data from users of your applications. If you use these features, you must comply with applicable law, including providing appropriate notices to users of your applications together with a copy of Microsoft's privacy statement. Our privacy statement is located at https://go.microsoft.com/fwlink/?LinkID=824704. You can learn more about data collection and use in the help documentation and our privacy statement. Your use of the software operates as your consent to these practices.

## Trademarks
This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft trademarks or logos is subject to and must follow Microsoft's Trademark & Brand Guidelines. Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship. Any use of third-party trademarks or logos are subject to those third-party's policies.