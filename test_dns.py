import dns.query
import dns.resolver
def main():
    domain = "yandex.ru"
    where = ["8.8.8.8",'77.88.8.8', '77.88.8.1']
    resolver = dns.resolver.Resolver()
    resolver.nameservers = where
    answers = resolver.query(domain, 'A')

    for rdata in answers:
        print(rdata.address)



if __name__ == "__main__":
    main()