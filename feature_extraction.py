import re
from urllib.parse import urlparse

def extract_url_features(url):
    features = {}

    parsed = urlparse(url)
    hostname = parsed.hostname if parsed.hostname else ''
    path = parsed.path if parsed.path else ''

    # URL string features
    features["length_url"] = len(url)
    features["length_hostname"] = len(hostname)
    features["ip"] = 1 if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", hostname) else 0
    features["nb_dots"] = url.count('.')
    features["nb_hyphens"] = url.count('-')
    features["nb_at"] = url.count('@')
    features["nb_qm"] = url.count('?')
    features["nb_and"] = url.count('&')
    features["nb_or"] = url.count('|')
    features["nb_eq"] = url.count('=')
    features["nb_underscore"] = url.count('_')
    features["nb_tilde"] = url.count('~')
    features["nb_percent"] = url.count('%')
    features["nb_slash"] = url.count('/')
    features["nb_star"] = url.count('*')
    features["nb_colon"] = url.count(':')
    features["nb_comma"] = url.count(',')
    features["nb_semicolumn"] = url.count(';')
    features["nb_dollar"] = url.count('$')
    features["nb_space"] = url.count(' ')
    features["nb_www"] = url.count('www')
    features["nb_com"] = url.count('.com')
    features["nb_dslash"] = url.count('//')

    # Special token check
    features["http_in_path"] = int("http" in path.lower())
    features["https_token"] = int("https" in url.lower())

    # Digit ratios
    digits_in_url = sum(c.isdigit() for c in url)
    digits_in_host = sum(c.isdigit() for c in hostname)
    features["ratio_digits_url"] = digits_in_url / len(url)
    features["ratio_digits_host"] = digits_in_host / len(hostname) if hostname else 0

    # Other URL structure
    features["punycode"] = int("xn--" in url)
    features["port"] = int(parsed.port) if parsed.port else 0
    features["tld_in_path"] = int(any(tld in path for tld in [".com", ".net", ".org"]))
    features["tld_in_subdomain"] = int(any(tld in hostname.split('.')[0] for tld in [".com", ".net", ".org"]))
    features["abnormal_subdomain"] = int(len(hostname.split('.')) > 3)
    features["nb_subdomains"] = len(hostname.split('.')) - 2 if len(hostname.split('.')) > 2 else 0
    features["prefix_suffix"] = int('-' in hostname)

    # Shortener services
    shortening_services = r"(bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|tinyurl|tr\.im|is\.gd|cli\.gs|yfrog\.com|migre\.me|ff\.im|tiny\.cc)"
    features["shortening_service"] = int(re.search(shortening_services, url) is not None)

    return features
