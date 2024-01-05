from odoo import fields, models, api


class EquipmentFleet(models.Model):
    _name = 'equipment.fleet'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Equipment fleet'

    _sql_constraints = [
        ('serial_number_id_unique', 'UNIQUE(serial_number_id)', 'Serial Number must be unique.'),
    ]

    serial_number_id = fields.Many2one(comodel_name='stock.lot', string='Lot/Serial Number', required=True,
                                       ondelete='restrict', readonly=True)
    image_1920 = fields.Binary(related='serial_number_id.product_id.image_1920')
    product_number = fields.Char()
    ref = fields.Char(related='serial_number_id.ref')
    product_qty = fields.Float(related='serial_number_id.product_qty')
    location_name = fields.Char(related='serial_number_id.location_id.name', string='Location')
    location_id = fields.Many2one(related='serial_number_id.location_id', string='Location Reference')
    product_id = fields.Many2one(related='serial_number_id.product_id')
    equipment_category = fields.Selection(related='serial_number_id.product_id.equipment_category')

    @api.model_create_multi
    def create(self, vals_list):
        # Convert data to uppercase before recording
        for vals in vals_list:
            if 'product_number' in vals and vals['product_number']:
                vals['product_number'] = vals['product_number'].upper()

                # Check if 'ref' is in stock.lot for serial_number_id in stock.lot
                # if False or '' then set ref = vals["product_number"] in stock.lot
                stock_lot_records = self.env['stock.lot'].search([
                    ('id', '=', vals['serial_number_id']),
                    ('ref', 'in', ['', False])
                ])
                if stock_lot_records:
                    stock_lot_records.ref = vals["product_number"]

        return super().create(vals_list)

    def write(self, vals):
        # Convert data to uppercase before recording

        # Check if 'product_number' is in vals and vals['product_number'] is not None
        if 'product_number' in vals and vals['product_number']:
            vals['product_number'] = vals['product_number'].upper()
        elif 'product_number' in vals and vals['product_number'] is False:
            vals['product_number'] = ''

        # Update the 'ref' field of 'serial_number_id'
        if 'product_number' in vals:
            self.serial_number_id.ref = vals['product_number']

        return super().write(vals)


class StockLot(models.Model):
    _inherit = 'stock.lot'

    processed_by_cron = fields.Boolean('Processed by Cron', default=False)

    @api.model_create_multi
    def create(self, vals_list):
        # Convert data to uppercase before recording
        created_records = super().create(vals_list)

        # Create equipment.fleet records
        for record in created_records:
            if record.name:
                record.name = record.name.upper()

        return created_records

    def write(self, vals):
        # Convert data to uppercase before recording

        # Check if 'name' is in vals and vals['name'] is not None
        if 'name' in vals and vals['name']:
            vals['name'] = vals['name'].upper()

        # Check if 'ref' is in vals and vals['ref'] is not None
        if 'ref' in vals and vals['ref']:
            vals['ref'] = vals['ref'].upper()
        elif 'ref' in vals and vals['ref'] is False:
            vals['ref'] = ''

        return super().write(vals)
