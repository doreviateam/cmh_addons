from odoo import api, models


class CronStockLot(models.AbstractModel):
    _name = 'stock.lot.cron'
    _description = 'Stock Lot Cron'

    @api.model
    def process_stock_lots(self):
        try:
            # 1. For each stock.lot object with processed_by_cron set to False, create an equipment.fleet object.
            stock_lots = self.env['stock.lot'].search([('processed_by_cron', '=', False)])

            for stock_lot in stock_lots:
                # 2. If the lot is created for a product_id within an equipment_category of 00,
                # then create the equipment.fleet object.
                if stock_lot.product_id.equipment_category == '00':
                    self.env['equipment.fleet'].create({
                        'serial_number_id': stock_lot.id,
                    })

            # 3. Then mark the stock.lot as processed.
            for stock_lot in stock_lots:
                stock_lot.write({'processed_by_cron': True})

            return True

        except Exception as e:
            # Handle unexpected exceptions
            print(f"Unexpected Error: {str(e)}")
            return False
