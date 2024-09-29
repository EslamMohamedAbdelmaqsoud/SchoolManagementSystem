from odoo import models, fields, api


class SchoolSubject(models.Model):
    _name = 'school.subject'
    _rec_name = 'name'

    name = fields.Char(string='Name')
    year_id = fields.Many2one('school.management.system', string='Year')
