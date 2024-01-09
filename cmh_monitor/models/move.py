from odoo import models, api
from odoo.exceptions import ValidationError


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    @api.constrains('lot_name', 'product_id')
    def _check_lot_in_monitor_line(self):
        for move_line in self:
            if move_line.product_id.tracking in ['lot', 'serial'] and move_line.lot_name:
                monitor_line = self.env['monitor.line'].search([
                    ('serial_number', '=', move_line.lot_name),
                    ('product_id', '=', move_line.product_id.id)
                ])
                if not monitor_line:
                    raise ValidationError(
                        f"The lot/serial number {move_line.lot_name} does not exist in Monitor for product"
                        f" {move_line.product_id.name}. Please, complete the Monitor before processed")
