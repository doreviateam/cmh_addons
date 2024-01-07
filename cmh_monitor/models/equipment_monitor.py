from odoo import fields, models, api


class EquipmentMonitor(models.Model):
    _name = 'equipment.monitor'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Equipment monitor'

    _sql_constraints = [
        ('product_id_unique', 'UNIQUE(product_id)', 'Product must be unique.'),
    ]

    name = fields.Char(related='product_id.name')
    product_id = fields.Many2one(comodel_name='product.template', required=True,
                                 domain=[])
    image_1920 = fields.Binary(related='product_id.image_1920')

    line_ids = fields.One2many(
        comodel_name='monitor.line',
        inverse_name='equipment_monitor_id',
        string='Equipments',
        required=False)
    equipment_count = fields.Integer(compute='_compute_equipment_count', store=True)
    free_qty = fields.Float(compute='_compute_on_hand_qty', string='Free quantity')
    uom_id = fields.Char(related='product_id.uom_id.name')

    @api.depends('product_id')
    def _compute_on_hand_qty(self):
        for record in self:
            products = self.env['product.product'].search([('id', '=', record.product_id.id)])
            free_qty = sum(product.free_qty for product in products) if products else 0.0
            record.free_qty = round(free_qty, 0)

    @api.depends('line_ids')
    def _compute_equipment_count(self):
        for record in self:
            record.equipment_count = len(record.line_ids)


class EquipmentLine(models.Model):
    _name = 'monitor.line'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Monitor line'
    _rec_name = 'serial_number'

    serial_number = fields.Char(string='Lot/Serial Number', required=True)
    product_number = fields.Char()
    equipment_monitor_id = fields.Many2one(comodel_name='equipment.monitor', string='Equipment Monitor')
    product_id = fields.Many2one(related='equipment_monitor_id.product_id')
    image_1920 = fields.Binary(related='equipment_monitor_id.product_id.image_1920')
    owner_id = fields.Many2one(comodel_name='res.partner')
    shortname = fields.Char(compute='_compute_shortname', store=True)
    option_ids = fields.Many2many('equipment.option', string='Options')
    fullname = fields.Char(compute='_compute_fullname', default='New', string='Equipment')

    @api.depends('owner_id')
    def _compute_shortname(self):
        for record in self:
            record.shortname = record.owner_id.shortname or record.owner_id.name or ''

    @api.depends('product_id', 'shortname')
    def _compute_fullname(self):
        for record in self:
            if record.product_id and record.shortname:
                record.fullname = f'{record.product_id.name} {record.shortname}'.upper()


class EquipmentOption(models.Model):
    _name = 'equipment.option'
    _description = 'Equipment option'

    name = fields.Char(required=True)
