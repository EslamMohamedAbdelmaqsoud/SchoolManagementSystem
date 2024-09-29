from odoo.tests.common import TransactionCase


class TestSchoolStudent(TransactionCase):

    # Method to setup the test environment for the test cases to run
    def setUp(self, *args, **kwargs):
        super(TestSchoolStudent, self).setUp()
        self.student_01_record = self.env['school.student'].create({
            'name': 'John Doe',
            'gender': 'm',
            'student_id': '12'})

    # Method Test Case for Student Values
    def test_01_student_values(self):
        student_id = self.student_01_record
        self.assertRecordValues(student_id, [{
            'name': 'John Doe',
            'gender': 'm',
            'student_id': '12'
        }])
