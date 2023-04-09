# S3TakeOver

S3TakeOver is a simple Python script that checks for potential subdomain takeover vulnerabilities when a DNS record points to a non-existing S3 bucket. This tool is designed for educational purposes and should be used responsibly.

# S3 Subdomain Takeover Checker & Exploiter

This script checks domains for possible S3 takeover vulnerabilities (subdomain takeover) and creates a static S3 website with a simple HTML file on each vulnerable domain found.

## Features

- Enumerates subdomains of a given domain using Google search
- Checks if the enumerated subdomains are vulnerable to S3 takeover
- Automatically creates a static S3 website with a simple HTML file for each vulnerable domain


## About Subdomain Takeover

A subdomain takeover vulnerability occurs when a DNS record points to a resource (in this case, an S3 bucket) that no longer exists. An attacker can then create a resource with the same name, potentially gaining control over the subdomain and serving malicious content or phishing pages. This script checks for such vulnerabilities by looking for specific error messages and status codes in the HTTP responses.

## Installation

To install the dependencies listed in the requirements.txt file, use the following command:
```bash
pip install -r requirements.txt
```

Or
```bash
pip install requests googlesearch-python boto3
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
    
    
## Notes

- This script is for educational purposes only and should not be used to exploit unauthorized systems.
- Ensure you have the necessary AWS permissions to create and manage S3 buckets.
