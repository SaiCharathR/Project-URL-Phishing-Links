import whois
from datetime import datetime
import socket

def extract_whois_features(url):
    features = {
        "domain_registration_length": 0,
        "domain_age": 0,
        "dns_record": 0,
        "whois_registered_domain": 0
    }

    try:
        domain = url.split("//")[-1].split("/")[0]
        w = whois.whois(domain)

        creation_date = w.creation_date
        expiration_date = w.expiration_date

        # Handle list vs single datetime case
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        if isinstance(expiration_date, list):
            expiration_date = expiration_date[0]

        if creation_date and expiration_date:
            features["domain_registration_length"] = (expiration_date - creation_date).days
            features["domain_age"] = (datetime.now() - creation_date).days
            features["whois_registered_domain"] = 1

    except Exception:
        features["whois_registered_domain"] = 0

    try:
        socket.gethostbyname(domain)
        features["dns_record"] = 1
    except:
        features["dns_record"] = 0

    return features
