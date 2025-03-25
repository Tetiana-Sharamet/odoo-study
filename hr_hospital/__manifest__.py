{
    'name': 'Hr Hospital',
    'summary': '',
    'author': 'Tetiana Sharamet',
    'category': 'Customizations',
    'license': 'OPL-1',
    'version': '17.0.1.0.1',

    'depends': ['base'],

    'external_dependencies': {'python': []},

    'data': [
        'security/ir.model.access.csv',
        'data/hr_hospital_disease.xml',
        'wizard/set_personal_doctor_wizard_view.xml',
        'wizard/hr_hospital_disease_report_wizard_view.xml',
        'views/hr_hospital_menu.xml',
        'views/hr_hospital_patient_views.xml',
        'views/hr_hospital_visit_views.xml',
        'views/hr_hospital_doctor_views.xml',
        'views/hr_hospital_diagnosis_views.xml',
        'views/hr_hospital_disease_views.xml',
    ],

    'demo': [
        'demo/hr_hospital_demo.xml',
    ],

    'installable': True,
    'auto_install': False,

    'images': [
        'static/description/icon.png'
    ],

}
