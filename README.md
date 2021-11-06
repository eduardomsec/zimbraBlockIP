# zimbraBlockIP
Block IP Invalid Login - Zimbra


This program aims to search logs from the zimbra mail server and filter for invalid logins.
Afterwards, an iptables rule is created to block the destination host. 

# Usage

Default usage:

```bash
./zimbraBlockIP.py 
```

This program has a options with `file`, `authentication` and `debug`.
Show optins and descriptions with `-h`

```bash
./zimbraBlockIP.py -h

Block Zimbra Authentication

optional arguments:
  -h, --help            show this help message and exit
  --file FILE           File zimbra.log
  --authentication AUTHENTICATION
                        Number of authentication failed
  --debug DEBUG         Active DEBUG True or False
```

Example usage

```bash
./zimbraBlockIP.py --authentication 5 --file /var/log/zimbra.log --debug true
```