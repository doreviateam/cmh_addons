{
    'name': 'CMH Equipment Monitor',
    'version': '0.1',
    'summary': 'Module to manage CMH activities',
    'description': 'Module to manage cash engine',
    'category': 'CMH',
    'author': 'David Saint-Aignan',
    'website': '',
    'license': 'LGPL-3',
    'depends': ['cmh_fleet'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/menus.xml',
        'views/equipment_monitor.xml',
        'views/monitor_line.xml',
    ],
    'demo': [],
    'sequence': 1,
    'application': False,
    'installable': True,
    'auto_install': False
}