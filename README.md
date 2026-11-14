**Cybersecurity project (Cyber Security Base 2026)**

https://cybersecuritybase.mooc.fi/ 

A small note-taking web application built with Python and Django. Users can register, log in, add entries, view them, and search their own entries.

The application intentionally contains five security flaws from the **OWASP Top 10 2021** list. Each flaw is marked in the code with a `FLAW` comment, and its fix is included next to it as commented-out code.

| # | OWASP 2021 category | Location |
|---|---|---|
| 1 | A01 Broken Access Control | `myapp/views.py`, `detail` |
| 2 | A02 Cryptographic Failures | `mysite/settings.py`, `PASSWORD_HASHERS` |
| 3 | A03 Injection | `myapp/views.py`, `search` |
| 4 | A07 Identification and Authentication Failures | `myapp/views.py`, `register` |
| 5 | A09 Security Logging and Monitoring Failures | `myapp/views.py`, top of the file |

Screenshots of each flaw before and after the fix are in the `screenshots` folder.

## Requirements

- Python 3.10 or newer
- Git

## Installation

Clone the repository and move into it:

```
git clone https://github.com/alkaakin/Cybersecurity-MOOC-Project.git
cd Cybersecurity-MOOC-Project
```

Create and activate a virtual environment.

Linux and macOS:

```
python3 -m venv venv
source venv/bin/activate
```

Windows (PowerShell):

```
python -m venv venv
venv\Scripts\Activate.ps1
```

Install the dependencies:

```
pip install -r requirements.txt
```
## Setting up the database

The database is not included in the repository, so create it:

```
python manage.py migrate
```

Create an admin account. The admin site (`/admin/`) is used to inspect stored password hashes for flaw 2:

```
python manage.py createsuperuser
```

## Running the application

```
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser.

## Test users

The database starts empty. To test the flaws, register **two** users through the "New user? Register" link on the login page (for example `alice` and `bob`), and add a few entries for each. Several flaws (1 and 3) are demonstrated by one user accessing the other user's entries.

## Applying the fixes

Each fix is commented out directly below or next to its flaw. To apply a fix, comment out the flawed lines and uncomment the fix, as described in the `FIX` comment. Restart the server if it does not reload automatically.
