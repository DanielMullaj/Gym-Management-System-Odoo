from odoo import models, fields, api
from odoo.exceptions import ValidationError


class GymAttendance(models.Model):
    _name = 'gym.attendance'
    _description = 'Gym Attendance'
    _order = 'check_in desc'

    member_id = fields.Many2one('gym.member', string='Member', required=True)
    check_in = fields.Datetime(string='Check In', default=fields.Datetime.now, required=True)
    check_out = fields.Datetime(string='Check Out')
    status = fields.Selection([
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out')
    ], string='Status', default='checked_in', readonly=True)

    @api.constrains('check_in', 'check_out')
    def _check_check_out_after_check_in(self):
        for record in self:
            if record.check_out and record.check_out < record.check_in:
                raise ValidationError('Check-out time must be after check-in time.')

    @api.model
    def create(self, vals):
        if 'member_id' in vals:
            existing_attendance = self.search([
                ('member_id', '=', vals['member_id']),
                ('status', '=', 'checked_in')
            ], limit=1)
            if existing_attendance:
                raise ValidationError('This member is already checked in.')
        return super(GymAttendance, self).create(vals)

    def action_check_out(self):
        for record in self:
            if record.status == 'checked_out':
                raise ValidationError('This member is already checked out.')
            record.write({
                'check_out': fields.Datetime.now(),
                'status': 'checked_out'
            })
