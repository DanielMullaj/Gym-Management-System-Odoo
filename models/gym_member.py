import re
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
import logging

_logger = logging.getLogger(__name__)


class GymMember(models.Model):
    _name = 'gym.member'
    _description = 'Gym Member'

    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    age = fields.Integer(string='Age')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string='Gender')
    join_date = fields.Date(string='Join Date', default=fields.Date.today)
    expiry_date = fields.Date(string='Expiry Date', compute='_compute_expiry_date', store=True)
    membership_id = fields.Many2one('gym.membership', string='Membership')

    @api.constrains('email')
    def _check_email(self):
        email_pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        for record in self:
            if record.email and not email_pattern.match(record.email):
                raise models.ValidationError(
                    f"The email '{record.email}' is not valid. Please provide a correct email address."
                )

    @api.constrains('age')
    def _check_age(self):
        for record in self:
            if record.age < 17:
                raise models.ValidationError(
                    f"Members must be at least 17 years old to join the gym. '{record.name}' is too young."
                )

    @api.constrains('phone')
    def _check_phone(self):
        phone_pattern = re.compile(r"^\d{9}$")
        for record in self:
            if record.phone and not phone_pattern.match(record.phone):
                raise models.ValidationError(
                    f"The phone number '{record.phone}' is not valid. Phone numbers in Albania must be exactly 9 digits."
                )

    @api.depends('join_date', 'membership_id')
    def _compute_expiry_date(self):
        for record in self:
            if record.join_date and record.membership_id:
                try:
                    duration = record.membership_id.duration
                    _logger.info(f"Calculating expiry date: join_date={record.join_date}, duration={duration}")
                    record.expiry_date = record.join_date + relativedelta(months=duration)
                    _logger.info(f"Computed expiry_date={record.expiry_date}")
                except Exception as e:
                    _logger.error(f"Error calculating expiry date: {e}")
                    record.expiry_date = False
            else:
                record.expiry_date = False

    def _capitalize_name(self):
        for record in self:
            if record.name:
                record.name = record.name.capitalize()

    @api.model
    def create(self, vals):
        if 'name' in vals:
            vals['name'] = vals['name'].capitalize()
        return super(GymMember, self).create(vals)

    def write(self, vals):
        if 'name' in vals and vals['name']:
            vals['name'] = vals['name'].capitalize()
        return super(GymMember, self).write(vals)
