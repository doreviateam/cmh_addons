from odoo import fields, models, api


class EquipmentTemplate(models.Model):
    _name = 'equipment.template'  # I could do it differently or maybe better, for example, delegate to product.template
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Equipment template'

    _sql_constraints = [
        ('equipment_id_unique', 'UNIQUE(equipment_id)', 'Equipment must be unique.'),
    ]

    equipment_id = fields.Many2one(comodel_name='equipment.equipment', required=False, string='Equipment Template')
    image = fields.Binary(related='equipment_id.image')
    equipment_category = fields.Selection(related='equipment_id.equipment_category')
    detailed_type = fields.Selection(selection=[
        ('consu', 'Consumable'),
        ('service', 'Service'),
        ('product', 'Product')
    ], string='Equipment Type')
    tracking = fields.Selection(selection=[
        ('serial', 'Serial Number'),
        ('lot', 'Lot Number'),
        ('none', 'No Tracking')
    ], string='Tracking Mode', default='serial')
    display_name = fields.Char(compute='_compute_display_name', default='New')

    @api.model
    def _compute_display_name(self):
        for record in self:
            if record.equipment_id:
                record.display_name = record.equipment_id.name

    @api.model_create_multi
    def create(self, vals):
        equipment_templates = super().create(vals)

        for record in equipment_templates:
            if not self.env['product.product'].search([('equipment_id', '=', record.equipment_id.id)]):
                product_vals = {
                    'name': record.equipment_id.name,
                    'detailed_type': record.detailed_type,
                    'image_1920': record.image,
                    'equipment_category': record.equipment_category,
                    'equipment_id': record.equipment_id.id,
                    'tracking': record.tracking,
                }

                # Create products
                self.env['product.product'].create(product_vals)

                if not self.env['equipment.monitor'].search([('product_id', '=', record.equipment_id.id)]):
                    # Create an equipment.monitor object
                    monitor_vals = {
                        'product_id': record.equipment_id.id,
                    }

                    # Créez l'objet equipment.monitor
                    self.env['equipment.monitor'].create(monitor_vals)

        return equipment_templates


class ProductNumber(models.Model):
    _name = 'equipment.pn'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Equipment Product Number'

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'PN must be unique.'),
    ]

    name = fields.Char(string='Version Name', required=True)

