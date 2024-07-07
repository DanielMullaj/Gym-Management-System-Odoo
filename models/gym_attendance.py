from odoo import fields, models


class GymAttendance(models.Model):
    _name = 'gym.attendance'
    _description = 'Gym Attendance'

    member_id = fields.Many2one('gym.member', string='Member')
    check_in = fields.Datetime(string='Check In')
    check_out = fields.Datetime(string='Check Out')
