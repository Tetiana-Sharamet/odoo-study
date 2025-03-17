{
    'name': 'Hr Hospital',
    'summary': '',
    'author': 'Tetiana Sharamet',
    'category': 'Customizations',
    'license': 'OPL-1',
    'version': '17.0.0.0.1',

    'depends': ['base'],

    'external_dependencies': {'python': []},

    'data': [
        'security/ir.model.access.csv',
        'views/hr_hospital_menu.xml',
        'views/hr_hospital_patient_patient_views.xml',
        'views/hr_hospital_doctor_views.xml',],

    'demo': [
        'demo/hr_hospital_demo.xml',

    ],


    'installable': True,
    'auto_install': False,
}