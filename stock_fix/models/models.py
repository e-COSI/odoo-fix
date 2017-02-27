# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from datetime import datetime
from dateutil import relativedelta

class Orderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    def _get_date_planned(self, product_qty, start_date):
        days = self.lead_days or 0.0
        if self.lead_type == 'supplier':
            # These days will be substracted when creating the PO
            days += self.product_id._select_seller(
                quantity=product_qty,
                date=fields.Date.to_string(start_date),
                uom_id=self.product_uom).delay or 0.0
        date_planned = start_date + relativedelta.relativedelta(days=days)
        return date_planned.strftime(DEFAULT_SERVER_DATE_FORMAT)

    @api.multi
    def _prepare_procurement_values(self, product_qty, date=False, group=False):
        return {
            'name': self.name,
            'date_planned': date or self._get_date_planned(product_qty, datetime.today()),
            'product_id': self.product_id.id,
            'product_qty': product_qty,
            'company_id': self.company_id.id,
            'product_uom': self.product_uom.id,
            'location_id': self.location_id.id,
            'origin': self.name,
            'warehouse_id': self.warehouse_id.id,
            'orderpoint_id': self.id,
            'group_id': group or self.group_id.id,
        }