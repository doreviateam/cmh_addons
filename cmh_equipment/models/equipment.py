import base64

from odoo import fields, models, api
from odoo.tools.misc import file_path


class Brand(models.Model):
    _name = 'equipment.brand'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Equipment Brand'

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Brand must be unique.'),
    ]

    name = fields.Char(string='Brand Name', required=True, default='_')
    equipment_ids = fields.One2many(comodel_name='equipment.equipment', inverse_name='brand_id', string='Equipments')
    model_ids = fields.One2many(comodel_name='equipment.brand_model', inverse_name='brand_id', string='Models')

    @api.model_create_multi
    def create(self, vals):
        brands = super().create(vals)
        for brand, vals in zip(brands, vals):
            if 'name' in vals and len(vals['name']) > 1 or vals['name'] != '_':
                brand.write({'name': vals['name'].upper().replace('_', ' ')})
        return brands


class BrandModel(models.Model):
    _name = 'equipment.brand_model'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Equipment Model'
    _rec_name = 'display_name'

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name, brand_id)', 'Model and brand must be unique.'),
    ]

    name = fields.Char(string='Model Name', required=True)
    brand_id = fields.Many2one(comodel_name='equipment.brand', required=True)
    equipment_ids = fields.One2many(comodel_name='equipment.equipment', inverse_name='model_id', string='Equipments')
    display_name = fields.Char(compute='_compute_display_name', default='New')

    @api.model_create_multi
    def create(self, vals):
        brand_models = super().create(vals)
        for brand_model, vals in zip(brand_models, vals):
            if 'name' in vals and len(vals['name']) > 1 or vals['name'] != '_':
                brand_model.write({'name': vals['name'].upper().replace('_', ' ')})
        return brand_models

    @api.depends('name', 'brand_id')
    def _compute_display_name(self):
        for record in self:
            if record.name and record.brand_id:
                record.display_name = f"{record.brand_id.name} {record.name}".upper().replace('_', ' ')


class Version(models.Model):
    _name = 'equipment.version'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Equipment Version'

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Version must be unique.'),
    ]

    name = fields.Char(string='Version Name', required=True, default='_')

    @api.model_create_multi
    def create(self, vals):
        versions = super().create(vals)
        for version, vals in zip(versions, vals):
            if 'name' in vals and len(vals['name']) > 1 or vals['name'] != '_':
                version.write({'name': vals['name'].upper().replace('_', ' ')})
        return versions


class Equipment(models.Model):
    _name = 'equipment.equipment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Equipment'

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Equipment must be unique.')
    ]

    name = fields.Char(compute='_compute_fullname', default='New', store=True)
    image = fields.Binary()
    brand_id = fields.Many2one(related='model_id.brand_id')
    model_id = fields.Many2one(comodel_name='equipment.brand_model', string='Model', required=True)
    version_id = fields.Many2one(comodel_name='equipment.version', string='Version', required=True)
    equipment_category = fields.Selection(
        string='Equipment Category',
        selection=[('00', 'Pos equipment'),
                   ('10', 'Other equipment'), ],
        required=True, default='00')

    @api.depends('brand_id', 'model_id', 'version_id')
    def _compute_fullname(self):
        for record in self:
            if record.brand_id and record.model_id and record.version_id:
                record.name = f"{record.brand_id.name} {record.model_id.name}" \
                              f" {record.version_id.name}"
                if len(record.name) > 1:
                    record.name = f"{record.name}"
                    if '_' in f"{record.name}":
                        record.name = record.name.replace('_', ' ')
