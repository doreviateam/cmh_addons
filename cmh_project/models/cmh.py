from odoo import models, fields


class Partners(models.Model):
    _inherit = 'res.partner'

    _sql_constraints = [
        ('shortname_unique', 'UNIQUE(shortname)', 'Short name must be unique.')
    ]

    shortname = fields.Char(help='e.g. CRCA31')
