# DNS Resolve
Application resolve list of DNS names to list of unique IP addresses.
Application use multiprocessing, you can change number of proceesses by change PROCESSESNUMBER global variable

usage: dnsResolve.py [-h] [-i INPUT_FILE] [-o OUTPUT_FILE] [-s DNS_SERVER]

Script to resolve Domain name to IPs for ACL using

options:

  -h, --help            show this help message and exit

  -i INPUT_FILE, --input_file INPUT_FILE File with domain names

  -o OUTPUT_FILE, --output_file OUTPUT_FILE File unique IP addresses

  -s DNS_SERVER, --dns_server DNS_SERVER List of DNS servers to requests comma separated

Usefull args 

```-i dnsnames.txt -o ipfile.txt -s 8.8.8.8,1.1.1.1```
- -i Read dns list from file dnsnames.txt
- -o Write ip addresses to ipfile.txt
- -s Use 8.8.8.8 and 1.1.1.1 DNS servers