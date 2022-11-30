# -*- coding: utf-8 -*-
{
    'name': 'Default Product Image',
    'description': """
            This module will help you to add default image to products with no images.
        """,
    'summary': 'Module to help you add default image to products',
    'author': 'Imal-Tech',
    'website': 'https://www.imal-tech.com',
    'maintainer': 'Imal-Tech',
    'category': 'Sales',
    'version': '15.0.1.0.0',
    'depends': ['base', 'sale_management'],
    'data': [
        'views/res_config_views.xml',
    ],
    'license': 'LGPL-3',
    'images': ['static/description/banner.gif'],
    'installable': True,
    'application': False,
    'auto_install': False,
}