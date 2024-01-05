from odoo import fields, models, api


class Product(models.Model):
    _inherit = 'product.template'

    _sql_constraints = [
        ('equipment_id_unique', 'UNIQUE(equipment_id)', 'This equipment reference must stay unique for products.'),
    ]

    equipment_category = fields.Selection(
        string='Equipment Category',
        selection=[('00', 'Pos equipment'),
                   ('10', 'Other equipment'), ],
        required=True, default='10')
    equipment_id = fields.Many2one('equipment.equipment', string='Equipment Reference')

    @api.model_create_multi
    def create(self, vals):
        products = super().create(vals)

        for product in products:
            if product.name:
                product.name = product.name.upper()

        return products
