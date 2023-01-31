# -*- coding: utf-8 -*-

{
    'name': 'Dark mode button',
    'version': '16.0.1.0.0',
    'summary': 'Dark Mode Button',
    'description': """Dark Mode Button""",
    'author': 'Imal-Tech',
    'website': 'https://www.imal-tech.com',
    'maintainer': 'Imal-Tech',
    'company': 'Imal-Tech',
    'category': 'Website',
    'depends': ['base'],
    'data': [],
    'assets': {
        'web.assets_backend': [
            '/dark_mode_button/static/src/js/dark_mode_button.js',
            '/dark_mode_button/static/src/xml/dark_mode_button.xml',
        ],
    },
    'images': ['static/description/banner.gif'],
    'sequence': -1,
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
