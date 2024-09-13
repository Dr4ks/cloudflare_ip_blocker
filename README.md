# Hi, I'm Dr4ks! 👋

## 🚀 About Me
I'm a Cyber Security student and open always to learning.

## 🔗 Links
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/Dr4ks/)
[![hackerrank](https://img.shields.io/badge/HackerRank-2EC866?style=for-the-badge&logo=hackerrank&logoColor=white)](https://www.hackerrank.com/Dr4ks)
[![tryhackme](https://img.shields.io/badge/tryhackme-1DB954?style=for-the-badge&logo=tryhackme&logoColor=white)](https://tryhackme.com/p/Dr4ks)
[![HackTheBox](https://img.shields.io/badge/HackTheBox-2DC3E8?style=for-the-badge&logo=hackthebox&logoColor=green)](https://app.hackthebox.com/profile/1037035)
[![github](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Dr4ks)




# CloudFlare IP Blocker

## Description

This application is used to block malicious ip addresses on CloudFlare.

There 2 options are available.


**First**: You can enter `.txt` file which contains `IP Addresses` and seperated with each other line by line.

*Example:*
```bash
127.0.0.1
127.0.0.1
127.0.0.1
```

**Second**: You can enter single `IP Address` to add into Block List.


## Installation

```bash
git clone https://github.com/Dr4ks/cloudflare_ip_blocker
cd cloudflare_ip_blocker
pip install -r requirements.txt
```


## Usage

You can use this software in two ways. Before implementing both ways, you need to change `account_id` and `list_id` with your own system's values on `cdf_endpoint` variable.

1.

```bash
py main.py # gives you one session
```

2.

```bash
pyinstaller --onefile --noconsole main.py  # gives you executable on dist folder for later use
```


## Demonstration


Authentication Page:

![alt text](img/image.png)

Dashboard Page:

![alt text](img/image-1.png)