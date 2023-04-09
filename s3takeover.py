import requests
import argparse
from googlesearch import search


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
    for url in search(f"site:{domain}", stop=stop):
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
    return parser.parse_args()

def print_results(matched_domains, non_matched_domains, errored_domains):
    print_banner()
    print("\nVulnerable Domains:")
    for domain in matched_domains:
        print(f"  [+] {domain}")

    print("\nNon-Matched Domains:")
    for domain in non_matched_domains:
        print(f"  [-] {domain}")

    print("\nError Occurred:")
    for domain, error in errored_domains:
        print(f"  [*] {domain}")

if __name__ == "__main__":
    args = parse_arguments()
    filename = args.file
    timeout = args.timeout
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
