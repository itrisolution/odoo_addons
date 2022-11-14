# -*- coding: utf-8 -*-

from odoo import models, fields, _, api


class ResConfig(models.TransientModel):
    """ Inherit Res Config Settings to add default image product field """
    _inherit = 'res.config.settings'

    product_default_image = fields.Binary(string="Default Image")

    @api.model
    def get_values(self):
        res = super(ResConfig, self).get_values()
        res.update(
            product_default_image=self.env['ir.config_parameter'].sudo().get_param(
                'res.config.settings.product_default_image'),
        )
        return res

    def set_values(self):
        super(ResConfig, self).set_values()
        param = self.env['ir.config_parameter'].sudo()
        param.set_param('res.config.settings.product_default_image', self.product_default_image)
