from odoo import models, fields, api
import requests

from odoo.odoo.exceptions import ValidationError


class SchoolStudent(models.Model):
    _name = 'school.student'
    _rec_name = 'name'

    name = fields.Char(string='Name', required=True, translate=True)
    class_id = fields.Many2one('school.class', string='Class')
    year_id = fields.Many2one('school.management.system', related='class_id.year_id', readonly=True)
    subject_ids = fields.Many2many('school.subject', string='Subjects')
    image = fields.Binary(string='Image')

    ######################## Computed Field ######################################
    birth_date = fields.Date(string='Birth Date')
    age = fields.Float(string='Age', compute='_compute_age', store=True, index=True)

    @api.depends('birth_date')
    def _compute_age(self):
        for record in self:
            if record.birth_date:
                today = fields.Date.today()
                birth_date = fields.Date.from_string(record.birth_date)
                record.age = today.year - birth_date.year - (
                        (today.month, today.day) < (birth_date.month, birth_date.day))
            else:
                record.age = 0

    gender = fields.Selection(
        [('m', "Male"),
         ('f', "Female")], default='m')

    ######################## Constraints ( Validations & Unique ) ######################################
    @api.constrains('age')
    def _check_age(self):
        for record in self:
            if record.age < 7:
                raise ValueError("Age must be greater than 7")

    student_id = fields.Char(string='Student ID', required=True)
    _sql_constraints = [('unique_student_id', 'unique(student_id)', 'ID already exists'), ]

    #################### Security Rules ############################

    lecture = fields.Many2one('res.users', string="Lecture")

    ########################################################################################################

    # Fetch data from another model using API (GET Request)
    def get_school_students(self):
        payload = dict()
        try:
            response = requests.get('http://localhost:8069/v1/school.students', data=payload)
            if response.status_code == 200:
                print("Data fetched successfully")
                print(response)
            else:
                print("Error fetching data")
        except Exception as error:
            raise ValidationError(str(error))
