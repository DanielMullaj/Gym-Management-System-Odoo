from odoo import fields, models


class GymActivity(models.Model):
    _name = 'gym.activity'
    _description = 'Gym Activity'

    name = fields.Selection([
        ('fitness', 'Fitness Class'),
        ('yoga', 'Yoga Class'),
        ('Crossfit', 'CrossFit Class')
    ], string='Name', required=True)
    trainer_id = fields.Many2one('gym.trainer', string='Trainer', required=True)
    duration = fields.Float(string='Duration (hours)')
    date = fields.Date(string='Date')
    start_time = fields.Datetime(string='Start Time')
    end_time = fields.Datetime(string='End Time')
