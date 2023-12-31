# Enable Banking CLI

A command-line interface for Enable Banking API and its control panel

## About

The Enable Banking CLI provides developers using Enable Banking API the possibility to manage the
service from the command line or through scripts and other automation.

This project also aims to implement simple yet powerful command-line interface for accessing banking
data and initiating payments through open banking APIs integrated by Enable Banking. This functionality
is based on the [api.enablebanking.com](https://api.enablebanking.com/) aggregating Open Banking APIs
(also known as PSD2 APIs) of a large number of financial institutions in Europe.

## How to install

It's the easiest to install the CLI using the Python Package Installer (PyPI):

```sh
pip3 install enablebanking-cli
```

If you want to do modifications, clone the repository from Github:

```sh
git clone https://github.com/enablebanking/enablebanking-cli.git
cd enablebanking-cli
pip3 install -r requirements.txt
```

## How to run

When installed using PyPI, the CLI can be run simply as:

```sh
enablebanking
```

Alternatively, the CLI is run like this:

```sh
python3 -m enablebanking_cli
```

This way you can run it from the source code; run the command from the repository root.

## How to use

When the CLI is run without arguments (i.e. `enablebanking` or `python3 -m enablebanking_cli`), the
usage information is displayed.

```
% enablebanking
usage: enablebanking [-h] [--cp-domain CP_DOMAIN] [--api-domain API_DOMAIN] [--root-path ROOT_PATH] {app,auth} ...

Enable Banking Command-Line Utility

optional arguments:
  -h, --help            show this help message and exit
  --cp-domain CP_DOMAIN
                        Domain of the Enable Banking Control Panel
  --api-domain API_DOMAIN
                        Domain of the Enable Banking API
  --root-path ROOT_PATH
                        Root path under which files used by this utility are stored

Commands:
  {app,auth}
    app                 Application commands
    auth                Authentication commands
```

Commands supported by the CLI are divided into several groups. In order to display list of commands in
a group, run the CLI passing the group name followed by `-h`, e.g. `enablebanking auth -h`.

```
% enablebanking auth -h
usage: enablebanking auth [-h] {default,list,login,logout} ...

optional arguments:
  -h, --help            show this help message and exit

Authentication Commands:
  {default,list,login,logout}
    default             Set an authenticated user to be used by default
    list                Display authenticated users
    login               Sign in as a user of the Enable Banking Control Panel
    logout              Remove locally stored credentials of an authenticated user
```

In order to display full usage details for a command, run the command followed by `-h`, e.g.
`enablebanking auth login -h`.

```
% enablebanking auth login -h
usage: enablebanking auth login [-h] [--callback-port CALLBACK_PORT] email

positional arguments:
  email                 User's email

optional arguments:
  -h, --help            show this help message and exit
  --callback-port CALLBACK_PORT
                        Port number of the authentication callback server
```

## How to package

```sh
pip3 install --upgrade build
```

```sh
python3 -m build
```

## Plans

The following commands and groups of commands are planned to be implemented:

- `app logs`, the command providing the possibility to fetch API request/response logs;
- `accounts`, the group of commands providing the possibility to authorise access to accounts in
  multiple ASPSPs (i.e. banks and similar financial institutions), fetch account balances and
  transactions, as well as perform periodic data synchronisation;
- `payments`, the group of commands providing the possibility to initiate and confirm payments;
- `data-insights`, the group of commands providing the possibility to retrieve statistical information
  about details on account information and payments being provided by different ASPSPs.

Suggest features and report bugs by submitting issues in the Github project [here](https://github.com/enablebanking/enablebanking-cli/issues/new).
