from odoo import fields, models
from odoo.exceptions import ValidationError


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
    state = fields.Selection([
        ('draft', 'Draft'),
        ('progress', 'Progress'),
        ('done', 'Finished'),
        ('cancel', 'Cancelled')], default='draft', string="Status", required=True)

    def action_share_whatsapp(self):
        if not self.trainer_id.phone:
            raise ValidationError("Missing phone number in trainer record")
        message = 'Hi *%s*, your next *activity* is on: %s. Thank you!' % (self.trainer_id.name, self.start_time)
        whatsapp_api_url = 'https://api.whatsapp.com/send?phone=%s&text=%s' % (self.trainer_id.phone, message)
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': whatsapp_api_url
        }
