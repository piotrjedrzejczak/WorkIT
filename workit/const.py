CATEGORIES = {
    'Frontend': {
        'frontend', 'front', 'typescript', 'javascript', 'js', 'vue', 'react',
        'angular', 'html', 'css', 'sass', 'node', 'acf', 'wordpress',
        'cms', 'ember', 'express', 'jquery', 'redux', 'vue.js', 'node.js',
        'react.js'
        },
    'Backend': {
        'backend', 'back', 'python', 'java', 'rails', 'ruby', 'php', 'symfony',
        'django', 'pyramid', 'flask', 'asp.net', 'mvc', 'apache', 'entity',
        'golang', 'graphql', 'hadoop', 'laravel', 'drupal', '.net', 'c#', 'go'
        },
    'Fullstack': {'fullstack', 'full', 'stack'},
    'Mobile': {
        'mobile', 'kotlin', 'swift', 'xamarin',
        'objectivec', 'android', 'ios', 'flutter'
        },
    'Data Science': {
        'data', 'database', 'db', 'sql', 'etl', 'ai', 'ml', 'artificial',
        'nlp', 'machine', 'learning', 'keras', 'pytorch', 'natural',
        'automl', 'matlab'
        },
    'C/C++': {'c', 'c++'},
    'Networks': {
        'sip', 'tcp', 'ccna', 'ccnp', 'cisco', 'networking',
        'haproxy', 'kerberos', 'network', 'sieci', 'sieciowy'
        },
    'DevOps': {'devops', 'ansible', 'ops'},
    'Testing': {'test', 'qa', 'junit', 'tester', 'quality', 'pentester'},
    'Cloud': {
        'cloud', 'aws', 'azure', 'amazon web services', 'heroku',
        'cloudops'
        },
    'Embedded': {'embedded', 'firmware'},
    'Hardware': {'hardware'},
    'GameDev': {'game', 'unity', 'unreal', 'gameplay'},
    'Analytics': {
        'bi', 'analiza', 'analityk', 'analysis', 'analyst',
        'analytics'
        },
    'Administration': {'admin', 'administrator'},
    'RPA': {'rpa', 'robotic', 'automation', 'anywhere', 'uipath', 'blueprism'},
    'SAP': {'sap', 'abap', 'hana'},
    'Security': {'security', 'cryptography', 'cybersecurity'},
    'Design': {'designer', 'ui', 'ux', 'design', 'adobe', 'photoshop'},
    'Ecommerce': {'sales', 'ecommerce', 'salesforce', 'magento'},
    'Support': {'helpdesk', 'support', 'service', 'supporter'},
    'Management': {
        'scrum', 'manager', 'management', 'cto',
        'leader', 'lead', 'product', 'head'
        },
    'HR': {'recruitment', 'recruit', 'recruiter', 'lms'},
    'Functional Programming': {'haskell', 'f#', 'scala'},
    'Automotive': {'autosar', 'automotive'}
}

POLISH_CHARS = {
    'ę': 'e',
    'ó': 'o',
    'ą': 'a',
    'ś': 's',
    'ł': 'l',
    'ż': 'z',
    'ź': 'z',
    'ć': 'c',
    'ń': 'n'
}

CURRENCIES = {
    'PLN': {'pln', 'zł', 'złoty'},
    'EUR': {'eur', 'euro', '€'},
    'USD': {'usd', 'dollar', 'dolar', '$'}
}

from workit.websites.BullDog import BullDogJobs  # noqa E402
from workit.websites.JustJoin import JustJoinJobs  # noqa E402
from workit.websites.NoFluff import NoFluffJobs  # noqa E402
from workit.websites.JobsForGeek import JobsForGeek # noqa E402
from workit.websites.Pracuj import PracujJobs # noqa E402

WEBSITES = [
    JustJoinJobs(),
    NoFluffJobs(),
    BullDogJobs(),
    JobsForGeek(),
    PracujJobs()
]
