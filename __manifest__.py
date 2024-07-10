{
    'name': 'Daniel Gym',
    'version': '1.0',
    'summary': 'Summery',
    'description': 'Description',
    'category': 'Gym Management',
    'author': 'Author',
    'website': 'Website',
    'depends': ['base', 'mail', 'calendar', 'sale'],
    'data': [
        'views/gym_menus.xml',
        'data/email_template_data.xml',
        'views/gym_member_views.xml',
        'views/gym_activity_views.xml',
        'views/gym_attendance_views.xml',
        'views/gym_membership_views.xml',
        'views/gym_trainer_views.xml',
        'views/gym_payment_views.xml',
    ],

    'installable': True,
    'auto_install': False,
    'application': True,
}
