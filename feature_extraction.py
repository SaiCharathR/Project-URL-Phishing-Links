import re
import urllib.parse

def extract_features(url):
    features = {}

    parsed = urllib.parse.urlparse(url)
    hostname = parsed.hostname or ''
    path = parsed.path or ''

    # Length-based
    features['length_url'] = len(url)
    features['length_hostname'] = len(hostname)

    # Count-based features
    features['nb_dots'] = url.count('.')
    features['nb_hyphens'] = url.count('-')
    features['nb_at'] = url.count('@')
    features['nb_qm'] = url.count('?')
    features['nb_and'] = url.count('&')
    features['nb_or'] = url.count('|')
    features['nb_eq'] = url.count('=')
    features['nb_underscore'] = url.count('_')
    features['nb_tilde'] = url.count('~')
    features['nb_percent'] = url.count('%')
    features['nb_slash'] = url.count('/')
    features['nb_star'] = url.count('*')
    features['nb_colon'] = url.count(':')
    features['nb_comma'] = url.count(',')
    features['nb_semicolumn'] = url.count(';')
    features['nb_dollar'] = url.count('$')
    features['nb_space'] = url.count(' ')

    # Word-based counts
    features['nb_www'] = url.lower().count('www')
    features['nb_com'] = url.lower().count('.com')
    features['nb_dslash'] = url.count('//')

    # Binary features
    features['http_in_path'] = int('http' in path.lower())
    features['https_token'] = int('https' in path.lower() or 'https' in hostname.lower())
    features['has_ip'] = int(bool(re.match(r'^\d{1,3}(\.\d{1,3}){3}$', hostname)))

    # Ratio-based features
    digits = sum(c.isdigit() for c in url)
    features['ratio_digits_url'] = digits / len(url)
    digits_host = sum(c.isdigit() for c in hostname)
    features['ratio_digits_host'] = digits_host / len(hostname) if hostname else 0

    # Other lexical features
    features['punycode'] = int('xn--' in url)
    features['port'] = int(bool(parsed.port))
    features['tld_in_path'] = int(any(tld in path.lower() for tld in ['.com', '.net', '.org', '.info']))
    features['tld_in_subdomain'] = int(any(tld in hostname.lower().split('.')[0] for tld in ['.com', '.net', '.org', '.info']))
    features['abnormal_subdomain'] = int(len(hostname.split('.')) > 3)
    features['nb_subdomains'] = len(hostname.split('.')) - 2 if len(hostname.split('.')) > 2 else 0
    features['prefix_suffix'] = int('-' in hostname)
    features['random_domain'] = int(bool(re.search(r'[a-z]{3,}\d{3,}', hostname)))

    # Shortening service
    shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|qr\.ae|adf\.ly|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|tr\.im|link\.zip\.net"
    features['shortening_service'] = int(bool(re.search(shortening_services, url)))

    # Path extension
    extension = path.split('.')[-1] if '.' in path else ''
    features['path_extension'] = extension

    return features
