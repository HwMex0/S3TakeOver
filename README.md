# S3TakeOver

S3TakeOver is a Python script that checks for potential subdomain takeover vulnerabilities when a DNS record points to a non-existing S3 bucket. This tool is designed for educational purposes and should be used responsibly.

## About Subdomain Takeover

A subdomain takeover vulnerability occurs when a DNS record points to a resource (in this case, an S3 bucket) that no longer exists. An attacker can then create a resource with the same name, potentially gaining control over the subdomain and serving malicious content or phishing pages. This script checks for such vulnerabilities by looking for specific error messages and status codes in the HTTP responses.

## Installation

No installation is needed. Simply download the script and make sure you have Python 3 and the `requests` and `googlesearch-python` libraries installed. You can install the libraries using pip:

```bash
pip install requests googlesearch-python
```


# Usage

There are two ways to use the script:

1. Provide a file containing a list of domains (one per line) using the `-f` or `--file` argument:
`python s3takeover.py -f domains.txt`

2. Provide a single domain using the -d or --domain argument. The script will use Google Dork to enumerate subdomains for the specified domain:
`python s3takeover.py -d example.com`

You can also set a custom timeout for the domain enumeration requests using the `-t` or `--timeout` argument (default is 2 seconds):
`python s3takeover.py -d example.com -t 5`

To limit the number of search results returned when using Google Dork, use the -s or --stop argument (default is 20):
`python s3takeover.py -d example.com -s 50`

After the script finishes running, it will print the results in three categories:

    1. Vulnerable Domains: Domains with a 404 status code and "Code: NoSuchBucket" in the response.
    3. Non-Matched Domains: Domains that do not meet the criteria for a potential subdomain takeover.
    4. Error Occurred: Domains where an error occurred during the check.
    
    
Remember to use this tool responsibly and for educational purposes only 
