import re

from odoo import models, fields, api


class GymTrainer(models.Model):
    _name = 'gym.trainer'
    _description = 'Gym Trainer'

    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email')
    phone = fields.Integer(string='Phone')
    specialization = fields.Char(string='Specialization')
    member_ids = fields.Many2many('gym.member', string='Members')

    @api.constrains('email')
    def _check_email(self):
        email_pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        for record in self:
            if record.email and not email_pattern.match(record.email):
                raise models.ValidationError(
                    f"The email '{record.email}' is not valid. Please provide a correct email address.")
