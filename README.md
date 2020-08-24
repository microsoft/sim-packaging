# Sim Packaging
Tooling to abstract away docker building of simulators that cannot be zip file dropped into the Bonsai Service as the status quo. It is a CLI tool which prompts for dependencies, OS requirements, logs into ACR, builds, and pushes for you.

> DISCLAIMER: This application is considered experimental and NOT an official Microsoft Bonsai tool. Use as one likes, feel free to submit PRs with fixes and small enhancements. We DO expect this to be replaced by in-product features of Microsoft Bonsai in the next few months, so we DO NOT encourage major contributions. 

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
microsoft-bonsai-api==0.1.1
bonsai-cli==1.0.0
```

### 4. Run the Script

Run `sim-pack <language_api>` where the `<language_api>` mode can consist of:
- python_api
- java_api
- C#_api

For example, the python route will look like the following.

```bash
sim-pack python_api
```

The application will prompt you for responses, an example may look like the following.

```bash
Is windows or linux required to run Simulator?: windows
Directory of Simulator: sample/
What is the name of the file with microsoft bonsai api? (e.g., __main__.py): __main__.py
Directory of requirements.txt: .
Image Name (No underscores): my-first-sim
Name of the ACR (without azurecr.io: mydemo
```