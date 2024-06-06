# Changelog

## 0.2.2 - 2024-06-06

- Added the `aspsp status` command for fetching ASPSP integration status information.
- Fixed a small issue in the base command handled.

## 0.2.1 - 2024-02-19

- Added the `app request-logs` command for fetching logs associated with a requests.
- Added `-l/--logs` parameter for the `app request` command for fetching logs associated with requests.

## 0.2.0 - 2024-02-17

- Added the `app requests` command for fetching the log of requests made by an application.
- Made the `app register` command to store application properties locally, so that they are easy to
  use with other commands.
- Added optional parameters for the `app register` command: `-d/--description`, `--gdpr-email`,
  `--privacy-url` and `--terms-url`.
- Small fixes and improvements.

## 0.1.1 - 2024-01-10

Refreshing token on the response code 401 instead of 403 as the control panel API has changed
accordingly.

## 0.1.0 - 2023-12-31

The very first version with minimum functionality only allowing to authenticate as a user of Enable
Banking Control Panel and register new applications.
