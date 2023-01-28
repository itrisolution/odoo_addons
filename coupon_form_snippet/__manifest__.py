# -*- coding: utf-8 -*-

{
    'name': 'Coupon Form Snippet',
    'version': '15.0.1.0.0',
    'summary': 'Coupon Form Snippet',
    'description': """Coupon Form Snippet""",
    'author': 'Imal-Tech',
    'website': 'https://www.imal-tech.com',
    'maintainer': 'Imal-Tech',
    'company': 'Imal-Tech',
    'category': 'Website',
    'depends': ['base', 'coupon'],
    'data': [
        'data/form_coupon_mail.xml',
        'views/coupon_for_snippet.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'coupon_form_snippet/static/src/js/intlTelInput.js',
            'coupon_form_snippet/static/src/css/coupon_form_snippet.css',
            'coupon_form_snippet/static/src/js/coupon_form_snippet.js',
        ],
    },
    'sequence': -1,
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
