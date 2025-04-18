from odoo import models, fields, api, _
from odoo.exceptions import UserError
import re
import requests

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def action_open_whatsapp(self):
        self.ensure_one()
        if not self.mobile:
            raise UserError(_("Número de celular não cadastrado!"))
        
        phone = re.sub(r'\D', '', self.mobile)
        
        if self.description and 'anúncios semelhantes' in self.description.lower():
            message = _("""Olá %s, sou %s. Recebi seu interesse em vários imóveis.
Por favor, envie os links para que eu possa te ajudar melhor.""") % (
                self.partner_name or 'Cliente',
                self.user_id.name or ''
            )
        else:
            message = _("""Olá %s, sou %s. Recebi seu interesse no imóvel: %s
Deseja agendar uma visita?""") % (
                self.partner_name or 'Cliente',
                self.user_id.name or '',
                self.x_studio_link_do_portal or ''
            )

        return {
            'type': 'ir.actions.act_url',
            'url': f"https://wa.me/{phone}?text={requests.utils.quote(message)}",
            'target': 'new',
        }
