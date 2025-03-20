import sys
from multiprocessing import Pool, Lock
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

FILE_DOMAINNAMES = './dnsnames_tmp.txt'
FILE_IPS = './ips.txt'
PROCESSESNUMBER = 8

class Domain:

    domains_with_ips = 0
    domains_without_ips = 0
    domains = 0
    lock = Lock()

    def __init__(self, domainname):
        self._domainname = domainname
        self._ips = []
        Domain.domains += 1

    def resolve_name(self):

            # print(socket.gethostbyname_ex(self._domainname))
            Domain.lock.acquire()
            try:
                logger.info("Increse domain with IP count, current count: " + Domain.domains_with_ips.__str__())
                Domain.domains_with_ips += 1
            finally:
                Domain.lock.release()
            # print(self._domainname + ": no IPs present")
            Domain.lock.acquire()
            try:
                logger.info("Increse domain without IP count, current count: " + Domain.domains_without_ips.__str__())
                Domain.domains_without_ips += 1
            finally:
                Domain.lock.release()

    @staticmethod
    def domains_statistics():
        logger.info("Domains count: " + Domain.domains.__str__())
        logger.info("Domains with IPs: " + Domain.domains_with_ips.__str__())
        logger.info("Domains without IPs: " + Domain.domains_without_ips.__str__())

def resolve_domainname(domain):
    domain.resolve_name()
    Domain.domains_statistics()
    return domain

def read_domainname_from_file():
    global FILE_DOMAINNAMES
    domainnames = []
    with open(FILE_DOMAINNAMES, 'r') as f:
        domainnames = [Domain(line.rstrip()) for line in f]
    Domain.domains_statistics()
    p = Pool(processes=PROCESSESNUMBER)
    p.map(resolve_domainname, domainnames)
    return domainnames
def main(argv):
    domainnames = read_domainname_from_file()
    # print(domainnames)
    Domain.domains_statistics()



if __name__ == "__main__":
    main(sys.argv)