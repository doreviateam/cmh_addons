{
    'name': 'CMH Equipment Fleet',
    'version': '0.1',
    'summary': 'Module to manage CMH activities',
    'description': 'Module to manage cash engine',
    'category': 'CMH',
    'author': 'David Saint-Aignan',
    'website': '',
    'license': 'LGPL-3',
    'depends': ['cmh_equipment', 'base'],
    'data': [
        'data/cron_stock_lot.xml',
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/menus.xml',
        'views/fleet_views.xml',
    ],
    'demo': [],
    'sequence': 1,
    'application': False,
    'installable': True,
    'auto_install': False
}