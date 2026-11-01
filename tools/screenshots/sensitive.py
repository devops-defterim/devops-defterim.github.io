"""Ekran görüntülerinde karartılacak hassas metin desenleri.

Kişisel desenler (ad, kullanıcı adı, bilgisayar adı) koda yazılmaz;
private-notes/redact-names.txt dosyasından okunur (her satır bir regex).
"""
import os
import re

KEEP_IP = {
    '127.0.0.1', '0.0.0.0', '8.8.8.8', '8.8.4.4', '1.1.1.1', '169.254.169.254', '10.10.10.10',
    '255.255.255.0', '255.255.255.255', '172.31.0.0', '172.31.0.1', '172.31.0.2', '199.199.199.0',
}
KEEP_IP_PREFIX = ('255.', '209.85.', '18.206.107.')


def _names():
    path = os.path.join(os.path.dirname(__file__), '..', '..', 'private-notes', 'redact-names.txt')
    if not os.path.exists(path):
        return None
    pats = [l.strip() for l in open(path, encoding='utf-8') if l.strip() and not l.startswith('#')]
    return re.compile('|'.join(pats), re.I) if pats else None


PATTERNS = [
    ('account', re.compile(r'(?<![\d-])(\d{4}-\d{4}-\d{4}|\d{12})(?![\d-])')),
    ('hostname', re.compile(r'ip-\d{1,3}-\d{1,3}-\d{1,3}-\d{1,3}', re.I)),
    ('ec2dns', re.compile(r'ec2-\d{1,3}-\d{1,3}-\d{1,3}-\d{1,3}[\w.-]*', re.I)),
    ('ipv4', re.compile(r'(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?:/\d{1,2})?(?![\d.])')),
    ('email', re.compile(r'[\w.+-]+@[\w-]+\.(com|net|org|io|tr)\b[\w.]*', re.I)),
    ('iamid', re.compile(r'\bA(IDA|ROA|IPA|NPA|NVA|SCA|GPA)[A-Z0-9]{10,}')),
    ('awskey', re.compile(r'(AKIA|ASIA)[0-9A-Z]{8,}')),
    ('secret', re.compile(r'(?<![A-Za-z0-9/+])(?=[A-Za-z0-9/+]*[A-Z])(?=[A-Za-z0-9/+]*[a-z])(?=[A-Za-z0-9/+]*\d)[A-Za-z0-9/+]{30,}(?![A-Za-z0-9/+])')),
    ('ghtoken', re.compile(r'gh[pousr]_[A-Za-z0-9]{10,}|github_pat_\w+')),
    ('resid', re.compile(r'\b(i|vol|sg|subnet|vpc|eni|rtb|igw|snap|lt|acl|nat|ami)-[0-9a-f]{8,17}\b', re.I)),
    ('mac', re.compile(r'\b(?!00:00:00|ff:ff:ff)([0-9a-f]{2}:){5}[0-9a-f]{2}\b', re.I)),
    ('fingerprint', re.compile(r'SHA256:[A-Za-z0-9+/]{20,}')),
]
_n = _names()
if _n is not None:
    PATTERNS.append(('name', _n))


def find(text):
    hits = []
    for kind, rx in PATTERNS:
        for m in rx.finditer(text):
            v = m.group(0)
            if kind == 'ipv4':
                ip = v.split('/')[0]
                if any(int(p) > 255 for p in ip.split('.')) or ip in KEEP_IP or ip.startswith(KEEP_IP_PREFIX):
                    continue
            if kind == 'secret' and ('Policy' in v or 'Role' in v or v.startswith('policy/')):
                continue
            hits.append((kind, m.start(), m.end()))
    return hits
