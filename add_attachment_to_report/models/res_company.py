# -*- coding: utf-8 -*-

from odoo import models, fields, _, api


class ResCompany(models.Model):
    """ Inherit Res Company to add related_model_ids """
    _inherit = 'res.company'

    related_model_ids = fields.Many2many('ir.model', string="Modules", domain="[('transient', '=', False), ('is_mail_thread', '=', True)]")

