import sys
import argparse
import socket
import dns.query
import dns.resolver
from multiprocessing import Pool, Lock, Value
from ctypes import c_int
import time
from itertools import repeat
import logging



FILE_DOMAINNAMES = './dnsnames.txt'
FILE_IPS = './ips.txt'
DNS_RESOLVER = ['8.8.8.8','77.88.8.8']
PROCESSESNUMBER = 32
OUTPUTSTEPCOUNT = 100
LOGFILE = "./log.log"
log_counter = 0

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s, %(name)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',)
logger = logging.getLogger(__name__)

class Domain:

    domains = 0

    def __init__(self, domainname):
        self._domainname = domainname
        self._ips = []
        Domain.domains += 1

    @staticmethod
    def get_all_domains():
        # TODO
        pass
    def get_domain_name(self):
        return self._domainname
    def get_ips(self):
        return self._ips
    def add_ip(self,ip):
        self._ips.append(ip)
    def remove_ip(self,ip):
        self._ips.remove(ip)
    def resolve_name(self):
        resolver = dns.resolver.Resolver()
        resolver.nameservers = DNS_RESOLVER
        try:
            answers = resolver.query(self.get_domain_name(), 'A')
            for rdata in answers:
                self._ips.append(rdata.address)
        except dns.resolver.NoAnswer as ex:
            raise Exception(self.get_domain_name() + ": no IPs present")
        except (dns.resolver.NXDOMAIN,dns.resolver.NoNameservers) as ex:
            raise Exception(self.get_domain_name() + ex.__str__())
    @staticmethod
    def get_domains_count():
        return Domain.domains;

def domains_statistics(domainnames):
    domains_count = 0
    domains_with_ips = 0
    domains_without_ips = 0
    for domain in domainnames:
        domains_count += 1
        if not domain.get_ips():
            domains_without_ips += 1
        else:
            domains_with_ips += 1
    logger.info("Domains count: " + domains_count.__str__())
    logger.info("Domains with IPs: " + domains_with_ips.__str__())
    logger.info("Domains without IPs: " + domains_without_ips.__str__())

def timer(func):
    def wrapper(*args,**kwargs):
        # start the timer
        start_time = time.time()
        # call the decorated function
        result = func(*args, **kwargs)
        # remeasure the time
        end_time = time.time()
        # compute the elapsed time and print it
        execution_time = end_time - start_time
        logger.info(f"Execution time: {execution_time} seconds")
        # return the result of the decorated function execution
        return result
        # return reference to the wrapper function
    return wrapper

def resolve_domainname(domain, domains_count):

    step = int(domains_count/OUTPUTSTEPCOUNT)
    with l.get_lock():
        if (l.value % step == 0):
            print(f"Status progress: ({l.value}/{domains_count})")
        l.value += 1
    try:
        domain.resolve_name()
    except Exception as ex:
        logger.info(f"{ex.__str__()}")
    return domain

def init_pool_processes(shared_value):
    global l
    l = shared_value

def read_domainname_from_file():

    logger.info("Request IPs for domain names...")
    print("Request IPs for domain names...")
    global FILE_DOMAINNAMES
    l = Value(c_int, 0)
    domainnames = []
    with open(FILE_DOMAINNAMES, 'r') as f:
        domainnames = [Domain(line.rstrip()) for line in f]
    domains_count = Domain.get_domains_count()
    p = Pool(initializer=init_pool_processes,processes=PROCESSESNUMBER,initargs=(l,))
    result = p.starmap(resolve_domainname, zip(domainnames,
                                               repeat(domains_count)))
    # print(l.value)
    return result

def get_ips_by_domainname(domainname):
    return socket.gethostbyname_ex(domainname)[2]

def read_all_ips_from_domainclasses(domains):
    logger.info("Extracting IP from domain...")
    print("Extracting IP from domain...")
    ips_set = set()
    ips_list = []
    ips_count = 0
    for domain in domains:
        ip_domain = [ip for ip in domain.get_ips()]
        ips_list.extend(ip_domain)
    ips_set = set(ips_list)
    for ip in ips_set:
        ips_count += 1
    logger.info(f"Uniq IP addresses: {ips_count}")
    print(f"Uniq IP addresses: {ips_count}")
    return ips_set

def write_ips_to_file(ips):
    global FILE_IPS
    with open(FILE_IPS, 'w') as f:
        for ip in ips:
            f.write(ip + "\n")


@timer
def main():

    domainnames = read_domainname_from_file()
    write_ips_to_file(read_all_ips_from_domainclasses(domainnames))
    domains_statistics(domainnames)


def createParser():
    parser = argparse.ArgumentParser(description='Script to resolve Domain name to IPs for ACL using')
    parser.add_argument('-i', '--input_file', help='File with domain names')
    parser.add_argument('-o', '--output_file', help='File unique IP addresses')
    parser.add_argument('-s', '--dns_server', help = 'List of DNS servers to requests comma separated')
    return parser

if __name__ == "__main__":
    parser = createParser()
    namespace = parser.parse_args()
    if (namespace.input_file != None):
        FILE_DOMAINNAMES = namespace.input_file
    if (namespace.output_file != None):
        FILE_IPS = namespace.output_file
    if (namespace.dns_server != None):
        dns = namespace.dns_server.split(',')
        DNS_RESOLVER = dns
    # print(FILE_DOMAINNAMES)
    # print(FILE_IPS)
    # print(DNS_RESOLVER)
    # print(namespace)

    main()