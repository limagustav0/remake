# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.tools.translate import _
import base64
from dataclasses import dataclass
from requests import post

class RequisicaoFachada(http.Controller):
    @http.route('/remake', auth='public', type="http", website=True, csrf=False)
    def index(self, **kw):
        users = http.request.env['res.users'].sudo().search([])
        partners = http.request.env['res.partner'].sudo().search([])
        facade_ad_type_ids = http.request.env['kami_sm.attendance.ad_type'].sudo().search([])
        partners = request.env['res.partner'].sudo().search([])
        
        return http.request.render('remake.remake', {
            'partners': partners,
            'users': users,
            'partners': partners,
            'facade_ad_type_ids': facade_ad_type_ids,
        })
    
    @http.route('/remake', type='http', auth='public', website=True, methods=['POST'], csrf=False)
    def create(self, **post):
        facade_type = http.request.env.ref('kami_sm.facade').id
        date = str(post.get('data_vencimento')).replace('/', '-')
        attachment = http.request.params['task_attachment']

        description = f"""
          <strong>Endereço completo do salão:</strong> {post.get('saloon_address')}<br></br>
          <strong>Nome do Vendedor:</strong> {post.get('seller_name')}<br></br>
          <strong>Arte para fachada:</strong> {post.get('img')}<br></br>
          <strong>Tipo de Aplicação:</strong> {post.get('aplicationtypevalue')}<br></br>
          <strong>Tipos de aplicações adicionais:</strong> {post.get('aditionalapp')}<br></br>
          <strong>Regional solicitante RS?:</strong> {post.get('regional_name') if True else "Não"}
        """

        attendance_vals = {
            'client_id': post.get('saloon_name'),
            'backoffice_user_id': post.get('responsible'),
            'type_id': facade_type,
            'images_position': post.get('position'),
            'facade_width': post.get('width_facade').replace(',', '.'),
            'facade_height': post.get('height_facade').replace(',', '.'),
            'magazine_types': post.get('magazinetype'),
            'magazine_format': post.get('magazineformat'),
            'magazine_width': post.get('magazinewidht').replace(',', '.'),
            'magazine_height': post.get('magazineheight').replace(',', '.'),
            'facade_has_ad': post.get('anuncio_checkbox'),
            'facade_ad_type_id': post.get('ad_type'),
            'has_cutting_edge': post.get('sangria'),
            'cutting_edge_size': post.get('mmsangria').replace(',', '.'),
            'has_safe_margin': post.get('margem'),
            'safe_margin_size': post.get('mmmargem').replace(',', '.'),
            'installation_images': base64.b64encode(attachment.read()),
            'description': description
        }
        new_task = request.env['kami_sm.attendance'].sudo().create(attendance_vals)
        if 'aditional_images' in http.request.params:
            attached_files = http.request.httprequest.files.getlist('aditional_images')
            for attachment in attached_files:
                http.request.env['ir.attachment'].sudo().create({
                    'name': "imagens adicionais" + attachment.filename,
                    'datas': base64.b64encode(attachment.read()),
                    'res_model': 'kami_sm.attendance',
                    'res_id': new_task.id,
                })
        return http.request.render('remake.forms_success_page')


class AudioVisualKamico(http.Controller):
    @http.route('/audiovisualkamico', auth='public', csrf=False, website=True)
    def index(self, **kw):
        return http.request.render('remake.audiovisualkamico', {
        })

    @http.route('/audiovisualkamico', auth='public', type="http", website=True, methods=['post'], csrf=False)
    def create(self, **post):

        quadrado = post.get('quadrado')
        vertical = post.get('vertical')
        horizontal = post.get('horizontal')
        ig = post.get('ig')

        youtube = post.get('Youtube')
        facebook = post.get('Facebook')
        instagram = post.get('Instagram')
        whatsapp = post.get('WhatsApp')
        stories = post.get('Stories')
        linkedin = post.get('LinkedIn')
        reels = post.get('Reels')

        quadrado = quadrado if quadrado == 'Quadrado 1:1 (1080x1080)' else ''
        vertical = vertical if vertical == 'Vertical 9:16 (1080x1920)' else ''
        horizontal = horizontal if horizontal == 'Horizontal 16:9 (1920x1080)' else ''
        ig = ig if ig == 'IG 4:5 (1080x1350)' else ''

        youtube = youtube if youtube == 'Youtube' else ''
        facebook = facebook if facebook == 'Facebook' else ''
        instagram = instagram if instagram == 'Instagram' else ''
        whatsapp = whatsapp if whatsapp == 'WhatsApp' else ''
        stories = stories if stories == 'Stories' else ''
        linkedin = linkedin if linkedin == 'LinkedIn' else ''
        reels = reels if reels == 'Reels' else ''

        project_id = request.env.ref('remake.audiovisualkamico').id
        description = f"""
            Seu nome:{post.get('nome')}<br></br>
            Departamento:{post.get('departamento')}<br></br>
            Título da solicitação:{post.get('tituloSolicitacao')}<br></br>
            Demanda:{post.get('demanda')}<br></br>
            Data da captação:{post.get('dataCaptacao')}<br></br>
            Precisa de fotos:{post.get('precisaFoto')}<br></br>
            Resolução:{post.get('resolucao')}<br></br>
            Refere a empresa KAMI:{post.get('referenteKami')}<br></br>
            Proporção do arquivo:{quadrado, vertical, horizontal, ig}<br></br>
            Tempo de vídeo estimado:{post.get('tamanhoVideo')}<br></br>
            Onde deseja compartilhá-la:{youtube, facebook, instagram, whatsapp, stories, linkedin, reels}  -  Quais outros locais:{post.get('outrosLocais')}<br></br>
            Trilha ou referência de trilha:{post.get('trilhaReferencia')}<br></br>
            Lettering/GC:{post.get('lettering')} -- O que?{post.get('oQue')}<br></br>
            Incluir logotipo:{post.get('incluiLogotipo')} -- {post.get('logotipoLocal')}<br></br>
            Animação:{post.get('animacao')}<br></br>
            Referência:{post.get('referencia')}<br></br>
            Detalhes da solicitação:{post.get('detalhesSolicitacao')}<br></br>
            Briefing/Roteiro:{post.get('briefing')}<br></br>
            Prazo de entrega estimado:{post.get('prazoEntrega')}<br></br>
        """
        task_vals = {
            'name': f"{post.get('nome')}-{post.get('departamento')}",
            'project_id': project_id,
            'description': description,
        }

        new_task = request.env["project.task"].sudo().create(task_vals)

        if 'task_attachment' in http.request.params:
            attached_files = http.request.httprequest.files.getlist('task_attachment')
            for attachment in attached_files:
                http.request.env['ir.attachment'].sudo().create({
                    'name': attachment.filename,
                    'datas': base64.b64encode(attachment.read()),
                    'res_model': 'project.task',
                    'res_id': new_task.id,

                })
        return http.request.render('remake.forms_success_page')