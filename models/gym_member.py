from odoo import models, fields, api
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
import re


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
    attendance_ids = fields.One2many('gym.attendance', 'member_id', string='Attendances')
    last_check_in = fields.Datetime(string='Last Check In', compute='_compute_last_check_in', store=True)
    payment_ids = fields.One2many('gym.payment', 'member_id', string='Payments')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('progress', 'Progress'),
        ('done', 'Confirmed'),
        ('cancel', 'Cancelled')], default='draft', string="Status", required=True)

    @api.constrains('email')
    def _check_email(self):
        email_pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        for record in self:
            if record.email and not email_pattern.match(record.email):
                raise ValidationError(
                    f"The email '{record.email}' is not valid. Please provide a correct email address."
                )

    @api.constrains('phone')
    def _check_phone(self):
        for record in self:
            if record.phone and not record.phone.isdigit():
                raise ValidationError('Phone number should contain only digits.')
            if len(record.phone) != 10:
                raise ValidationError('Phone number should be exactly 10 digits long.')

    @api.constrains('age')
    def _check_age(self):
        for record in self:
            if record.age < 17:
                raise ValidationError('Members under 17 years old cannot join the gym.')

    @api.depends('join_date', 'membership_id')
    def _compute_expiry_date(self):
        for record in self:
            if record.join_date and record.membership_id:
                duration = record.membership_id.duration
                record.expiry_date = record.join_date + relativedelta(months=duration)
            else:
                record.expiry_date = False

    @api.depends('attendance_ids.check_in')
    def _compute_last_check_in(self):
        for member in self:
            last_attendance = self.env['gym.attendance'].search([
                ('member_id', '=', member.id),
                ('status', '=', 'checked_in')
            ], limit=1, order='check_in desc')
            member.last_check_in = last_attendance.check_in if last_attendance else False

    def action_check_in(self):
        for member in self:
            self.env['gym.attendance'].create({
                'member_id': member.id,
                'check_in': fields.Datetime.now(),
            })

    def action_check_out(self):
        for member in self:
            last_attendance = self.env['gym.attendance'].search([
                ('member_id', '=', member.id),
                ('status', '=', 'checked_in')
            ], limit=1, order='check_in desc')
            if last_attendance:
                last_attendance.action_check_out()
            else:
                raise ValidationError('This member is not currently checked in.')

    def _capitalize_name(self):
        for record in self:
            if record.name:
                record.name = record.name[0].upper() + record.name[1:]

    @api.model
    def create(self, vals):
        if 'name' in vals and vals['name']:
            vals['name'] = vals['name'][0].upper() + vals['name'][1:]
        return super(GymMember, self).create(vals)

    def write(self, vals):
        if 'name' in vals and vals['name']:
            vals['name'] = vals['name'][0].upper() + vals['name'][1:]
        return super(GymMember, self).write(vals)

