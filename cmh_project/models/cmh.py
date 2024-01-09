from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Partners(models.Model):
    _inherit = 'res.partner'

    _sql_constraints = [
        ('shortname_unique', 'UNIQUE(shortname)', 'Short name must be unique.')
    ]

    shortname = fields.Char(help='e.g. CRCA31')

    @api.model_create_multi
    def create(self, vals_list):
        partners = super().create(vals_list)
        for partner, vals in zip(partners, vals_list):
            if 'shortname' in vals and vals['shortname']:
                partner.write({'shortname': vals['shortname'].upper()})
        return partners

    @api.onchange('shortname')
    def _onchange_shortname(self):
        if self.shortname:
            self.shortname = self.shortname.upper()

    def write(self, vals):
        if 'shortname' in vals and vals['shortname']:
            vals['shortname'] = vals['shortname'].upper()
        return super().write(vals)

# pour tout article suivi par serial ou lot (numéro de série ou numéro de lot), je dois vérifier si le serial ou lot number existe dans monitor.line
# avant de valider une réception, un transfert interne ou une livraison
