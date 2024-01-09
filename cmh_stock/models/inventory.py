from odoo import models, api
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.constrains('pack_operation_product_ids')
    def _check_serial_lot_availability(self):
        for picking in self:
            for operation in picking.pack_operation_product_ids:
                if operation.product_id.tracking == 'serial':
                    self._check_serial_availability(operation.product_id, operation.lot_id)
                elif operation.product_id.tracking == 'lot':
                    self._check_lot_availability(operation.product_id, operation.lot_id)

    def _check_serial_availability(self, product, lot):
        if lot:
            monitor_line = self.env['monitor.line'].search([('serial_number', '=', lot)])
            if not monitor_line:
                raise ValidationError(
                    f"The serial number {lot} does not exist in monitor.line for product {product.name}.")

    def _check_lot_availability(self, product, lot):
        if lot:
            monitor_line = self.env['monitor.line'].search([('serial_number', '=', lot)])
            if not monitor_line:
                raise ValidationError(
                    f"The lot number {lot} does not exist in monitor.line for product {product.name}.")
