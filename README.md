# WebRoot - Static Page Server

WebRoot is an easily deployable, lightweight, and secure server that can be deployed to any computer or storage device to expose a selected folder to the web. This specific version is the **Static Page WebRoot Server**, built to operate securely without the need for client-side scripts.

## Privacy and Security First

This server uses purely static pages (HTML and CSS only) and contains zero JavaScript. Because there is no JavaScript, the page completely reloads every time a user clicks on any link or button.

This architecture was specifically made for users who do not trust the server and is highly recommended for Tor users. It allows individuals to self-host a secure folder on the Tor network to easily transfer and share multiple files and folders safely.

## Key Features

* **Authentication:** Access is restricted using a login ID and password. The app intercepts users at the `/login` route to verify credentials before granting access to the file explorer.
* **File Explorer Interface (`/file_expo`):** Acts as the heart of the web app, allowing users to navigate parent directories, open folders, and refresh the current view.
* **Secure File Uploads & Downloads:** * Features a `/download` endpoint that forces files to be sent as attachments.
* Features an `/upload` endpoint that processes incoming files using Python threading for non-blocking execution and utilizes Werkzeug's `secure_filename` to sanitize file names.


* **HTTPS Enforcement:** The server automatically upgrades `http://` requests to `https://` requests via a 301 redirect.
* **Activity Logging:** Incorporates internal logging modules to track uploads, downloads, and system errors (`downloads_logger`, `uploads_logger`, and `error_log`).
* **Custom Error Pages:** Dedicated HTML templates are served for common HTTP errors, including 400 (Bad Request), 401 (Unauthorized), 403 (Forbidden), 404 (Not Found), and 500 (Internal Server Error).

## Technical Stack & Configuration

The application is built on top of the **Flask** web framework and uses **Gunicorn** to act as the production HTTP server.

**Server Specifications:**

* **Host & Port:** Binds to `0.0.0.0:5000` by default.
* **Workers:** Scales automatically by calculating `(number of CPU cores * 2) + 1` workers, utilizing the `gevent` worker class to handle up to 1000 concurrent connections per worker.
* **Certificates:** Requires local SSL certificates located at `./certificates/key.pem` and `./certificates/cert.pem` to ensure an encrypted connection.
