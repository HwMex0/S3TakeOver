# S3TakeOver

S3TakeOver is a Python script that checks a list of domains for the potential of an S3 subdomain takeover vulnerability. The script checks if the response code is 404 and if the response contains "Code: NoSuchBucket", which may indicate that the domain is pointing to a non-existent S3 bucket. This tool is meant for educational purposes only and should not be used for any malicious activities.

## S3 Subdomain Takeover

An S3 subdomain takeover is a type of security vulnerability that occurs when a domain or subdomain is configured with a DNS record (e.g., CNAME) pointing to an Amazon S3 bucket that does not exist or has been deleted. An attacker can exploit this vulnerability by creating an S3 bucket with the same name and potentially serve malicious content or intercept sensitive data.

The attack is possible because of the way some DNS providers handle CNAME records that point to non-existent resources. When a CNAME record points to an S3 bucket that does not exist, Amazon returns an HTTP 404 status code with a "Code: NoSuchBucket" message in the response. By identifying such cases, it may be possible to discover misconfigured DNS records that could lead to subdomain takeover vulnerabilities.

## Requirements

- Python 3
- `requests` library (install using `pip install requests`)

## Usage

1. Clone this repository or download the script `s3takeover.py`.

2. Prepare a text file with a list of domain names to check, with one domain per line. Example:

    example-domain-1.com
    example-domain-2.com
    example-domain-3.com
    

3. Run the script with the following command-line arguments:
    python s3takeover.py -f domains.txt -t 2
    

Replace `s3takeover.py` with the name of the Python script, `domains.txt` with the path to your text file containing the domains, and `2` with the desired timeout value in seconds.

The script will output the results in three categories:

- Matched Domains: Domains that have a 404 status code and 'Code: NoSuchBucket' in the response
- Non-Matched Domains: Domains that do not meet the criteria
- Errors: Domains where an error occurred during the check



## Mitigation

To prevent S3 subdomain takeover attacks, it is essential to monitor DNS records and ensure that they point to valid and existing resources. When removing or updating S3 buckets, make sure to update the corresponding DNS records as well.

It is also recommended to use DNS providers that automatically remove or block CNAME records pointing to non-existent resources.

## Disclaimer

This tool is intended for educational purposes only. The authors and contributors are not responsible for any misuse or damage caused by this tool. Always seek permission from the domain owners before testing for vulnerabilities.
