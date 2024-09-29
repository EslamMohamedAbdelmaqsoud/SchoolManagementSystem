# dictionary that contains metadata about the module

{
    'name': 'School',
    'description': 'School Management System',
    'author': 'Eslam Mohamed',
    'depends': ['base', 'board'],

    'data': [

        "reports/school_subject_templates.xml",
        "reports/school_subject_reports.xml",
        "reports/school_student_templates.xml",
        "reports/school_student_reports.xml",

        'security/school_security.xml',
        'security/ir.model.access.csv',
        'views/school_management_system_view.xml',
        'views/school_class_view.xml',
        'views/school_subject_view.xml',
        'views/school_student_view.xml',
        'views/student_board.xml',
        'wizard/school_wizard_view.xml',

    ],
    'application': True,
    'installable': True,

}
