from odoo import models, fields, api


class SchoolClass(models.Model):
    _name = 'school.class'
    _rec_name = 'name'

    name = fields.Char(string='Name')
    year_id = fields.Many2one('school.management.system', string='Year')
