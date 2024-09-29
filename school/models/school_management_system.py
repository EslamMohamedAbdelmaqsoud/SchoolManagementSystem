from odoo import models, fields, api


class SchoolManagementSystem(models.Model):
    _name = 'school.management.system'
    _rec_name = 'year'

    year = fields.Integer(string='Year')
    number_of_classes = fields.Integer(string='Number of Classes')
