# Garuda 🔎

[![version-1.0](https://img.shields.io/badge/version-1.0-green)](https://github.com/Datalux/Garuda/releases/tag/1.0)
[![Python3](https://img.shields.io/badge/language-Python3-red)](https://img.shields.io/badge/language-Python3-red)
[![Telegram](https://img.shields.io/badge/Telegram-Channel-blue.svg)](https://t.me/Itsydv)

Garuda is a **FUN OSINT** tool on Instagram to know who haven\'t followed you back.

Disclaimer: **FOR FUN AND PERSONEL USE ONLY!**

Warning: It is advisable to **not** use your own/primary account when using this tool.

## Installation ⚙️

1. Fork/Clone/Download this repo

    `git clone https://github.com/Itsydv/Garuda.git`

2. Navigate to the directory

    `cd Garuda`

3. Create a virtual environment for this project

    `python3 -m venv venv`

4. Load the virtual environment
   - On Windows Powershell: `.\venv\Scripts\activate.ps1`
   - On Linux and Git Bash: `source venv/bin/activate`
  
5. Run `pip install -r requirements.txt`

6. Execute `make setup` command in terminal/shell to create the `credentials.ini` file to save Instagram account username and password in the corresponding fields

7. Run the main.py script in one of two ways

    * As an interactive prompt `python3 main.py <target username>`
    * Or execute your command straight away `python3 main.py <target username> --command <command>` where commands ->  check, help

### External library 🔗
[Instagram API](https://github.com/ping/instagram_private_api)

### Special Thanks
[Datalux for Osintgram Tool](https://github.com/Datalux/Osintgram)
Because I have used some functionalities of Original Osint Tool by Datalux just for Educational Purpose. There is No Intention of taking Credits or Earning anything using this.
