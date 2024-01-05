from odoo import fields, models, api


class Stock(models.Model):
    _inherit = 'stock.picking'
