from odoo import models, fields


class SchoolWizard(models.TransientModel):
    _name = 'school.wizard'
    _description = 'School Wizard'

    student_id = fields.Many2one('school.student', string='Student')
    subject_id = fields.Many2one('school.subject', string='Subject')
    grade = fields.Float(string='Grade')

    def action_confirm(self):
        print('Student:', self.student_id.name)
        print('Subject:', self.subject_id.name)
        print('Grade:', self.grade)
