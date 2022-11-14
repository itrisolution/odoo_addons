# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools


class ProductTemplate(models.Model):
    """ Inherit Product Template Settings to add default image product from setting """
    _inherit = "product.template"

    @api.model_create_multi
    def create(self, vals_list):
        for val_list in vals_list:
            if not val_list['image_1920']:
                product_default_image = self.env['ir.config_parameter'].sudo().get_param(
                    'res.config.settings.product_default_image')
                if product_default_image:
                    val_list['image_1920'] = product_default_image

        return super(ProductTemplate, self).create(vals_list)
