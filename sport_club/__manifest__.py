< odoo >
< record
id = "group_sport_club_user"
model = "res.groups" >
< field
name = "name" > Sport
Club
User < / field >
< field
name = "category_id"
ref = "base.module_category_hr" / >
< / record >

< record
id = "group_sport_club_admin"
model = "res.groups" >
< field
name = "name" > Sport
Club
Admin < / field >
< field
name = "category_id"
ref = "base.module_category_hr" / >
< / record >

< !-- Access
rules -->
< record
id = "access_sport_club_user"
model = "ir.model.access" >
< field
name = "name" > access.sport.club.user < / field >
< field
name = "model_id"
ref = "model_club_visit" / >
< field
name = "group_id"
ref = "group_sport_club_user" / >
< field
name = "perm_read"
eval = "1" / >
< field
name = "perm_write"
eval = "0" / >
< field
name = "perm_create"
eval = "0" / >
< field
name = "perm_unlink"
eval = "0" / >
< / record >

< record
id = "access_sport_club_admin"
model = "ir.model.access" >
< field
name = "name" > access.sport.club.admin < / field >
< field
name = "model_id"
ref = "model_club_visit" / >
< field
name = "group_id"
ref = "group_sport_club_admin" / >
< field
name = "perm_read"
eval = "1" / >
< field
name = "perm_write"
eval = "1" / >
< field
name = "perm_create"
eval = "1" / >
< field
name = "perm_unlink"
eval = "1" / >
< / record >
< / odoo >
4.
Обновлення
manifest
Не
забудьте
додати
нові
файли
у
ваш
файл
__manifest__.py.

📄 __manifest__.py
python
Копіювати
Редагувати
{
    'name': 'Sport Club',
    'version': '1.0',
    'category': 'Sports',
    'summary': 'Module for managing a sports club with sessions, visits, and reports',
    'description': 'Manage club visits, sessions, and create certificates.',
    'author': 'Your Name',
    'depends': ['base'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizards/register_session_wizard.py',
        'views/club_visit_views.xml',
        'views/report_certificate.xml',
        'views/sport_club_menu.xml',
        'views/member_views.xml',
        'views/coach_views.xml',
        'views/training_session_views.xml',
        'views/subscription_views.xml',
        'views/event_views.xml',
        'views/wizard_views.xml',
        'reports/certificate_report.xml',
        'views/register_session_wizard_view.xml',
    ],
    'demo': [
        'demo/club_visit_demo.xml',
    ],
    'installable': True,
    'application': True,
}