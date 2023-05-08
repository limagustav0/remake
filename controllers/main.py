# -*- coding: utf-8 -*-
from odoo import http, api, models
from odoo.http import request
from odoo.tools.translate import _
import base64
from dataclasses import dataclass
from requests import post
from datetime import datetime

class RequisicaoFachada(http.Controller):
    @http.route('/fachada', auth='public', type="http", website=True, csrf=False)
    def index(self, **kw):
        users = http.request.env['res.users'].sudo().search([])
        partners = http.request.env['res.partner'].sudo().search([])
        facade_ad_type_ids = http.request.env['kami_sm.attendance.ad_type'].sudo().search([])
        partners = request.env['res.partner'].sudo().search([])
        
        return http.request.render('kami_form.fachada', {
            'partners': partners,
            'users': users,
            'partners': partners,
            'facade_ad_type_ids': facade_ad_type_ids,
        })
    
    @http.route('/fachada', type='http', auth='public', website=True, methods=['POST'], csrf=False)
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
        return http.request.render('kami_form.forms_success_page')

class Audiovisual(http.Controller):
    @http.route('/audiovisual', auth='public', type="http", website=True, csrf=False)
    def index(self, **kw):
        users = http.request.env['res.users'].sudo().search([])
        partners = http.request.env['res.partner'].sudo().search([])
        
        
        return http.request.render('kami_form.audiovisual', {
            'partners': partners,
            'users': users,
        })
    
    @http.route('/audiovisual', type='http', auth='public', website=True, methods=['POST'], csrf=False)
    def create(self, **post):
        
        prazo_entrega = datetime.strptime(post.get('prazo_data'), '%Y-%m-%dT%H:%M')
        prazo_entrega_estimado = prazo_entrega.strftime('%d/%m/%Y - %H:%M')

        partner = http.request.env['res.partner'].browse(
            int(post.get("partner_name"))
        )

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

        project_id = request.env.ref('kami_form.audiovisual_kamico').id
        description = f"""
            <strong>Seu nome: </strong>{partner.name}<br></br>
            <strong>Departamento: </strong>{post.get('department')}<br></br>
            <strong>Título da solicitação: </strong>{post.get('title_solicitation')}<br></br>
            <strong>Demanda:</strong>{post.get('demand')}<br></br>
            <strong>Data da captação: </strong>{post.get('captation_date') if post.get('captation_date') else post.get('captation_date_edition')}<br></br>
            <strong>Precisa de fotos: </strong>{post.get('need_photo')}<br></br>
            <strong>Resolução: </strong>{post.get('resolution')}<br></br>
            <strong>Refere a empresa KAMI: </strong>{post.get('kami_company')}<br></br>
            <strong>Proporção do arquivo: </strong>{post.get('file_proportion1') if post.get('file_proportion1') else ""}   {post.get('file_proportion2') if post.get('file_proportion2') else ""}   {post.get('file_proportion3') if post.get('file_proportion3') else ""}   {post.get('file_proportion3') if post.get('file_proportion3') else ""}   {post.get('file_proportion4') if post.get('file_proportion4') else ""}<br></br>
            <strong>Tempo de vídeo estimado: </strong>{post.get('time_video')}<br></br>
            <strong>Onde deseja compartilhá-la: </strong>{post.get('share1') if post.get('share1') else ""}   {post.get('share2') if post.get('share2') else ""}   {post.get('share3') if post.get('share3') else ""}   {post.get('share4') if post.get('share4') else ""}   {post.get('share5') if post.get('share5') else ""}   {post.get('share6') if post.get('share6') else ""}   {post.get('share7') if post.get('share7') else ""}   {post.get('share8') if post.get('share8') else ""}<br></br>
            <strong>Trilha ou referência de trilha: </strong>{post.get('trilha')}<br></br>
            <strong>Lettering/GC: </strong>{post.get('Lettering')}  <strong>{post.get('Letteringtext') if post.get('Letteringtext') else ""}</strong><br></br>
            <strong>Incluir logotipo: </strong>{post.get('logotipo')}  <strong>{post.get('logo_radio') if post.get('logo_radio') else ""}</strong><br></br>
            <strong>Animação: </strong>{post.get('animation')}  <strong>{post.get('reference') if post.get('reference') else ""}</strong><br></br>
            <strong>Detalhes da solicitação: </strong>{post.get('solicitation_detail')}<br></br>
            <strong>Briefing/Roteiro: </strong>{post.get('briefing')}<br></br>
            <strong>Prazo de entrega estimado: </strong>{prazo_entrega_estimado}<br></br>
        """
        task_vals = {
            'name': f"{post.get('title_solicitation')}-{post.get('department')}",
            'project_id': project_id,
            'description': description,
        }

        new_task = request.env["helpdesk_mgmt.ticket"].sudo().create(task_vals)

        if 'attachment' in http.request.params:
            attached_files = http.request.httprequest.files.getlist('attachment')
            for attachment in attached_files:
                http.request.env['ir.attachment'].sudo().create({
                    'name': attachment.filename,
                    'datas': base64.b64encode(attachment.read()),
                    'res_model': 'project.task',
                    'res_id': new_task.id,

                })
        return http.request.render('kami_form.forms_success_page')
    
class HelpdeskTicket(http.Controller):
    @http.route('/helpdeskticket', auth='public', csrf=False, website=True)
    def index(self, **kw):
        types = http.request.env['helpdesk.ticket.type']
        categories = http.request.env['helpdesk.ticket.category']
        priorities = {
            0: _('Baixa'),
            1: _('Média'),
            2: _('Alta'),
            3: _('Urgente')
        }
        return http.request.render('kami_form.helpdesk_ticket', {
            'types': types.sudo().search([]),
            'categories': categories.sudo().search([]),
            'priorities': priorities
        })

    @http.route('/helpdeskticket', auth='public', type="http", website=True, methods=['post'], csrf=False)
    def create(self, **post):
        ticket_vals = {
            'name': f"{post.get('subject')}",
            'type_id': int(post.get('type')),
            'category_id': int(post.get('category')),
            'description': post.get('description'),
            'priority': post.get('priority')
        }

        new_ticket = http.request.env["helpdesk.ticket"].sudo().create(
            ticket_vals)
        if 'attachment' in http.request.params:
            attached_files = http.request.httprequest.files.getlist(
                'attachment')
            for attachment in attached_files:
                http.request.env['ir.attachment'].sudo().create({
                    'name': attachment.filename,
                    'datas': base64.b64encode(attachment.read()),
                    'res_model': 'helpdesk.ticket',
                    'res_id': new_ticket.id,
                })
        return http.request.render('kami_form.forms_success_page')
    
class PlanejamentoCampanhaMarketing(http.Controller): 
    @http.route('/planejamentocampanhamarketing', auth='public', type="http", website=True, csrf=False)
    def index(self, **kw):
        return http.request.render('kami_form.planejamentocampanhamarketing', {
        })

    @http.route('/planejamentocampanhamarketing', type='http', auth='public', website=True, methods=['POST'], csrf=False)
    def create(self, **post):
        project_id = request.env.ref('kami_form.digital_invite_project').id
        description = f"""
            Nome da campanha:{post.get('nomeCampanha')}<br></br>
            Tipos de Campanha:{post.get('tipoCampanha')}<br></br>
            Ano:{post.get('ano')}<br></br>
            Briefing da campanha:{post.get('briefing')}<br></br>
            periodo:{post.get('periodo')}<br></br>
            Vencimento do Planejamento:{post.get('dataVencimento')}<br></br>
        """
        new_task = {
            'name': f"{post.get('nomeCampanha')}-{post.get('tipoCampanha')}-{post.get('ano')}",
            'project_id': project_id,
            'description': description,
        }
        http.request.env["project.task"].sudo().create(new_task)
        return http.request.render('kami_form.forms_success_page', {})

class ControleRomaneio(http.Controller): 
    @http.route('/romaneio', auth='public', type="http", website=True, csrf=False)
    def index(self, **kw):
        companyes = http.request.env['res.company'].sudo().search([])

        
        return http.request.render('kami_form.romaneio', {
            'companyes' : companyes,
        })
    
    @http.route('/romaneio', type='http', auth='public', website=True, methods=['POST'], csrf=False)
    def create(self, **post):
        project_id = request.env.ref('kami_form.financeiro_team').id

        type_id = request.env.ref('kami_form.financeiro_type_romaneio').id

        company = http.request.env["res.company"].browse(
            int(post.get("company_name"))
        )

        description = f"""
            <strong>Empresa: </strong>{company.name}<br><br/>
            <strong>Número do Romaneio: </strong>{post.get('number_romaneio')}<br><br/>
            <strong>Data de Saída: </strong>{post.get('exit_date')}<br><br/>

        """
        new_task = {
            'name': "Romaneio " + company.name,
            'team_id' : project_id,
            'type_id' : type_id,
            'description': description,
        }
        http.request.env["helpdesk.ticket"].sudo().create(new_task)
        return http.request.render('kami_form.forms_success_page', {})
    
class GerenciamentoInvasaoTruss(http.Controller): 
    @http.route('/invasaotruss', auth='public', type="http", website=True, csrf=False)
    def index(self, **kw):

        return http.request.render('kami_form.invasaotruss', {

        })
    
    @http.route('/invasaotruss', type='http', auth='public', website=True, methods=['POST'], csrf=False)
    def create(self, **post):
        project_id = request.env.ref('kami_form.invasao_truss').id

        data_recebimento = datetime.strptime(post.get('dataRecebimento'), '%Y-%m-%dT%H:%M')
        data_recebimento_formatada = data_recebimento.strftime('%d/%m/%Y - %H:%M')

        description = f"""
            <strong>Tipo Notificação:</strong> {post.get('region_invasion') if post.get('region_invasion') else " "}     {post.get('invalid_sell') if post.get('invalid_sell') else " "}<br><br/>
            <strong>Data de Recebimento:</strong> {data_recebimento_formatada}<br><br/>
            <strong>Empresa Notificada:</strong> {post.get('Movement') if post.get('Movement') else " "}     {post.get('NewHauss') if post.get('NewHauss') else " "}     {post.get('RiodeJaneiro') if post.get('RiodeJaneiro') else " "}<br><br/>
            <strong>Prazo de Resposta:</strong> {post.get('Prazo')}<br><br/>
            <strong>Número OCTADESK:</strong> {post.get('octadesk_number')}<br><br/>
            <strong>Local onde o produto foi encontrado:</strong> {post.get('found_location')}<br><br/>
            <strong>Nome do Cliente:</strong> {post.get('client_name')}<br><br/>
            <strong>Prioridade:</strong> {post.get('priority')}<br><br/>
        """
        new_task = {
            'name': f"Notificações TRUSS - {post.get('priority')} PRIORIDADE",
            'project_id': project_id,
            'description': description,
        }
        new_task = http.request.env["project.task"].sudo().create(new_task)
        if 'aditional_archives' in http.request.params:
            attached_files = http.request.httprequest.files.getlist('aditional_archives')
            for attachment in attached_files:
                http.request.env['ir.attachment'].sudo().create({
                    'name': attachment.filename,
                    'datas': base64.b64encode(attachment.read()),
                    'res_model': 'project.task',
                    'res_id': new_task.id,
                })
        return http.request.render('kami_form.forms_success_page')

class CriativoKamico(http.Controller): 
    @http.route('/criativo', auth='public', type="http", website=True, csrf=False)
    def index(self, **kw):
        return http.request.render('kami_form.criativo')
    
    @http.route('/criativo', type='http', auth='public', website=True, methods=['POST'], csrf=False)
    def create(self, **post):
        project_id = request.env.ref('kami_form.criativo_kami').id


        data_prazo = datetime.strptime(post.get('data_prazo'), '%Y-%m-%dT%H:%M')
        data_prazo_formatada = data_prazo.strftime('%d/%m/%Y - %H:%M')


        description = f"""
            <strong>Título da solicitação:</strong> {post.get('notification_title')}<br/><br/>
            <strong>Essa solicitação se refere a qual empresa KAMI?:</strong> {post.get('solicitation')}<br/><br/>

            <strong>Tipo da solicitação:</strong> {post.get('notification_type')}<br/><br/>

            <strong>Onde deseja compartilhá-la?:</strong> {post.get('Email') if post.get('Email') else " "}<br/>
                                 {post.get('Mídiassociais') if post.get('Mídiassociais') else " "}<br/>
                                 {post.get('Youtube') if post.get('Youtube') else " "}<br/>
                                 {post.get('WhatsApp') if post.get('WhatsApp') else " "}<br/>
                                 {post.get('Stories') if post.get('Stories') else " "}<br/>
                                 {post.get('Materialimpresso') if post.get('Materialimpresso') else " "}<br/>
                                 {post.get('Workplace') if post.get('Workplace') else " "}<br/>
                                 {post.get('LinkedIn') if post.get('LinkedIn') else " "}<br/>
                                 {post.get('Outroslocais') if post.get('Outroslocais') else " "}<br/><br/><br/>

            <strong>Inserir Logotipo:</strong> {post.get('KAMICO') if post.get('KAMICO') else ""}<br/>
                              {post.get('SBMP') if post.get('SBMP') else ""}<br/>
                              {post.get('TRUSSHair') if post.get('TRUSSHair') else ""}<br/>
                              {post.get('HairSPA') if post.get('HairSPA') else ""}<br/>
                              {post.get('HairPro') if post.get('HairPro') else ""}<br/>
                              {post.get('LogodoCliente') if post.get('LogodoCliente') else ""}<br/>
                              {post.get('Outros') if post.get('Outros') else ""}<br/>
                              {post.get('SemLogo') if post.get('SemLogo') else ""}<br/><br/><br/>
            
            
            <strong>Detalhes da solicitação:</strong> {post.get('solicitation_detail')}<br/><br/><br/>

            <strong>Prazo de entrega estimado:</strong> {data_prazo_formatada}<br/><br/><br/>

            <strong>Seu nome:</strong> {post.get('yourname')}<br/><br/><br/>

            <strong>Seu e-mail:</strong> {post.get('yourmail')}<br/><br/><br/>

            <strong>Whatsapp:</strong> {post.get('celular')}<br/><br/><br/>

            <strong>Por onde você deseja receber o arquivo final?:</strong> {post.get('email')} {post.get('whatsapp')}<br/><br/><br/>
        """
        new_task = {
            'name': f"Criativo - {post.get('solicitation')}",
            'project_id': project_id,
            'description': description,
        }
        new_task = http.request.env["project.task"].sudo().create(new_task)
        if 'aditional_archives' in http.request.params:
            attached_files = http.request.httprequest.files.getlist('aditional_archives')
            for attachment in attached_files:
                http.request.env['ir.attachment'].sudo().create({
                    'name': attachment.filename,
                    'datas': base64.b64encode(attachment.read()),
                    'res_model': 'project.task',
                    'res_id': new_task.id,
                })
        return http.request.render('kami_form.forms_success_page')

class LancamentoEducacionalMvp(http.Controller):
    @http.route('/educacionalmvp', auth='public', csrf=False, website=True)    
    def index(self, **kw):
        users = http.request.env['res.users']
        return http.request.render('kami_form.educacionalmvp', {
            'users': users.search([])
        })

    @http.route('/educacionalmvp', auth='public', type="http", website=True, methods=['post'], csrf=False)
    def create(self, **post):
        project_id = request.env.ref('kami_form.lancamento_educacional_mvp').id
        description = f"""
                <strong>Atividade:</strong> {post.get('atividade')}<br></br>
                <strong>Descrição da atividade:</strong> {post.get('descricaoAtividade')}<br></br>
                <strong>Data preferida para entrega:</strong> {post.get('dataEntrega')}<br></br>
                <strong>Prioridade:</strong> {post.get('priority')}<br></br>
                <strong>Responsável pela atividade:</strong> {post.get('responsavel')}<br></br>
        """
        new_task = {
            'name': f"{post.get('atividade')}-{post.get('responsavel')}-{post.get('priority')}",
            'project_id': project_id,
            'description': description,
        }

        new_task = http.request.env["project.task"].sudo().create(new_task)
        if 'anexo' in http.request.params:
            attached_files = http.request.httprequest.files.getlist('anexo')
            for attachment in attached_files:
                http.request.env['ir.attachment'].sudo().create({
                    'name': attachment.filename,
                    'datas': base64.b64encode(attachment.read()),
                    'res_model': 'project.task',
                    'res_id': new_task.id,
                })
        return http.request.render('kami_form.forms_success_page')
    
class PromotoriaFreelancer(http.Controller):
    @http.route('/promotoriafreelancer', auth='public', csrf=False, website=True)    
    def index(self, **kw):
        partners = http.request.env['res.partner'].sudo().search([])
        users = http.request.env['res.users'].sudo().search([])
        return http.request.render('kami_form.promotoriafreelancer', {
            'partners' : partners,
            'users' : users,
        })

    # @http.route('/promotoriafreelancer', auth='public', type="http", website=True, methods=['post'], csrf=False)
    # def create(self, **post):
    #     #project_id = request.env.ref('kami_form.digital_invite_project').id
    #     description = f"""
    #             Nome do vendedor:{post.get('nomeVendedor')}<br></br>
    #             Email do vendedor:{post.get('emailVendedor')}<br></br>
    #             Nome da Loja:{post.get('nomeLoja')}<br></br>
    #             Código do cliente:{post.get('codCliente')}<br></br>
    #             Data da atividade:{post.get('dataAtividade')}<br></br>
    #             Horário do Evento:{post.get('horarioEvento')}<br></br>
    #             Endereço completo da Loja:{post.get('enderecoLoja')}<br></br>
    #             Tipo de atendimento:{post.get('tipoAtendimento')}<br></br>
    #             Observações do cliente:{post.get('observacoesImportantes')}<br></br>
    #     """
    #     new_task = {
    #         'name': f"{post.get('nomeVendedor')}-{post.get('nomeLoja')}-{post.get('codCliente')}",
    #         'description': description,
    #     }
    #     http.request.env["project.task"].sudo().create(new_task)
    #     return http.request.render('kami_forms.forms_success_page', {})

class CampanhaMKT(http.Controller):
    @http.route('/campanhamkt', auth='public', csrf=False, website=True)    
    def index(self, **kw):
        return http.request.render('kami_form.campanhamkt')
    
    @http.route('/campanhamkt', auth='public', type="http", website=True, methods=['post'], csrf=False)
    def create(self, **post):
        project_id = request.env.ref('kami_form.campanhas_mkt').id

        data_inicio = datetime.strptime(post.get('data_inicio'), '%Y-%m-%dT%H:%M')
        data_inicio_formatada = data_inicio.strftime('%d/%m/%Y - %H:%M')

        data_vencimento = datetime.strptime(post.get('data_vencimento'), '%Y-%m-%dT%H:%M')
        data_vencimento_formatada = data_vencimento.strftime('%d/%m/%Y - %H:%M')

        description = f"""
                <strong>Empresa:</strong> {post.get('empresa')}<br></br>
                <strong>Ano:</strong> {post.get('ano')}<br></br>
                <strong>Periodo:</strong> {post.get('trimestre')}<br></br>
                <strong>Início:</strong> {data_inicio_formatada}<br></br>
                <strong>Vencimento do Planejamento:</strong> {data_vencimento_formatada}<br></br>
                <strong>Tipos de Campanha:</strong><br></br>
                                   {post.get('lancamento') if post.get('lancamento') else " "}<br></br>
                                   {post.get('branding') if post.get('branding') else " "}<br></br>
                                   {post.get('comercial') if post.get('comercial') else " "}<br></br>
                                   {post.get('fluxo') if post.get('fluxo') else " "}<br></br>
                                   {post.get('encantamento') if post.get('encantamento') else " "}<br></br>
                                   {post.get('reativacao') if post.get('reativacao') else " "}<br></br>

        """
        new_task = {
            'name': f"Campannha - {post.get('empresa')} - {post.get('ano')}",
            'project_id': project_id,
            'description': description,
        }

        new_task = http.request.env["project.task"].sudo().create(new_task)
        return http.request.render('kami_form.forms_success_page')
    
class SolicitacaoRedeSocial(http.Controller):
    @http.route('/solicitacaoredesocial', auth='public', csrf=False, website=True)    
    def index(self, **kw):
        return http.request.render('kami_form.solicitacaoredesocial')
    
    @http.route('/solicitacaoredesocial', auth='public', type="http", website=True, methods=['post'], csrf=False)
    def create(self, **post):
        project_id = request.env.ref('kami_form.solicitacao_redes_sociais').id
        description = f"""
                <strong>Assunto:</strong> {post.get('subject')}<br></br>
                <strong>Onde será publicado?:</strong> {post.get('publi')}<br></br>
                <strong>Briefing:</strong> {post.get('briefing')}<br></br>
                <strong>Legenda:</strong> {post.get('legenda')}<br></br>
                <strong>Data da Publicação:</strong> {post.get('pud_date')}<br></br>
        """
        new_task = {
            'name': f"Social Mídia - {post.get('subject')} - {post.get('publi')}",
            'project_id': project_id,
            'description': description,
        }

        new_task = http.request.env["project.task"].sudo().create(new_task)
        if 'aditional_archives_reference' in http.request.params:
            attached_files = http.request.httprequest.files.getlist('aditional_archives_reference')
            for attachment in attached_files:
                http.request.env['ir.attachment'].sudo().create({
                    'name': "REFERÊNCIAS" + attachment.filename,
                    'datas': base64.b64encode(attachment.read()),
                    'res_model': 'project.task', 
                    'res_id': new_task.id,
                })

        if 'aditional_archives_layout' in http.request.params:
            attached_files = http.request.httprequest.files.getlist('aditional_archives_layout')
            for attachment in attached_files:
                http.request.env['ir.attachment'].sudo().create({
                    'name': "LAYOUT" + attachment.filename,
                    'datas': base64.b64encode(attachment.read()),
                    'res_model': 'project.task', 
                    'res_id': new_task.id,
                })

        if 'aditional_archives_story' in http.request.params:
            attached_files = http.request.httprequest.files.getlist('aditional_archives_story')
            for attachment in attached_files:
                http.request.env['ir.attachment'].sudo().create({
                    'name': "STORY" + attachment.filename,
                    'datas': base64.b64encode(attachment.read()),
                    'res_model': 'project.task',  
                    'res_id': new_task.id,
                })
        return http.request.render('kami_form.forms_success_page')

class CursosKamico(http.Controller):
    @http.route('/cursoskamico', auth='public', csrf=False, website='True')
    def index(self, **kw): 
         return http.request.render('kami_form.cursoskamico', {
         })

    @http.route('/cursoskamico', auth='public', type="http", website=True, methods=['post'], csrf=False)
    def create(self, **post):
        project_id = request.env.ref('kami_form.cursos_kamico_project').id
        description = f"""
            Nome do Vendedor:{post.get('nomeVendedor')}<br></br>
            Nome completo do Aluno:{post.get('nomeAluno')}<br></br>
            WhatsApp do Aluno:{post.get('whatsappAluno')}<br></br>
            Email do Aluno:{post.get('emallAluno')}<br></br>
            Classificação do aluno:{post.get('classificacaoAluno')}<br></br>
            Nome do salão que o aluno trabalha:{post.get('salaoAluno')}<br></br>
            Região do salão:{post.get('regiaoSalao')}<br></br>
            Código do cliente no UNO:{post.get('codClientUno')}<br></br>
            Código do pedido do cliente no UNO:{post.get('codPedidoUno')}<br></br>
            Forma de pagamento:{post.get('formaPagamento')}<br></br>
            Referente ao curso:{post.get('cursoReferencia')}<br></br>
            Observações:{post.get('observacao')}<br></br>
        
        """
        task_vals = {
            'name': f"{post.get('nomeVendedor')}-{post.get('nomeAluno')}",
            'project_id': project_id,
            'description': description,
        }

        new_task = request.env["project.task"].sudo().create(task_vals)

        if 'task_attachment'  in http.request.params:
            attached_files = http.request.httprequest.files.getlist('task_attachment')
            for attachment in attached_files:
                http.request.env['ir.attachment'].sudo().create({
                    'name': attachment.filename,
                    'datas': base64.b64encode(attachment.read()),
                    'res_model': 'project.task',
                    'res_id': new_task.id,

                })
        return http.request.render('kami_form.forms_success_page')
    
class FormularioRH(http.Controller):
    @http.route('/formulariorh', auth='public', csrf=False, website=True)    
    def index(self, **kw):
        return http.request.render('kami_form.formulariorh')

    @http.route('/formulariorh', auth='public', type="http", website=True, methods=['post'], csrf=False)
    def create(self, **post):

        prestacao_serv = datetime.strptime(post.get('prestacaoServicoInicio'), '%Y-%m-%dT%H:%M')
        prestacao_serv_formatado = prestacao_servo.strftime('%d/%m/%Y - %H:%M')

        prestacao_serv = datetime.strptime(post.get('prestacaoServicoFim'), '%Y-%m-%dT%H:%M')
        prestacao_serv_fim = prestacao_serv.strftime('%d/%m/%Y - %H:%M')

        data_expedicao = datetime.strptime(post.get('dataExpedicao'), '%Y-%m-%dT%H:%M')
        data_expedicao_formatado = predata_expedicaostacao_serv.strftime('%d/%m/%Y - %H:%M')

        data_nascimento = datetime.strptime(post.get('dataNascimento'), '%Y-%m-%dT%H:%M')
        data_nascimento_formatado = data_nascimento.strftime('%d/%m/%Y - %H:%M')

        project_id = request.env.ref('kami_form.solicitacao_rh_project').id
        description = f"""
                <strong>NOME COMPLETO:</strong> {post.get('nomeCompleto')}<br></br>
                <strong>NOME SOCIAL:</strong> {post.get('nomeSocial')}<br></br>
                <strong>CNPJ:</strong> {post.get('cnpj')}<br></br>
                <strong>NOME PAI:</strong> {post.get('nomePai')}<br></br>
                <strong>NOME MÃE:</strong> {post.get('nomeMae')}<br></br>
                <strong>DATA NASCIMENTO:</strong> {post.get('dataNascimento')}<br></br>
                <strong>MUNICIPIO DE NASCIMENTO:</strong> {post.get('municipioNascimeno')}<br></br>
                <strong>UF:</strong> {post.get('uf')}<br></br>
                <strong>PAÍS DE NASCIMENTO:</strong> {post.get('paisNascimento')}<br></br>
                <strong>GÊNERO:</strong> {post.get('genero')}<br></br>
                <strong>ESTADO CIVIL:</strong> {post.get('estadoCivil')}<br></br>
                <strong>ENDEREÇO RESIDENCIAL:</strong> {post.get('enderecoResidencial')}<br></br>
                <strong>BAIRRO:</strong> {post.get('bairro')}<br></br>
                <strong>CEP:</strong> {post.get('cep')}<br></br>
                <strong>ESTADO:</strong> {post.get('estado')}<br></br>
                <strong>EMAIL PESSOAL:</strong> {post.get('emailPessoal')}<br></br>
                <strong>TAMANHO DA ROUPA:</strong> {post.get('tamanhoRoupa')}<br></br>
                <strong>TAMANHO DO SAPATO:</strong> {post.get('tamanhoSapato')}<br></br>
                <strong>BANCO:</strong> {post.get('banco')}<br></br>
                <strong>AGÊNCIA:</strong> {post.get('agencia')}<br></br>
                <strong>NÚMERO DA CONTA:</strong> {post.get('numeroConta')}<br></br>
                <strong>TIPO DE CONTA:</strong> {post.get('tipoConta')}<br></br>
                <strong>PIX:</strong> {post.get('pix')}<br></br>
                <strong>NÚMERO DO RG:</strong> {post.get('numeroRg')}<br></br>
                <strong>ORGÃO EMISSOR:</strong> {post.get('orgaoEmissor')}<br></br>
                <strong>DATA DA EXPEDIÇÃO:</strong> {post.get(data_expedicao_formatado)}<br></br>
                <strong>NUMERO DO CPF:</strong> {post.get('numeroCpf')}<br></br>
                <strong>PERIODO DA PRESTAÇÃO DE SERVIÇO (DATA INICIO):</strong> {post.get(prestacao_serv_formatado)}<br></br>
                <strong>PERIODO DA PRESTAÇÃO DE SERVIÇO (DATA FINAL):</strong> {post.get(prestacao_serv_fim)}<br></br>
                <strong>FUNÇÃO:</strong> {post.get('funcao')}<br></br>
                <strong>VALOR DO PAGAMENTO:</strong> {post.get('valorPagamento')}<br></br>
                <strong>AJUDA DE CUSTO:</strong> {post.get('ajudaCusto')}<br></br>
                <strong>OUTROS:</strong> {post.get('outros')}<br></br>
        """
        task_vals = {
            'name': f"{post.get('nomeCompleto')}-{post.get('funcao')}",
            'project_id': project_id,
            'description': description,
        }
        new_task = request.env["project.task"].sudo().create(task_vals)
        if 'anexo'  in http.request.params:
            attached_files = http.request.httprequest.files.getlist('anexo')
            for attachment in attached_files:
                http.request.env['ir.attachment'].sudo().create({
                    'name': attachment.filename,
                    'datas': base64.b64encode(attachment.read()),
                    'res_model': 'project.task',
                    'res_id': new_task.id,
                })
        return http.request.render('kami_form.forms_success_page')
    
class EducacionalContent(http.Controller):
    @http.route('/educacionalcontent', auth='public', csrf=False, website='True')
    def index(self, **kw):
        return http.request.render('kami_form.educacionalcontent', {
        })

    @http.route('/educacionalcontent', auth='public', type="http", website=True, methods=['post'], csrf=False)
    def create(self, **post):
        project_id = request.env.ref("kami_form.educacional_content_project").id
        description = f"""
                Capa (HEADLINE):{post.get('capaHeadline')}<br></br>
                Onde será publicado:{post.get('pulicacao')}<br></br>
                Formato:{post.get('formato')}<br></br>
                Selo:{post.get('selo')}<br></br>
                Referências:{post.get('referencia')}<br></br>
                Briefing Tema:{post.get('briefingTema')}<br></br>
                Legenda:{post.get('legenda')}<br></br>
                Briefing do Criativo:{post.get('briefingCriativo')}<br></br>
                Data da Publicação:{post.get('dataPublicacao')}<br></br>
        """
        task_vals = {
            'name': f"{post.get('capaHeadline')}-{post.get('pulicacao')}",
            'project_id': project_id,
            'description': description,
        }

        new_task = request.env["project.task"].sudo().create(task_vals)

        if 'task_attachment_referencias'  in http.request.params:
            attached_files = http.request.httprequest.files.getlist('task_attachment_referencias')
            for attachment in attached_files:
                http.request.env['ir.attachment'].sudo().create({
                    'name': "REFERENCIAS" + attachment.filename,
                    'datas': base64.b64encode(attachment.read()),
                    'res_model': 'project.task',
                    'res_id': new_task.id,
                })
        if 'task_attachment_layout'  in http.request.params:
            attached_files = http.request.httprequest.files.getlist('task_attachment_layout')
            for attachment in attached_files:
                http.request.env['ir.attachment'].sudo().create({
                    'name': "LAYOUT" + attachment.filename,
                    'datas': base64.b64encode(attachment.read()),
                    'res_model': 'project.task',
                    'res_id': new_task.id,
                })
        
        if 'story_task_attachment'  in http.request.params:
            attached_files = http.request.httprequest.files.getlist('story_task_attachment')
            for attachment in attached_files:
                http.request.env['ir.attachment'].sudo().create({
                    'name': "STORY" + attachment.filename,
                    'datas': base64.b64encode(attachment.read()),
                    'res_model': 'project.task',
                    'res_id': new_task.id,
                })
        return http.request.render('kami_form.forms_success_page')
  
class NovoProduto(http.Controller): 
    @http.route('/novoproduto', auth='public', type="http", website=True, csrf=False)
    def index(self, **kw):
        users = http.request.env['res.users'].sudo().search([])
        return http.request.render('kami_form.novoproduto', {
            'users': users,
        })
    
    @http.route('/novoproduto', type='http', auth='public', website=True, methods=['POST'], csrf=False)
    def create(self, **post):

        project_id = request.env.ref("kami_form.backoffice_team").id

        type_id = request.env.ref("kami_form.backoffice_novoproduto").id

        description = f"""
            <strong>*Qual o tipo de cadastro?:</strong> {post.get('c_type')}<br><br/>
            <strong>*Estoque colocado no sistema?:</strong> {post.get('estoque')}<br><br/>
            <strong>*cod produto fabricante: </strong> {post.get('cod_produto')}<br><br/>
            <strong>*descricao comercial: </strong> {post.get('desc_comercial')}<br><br/>
            <strong>*codigo do fabricante no sistema: </strong> {post.get('cod_fabricante')}<br><br/>
            <strong>*nome do fabricante: </strong> {post.get('nome_fabricante')}<br><br/>
            <strong>*grupo de produto: </strong> {post.get('grupo_prod')}<br><br/>
            <strong>codigo ean: </strong> {post.get('ean')}<br><br/>
            <strong>marca: </strong> {post.get('marca')}<br><br/>
            <strong>tipo: </strong> {post.get('tipo')}<br><br/>
            <strong>*profissional: </strong> {post.get('profissional')}<br><br/>
            <strong>*ncm: </strong> {post.get('ncm')}<br><br/>
            <strong>custo: </strong> {post.get('custo')}<br><br/>
            <strong>tabela de preço: </strong> {post.get('price_table')}<br><br/>
            <strong>valor de venda: </strong> {post.get('sell_price')}<br><br/>
            <strong>empresa de cadastro: </strong> {post.get('sell_price')}<br><br/>
        """
        new_task = {
            'name': post.get('marca')+'-'+post.get('marca'),
            'team_id' : project_id,
            'type_id' : type_id,
            'description': description,
        }
        http.request.env["helpdesk.ticket"].sudo().create(new_task)
        return http.request.render('kami_form.forms_success_page', {})

class TradeMarketing(http.Controller):
    @http.route('/trademarketing', auth='public', type="http", website=True, csrf=False)
    def index(self, **kw):
        users = http.request.env['res.users'].sudo().search([])
        partners = http.request.env['res.partner'].sudo().search([])

        
        return http.request.render('kami_form.trademarketing', {
            'partners': partners,
            'users': users,
        })

class HelpDesk(http.Controller): 
    @http.route('/abrirchamado', auth='public', type="http", website=True, csrf=False)
    def index(self, **kw):
        types = request.env["helpdesk.ticket.type"].sudo().search([])
        tags = request.env["helpdesk.ticket.tag"].sudo().search([])
        categories = request.env["helpdesk.ticket.category"].sudo().search(
             [("active", "=", True)]
        )
        users = http.request.env['res.users'].sudo().search([])
        return http.request.render('kami_form.kamihelpdesk', {
            'categories': categories,
            'users': users,
            'types': types,
            'tags': tags,
        })
    
    @http.route('/abrirchamado', type='http', auth='public', website=True, methods=['POST'], csrf=False)
    def create(self, **post):
        
        if post.get("rh_categories") and post.get("types") == "3":
            category = http.request.env["helpdesk.ticket.category"].browse(
                int(post.get("rh_categories"))
            )

        elif post.get("ti_categories") and post.get("types") == "2":
            category = http.request.env["helpdesk.ticket.category"].browse(
                int(post.get("ti_categories"))
            )

        elif post.get("tp") and post.get("types") == "1":
            category = http.request.env["helpdesk.ticket.category"].browse(
                int(post.get("tp"))
            )

        user = http.request.env['res.users'].browse(
            int(post.get("responsible"))
        )

        type = request.env["helpdesk.ticket.type"].browse(
            int(post.get("types"))
        )

        description = f"""
            <strong>SLA: </strong> : {post.get('priority') if post.get('priority1') == "Não" else post.get('priority1') }<br/>
            {post.get('description')}<br/>
        """
        
        vals = {
            "name": post.get('subject'),
            "type_id" : type.id,
            "user_id" : user.id,
            "category_id": category.id,
            "company_id": category.company_id.id or user.company_id.id,
            "description": description,
            "channel_id": request.env["helpdesk.ticket.channel"]
            .sudo()
            .search([("name", "=", "Web")])
            .id,
            "partner_id": request.env.user.partner_id.id,
            "partner_name": request.env.user.partner_id.name,
            "partner_email": request.env.user.partner_id.email,
        }
        new_ticket = request.env["helpdesk.ticket"].sudo().create(vals)
        if 'attachment' in http.request.params:
            for c_file in request.httprequest.files.getlist("attachment"):
                data = c_file.read()
                if c_file.filename:
                    request.env["ir.attachment"].sudo().create(
                        {
                            "name": c_file.filename,
                            "datas": base64.b64encode(data),
                            "res_model": "helpdesk.ticket",
                            "res_id": new_ticket.id,
                        }
                    )
        elif 'o_attachment' in http.request.params:
            for c_file in request.httprequest.files.getlist("o_attachment"):
                data = c_file.read()
                if c_file.filename:
                    request.env["ir.attachment"].sudo().create(
                        {
                            "name": c_file.filename,
                            "datas": base64.b64encode(data),
                            "res_model": "helpdesk.ticket",
                            "res_id": new_ticket.id,
                        }
                    )
        
        return http.request.render('kami_form.forms_success_page')
    
class MalaTecnica(http.Controller):
    @http.route('/malatecnica', auth='public', csrf=False, website=True)    
    def index(self, **kw):
        users = http.request.env['res.users']
        return http.request.render('kami_form.mala_tecnica', {
            'users': users.sudo().search([]),
        })

    @http.route('/malatecnica', auth='public', type="http", website=True, methods=['post'], csrf=False)
    def create(self, **post):

        user = http.request.env['res.users'].browse(
            int(post.get("responsible"))
        )

        team_id = request.env.ref('kami_form.backoffice_team').id

        type_id = request.env.ref('kami_form.backoffice_type_malatecnica').id
        description = f"""
                <strong>Departamento:</strong> {post.get('backoffice')} <br></br>
                <strong>Solicitação:</strong> {post.get('mala')} <br></br>
                <strong>Responsavel:</strong> {user.name} <br></br>
                <strong>Observações / Solicitação:</strong> {post.get('comments')}
        """
        new_task = {

            "name": post.get('subject'),
            #"user_id" : user.id,
            'type_id' : type_id,
            'team_id' : team_id,
            'name': f"{post.get('backoffice')}-{post.get('mala')}",
            'user_id': int(post.get('responsible')),
            'description': description,
        }
        request.env["helpdesk.ticket"].sudo().create(new_task)
        return http.request.render('kami_form.forms_success_page', {})
    


class Dossie(http.Controller):
    @http.route('/dossie', auth='public', csrf=False, website=True)    
    def index(self, **kw):
        users = http.request.env['res.users']
        partners = request.env['res.partner'].sudo().search([])
        return http.request.render('kami_form.dossie', {
            'users': users.sudo().search([]),
            'partners' : partners,
        })

    # @http.route('/dossie', auth='public', type="http", website=True, methods=['post'], csrf=False)
    # def create(self, **post):
    #     #finalizar

class KamiSM(http.Controller):
    @http.route('/kamism', auth='public', csrf=False, website=True)    
    def index(self, **kw):
        users = http.request.env['res.users']
        partners = request.env['res.partner'].sudo().search([])
        att_types = request.env['kami_sm.attendance.type'].sudo().search([])
        att_themes = request.env['kami_sm.attendance.theme'].sudo().search([])
        return http.request.render('kami_form.kamism', {
            'users': users.sudo().search([]),
            'partners' : partners,
            'att_types' : att_types,
            'att_themes' : att_themes,
        })

    @http.route('/kamism', auth='public', type="http", website=True, methods=['post'], csrf=False)
    def create(self, **post):
        
        theme_list = ['barman', 'spoon_brigadeiro', 'candied_brigadeiro', 'gourmet_fit_cart', 'tower_macarons', 'italian_straw', 'popcorn_gourmet', 'cotton_candy', 'acai_in_a_glass', 'barman', 'brigadeiro_bike', 'churros', 'mini_quiche', 'coloring', 'coloring_discoloring_finishers', 'mens_line', 'reduction_with_high_liss', 'home_cara_training', 'workstation_infusion_recoveri_finishers', 'home_cara_training_finishers', 'barman', 'candied_brigadeiro', 'spoon_brigadeiro', 'theme', 'theme', 'italian_straw', 'theme', 'cotton_candy', 'acai_in_a_glass', 'honey_bread_candy', 'barman', 'brigadeiro_bike', 'churros', 'mini_quiche']

        selected_themes = []
        for theme in theme_list:
            if post.get(theme):
                theme_ids = http.request.env['kami_sm.attendance.theme'].browse(
                    int(post.get(theme))
                )
                
                selected_themes.append(theme_ids.id)

        

        type_ids = http.request.env['kami_sm.attendance.type'].browse(
            int(post.get("types"))
        )

        user = http.request.env['res.users'].browse(
            int(post.get("responsible"))
        )

        vals = {
            'client_id' : post.get('client_name'),
            'type_id' : type_ids.id,
            'theme_ids' : selected_themes,
            'has_tasting' : post.get('has_deg_checkbox'),
            'start_date' : post.get('date'),
            'backoffice_user_id' : user.id,
        }

        request.env['kami_sm.attendance'].sudo().create(vals)
        return http.request.render('kami_form.forms_success_page')
        

class Teste(http.Controller):
    @http.route('/teste', auth='public', csrf=False, website=True)    
    def index(self, **kw):
        users = http.request.env['res.users']
        partners = request.env['res.partner'].sudo().search([])
        att_types = request.env['kami_sm.attendance.type'].sudo().search([])
        att_themes = request.env['kami_sm.attendance.theme'].sudo().search([])
        return http.request.render('kami_form.teste', {
            'users': users.sudo().search([]),
            'partners' : partners,
            'att_types' : att_types,
            'att_themes' : att_themes,
        })
    
class SolicitacaoViagem(http.Controller):
    @http.route('/viagem', auth='public', csrf=False, website=True)    
    def index(self, **kw):
        users = http.request.env['res.users']
        partners = request.env['res.partner'].sudo().search([])
        companyes = http.request.env['res.company'].sudo().search([])
        
        return http.request.render('kami_form.viagem', {
            'users': users.sudo().search([]),
            'partners' : partners,
            'companyes' : companyes,
        })
    
    @http.route('/viagem', auth='public', type="http", website=True, methods=['post'], csrf=False)
    def create(self, **post):

        data_saida = datetime.strptime(post.get('date_exit'), '%Y-%m-%d')
        data_saida_formatado = data_saida.strftime('%d/%m/%Y')

        data_volta = datetime.strptime(post.get('date_entrance'), '%Y-%m-%d')
        data_volta_formatado = data_volta.strftime('%d/%m/%Y')

        category = request.env.ref('kami_form.financeiro_solicitacaoviagem_category')

        partner = http.request.env['res.partner'].browse(
            int(post.get("responsible"))
        )

        company = http.request.env['res.partner'].browse(
            int(post.get("empresa"))
        )

        team_id = request.env.ref('kami_form.financeiro_team')

        type_id = request.env.ref('kami_form.financeiro_solicitacaoviagem')

        description = f"""
                <strong>Empresa:</strong> {company.name} <br></br>
                <strong>Solicitante:</strong> {partner.name} <br></br>
                <strong>CPF:</strong> {post.get('cpf')} <br></br>
                <strong>RG:</strong> {post.get('rg')} <br></br>
                <strong>Data de Nascimento: </strong> {post.get('data_nascimento')} <br></br>
                <strong>E-mail: </strong> {partner.email if partner.email else 'O usuario não possui e-mail. Precisa cadastrar'} <br></br>
                <strong>Data de Saída: </strong> {data_saida_formatado} <br></br>
                <strong>Hora de Saída: </strong> {data_volta_formatado} <br></br>
                <strong>Data de Entrada: </strong> {post.get('date_entrance')} <br></br>
                <strong>Hora de Entrada: </strong> {post.get('hour_entrance')} <br></br>
                <strong>Local do compromisso para reserva da Hospedagem: </strong> {post.get('accommodation')} <br></br>
        """
        new_task = {


            "name": "Solicitação de Viagem",
            "type_id" : type_id.id,
            "user_id" : partner.id,
            "team_id" : team_id.id,
            "category_id": category.id,
            "company_id": category.company_id.id or partner.company_id.id,
            "description": description,
            "channel_id": request.env["helpdesk.ticket.channel"]
            .sudo()
            .search([("name", "=", "Web")])
            .id,
            "partner_id": request.env.user.partner_id.id,
            "partner_name": request.env.user.partner_id.name,
            "partner_email": request.env.user.partner_id.email,
        
        }
        request.env["helpdesk.ticket"].sudo().create(new_task)
        return http.request.render('kami_form.forms_success_page', {})
    
class SolicitacaoPagamento(http.Controller):
    @http.route('/pagamento', auth='public', csrf=False, website=True)    
    def index(self, **kw):
        
        users = http.request.env['res.users']
        partners = request.env['res.partner'].sudo().search([])
        companyes = http.request.env['res.company'].sudo().search([])
        teams = http.request.env['helpdesk.ticket.team'].sudo().search([])
        return http.request.render('kami_form.pagamento', {
            'users': users.sudo().search([]),
            'partners' : partners,
            'companyes' : companyes,
            'teams' : teams,
        })

    @http.route('/pagamento', type='http', auth='public', website=True, methods=['POST'], csrf=False)  
    def create(self, **post):

        partner = http.request.env['res.users'].browse(
            int(post.get("responsible"))
        )


        
        category = request.env.ref('kami_form.financeiro_solicitacaopagamento_category')

        team_id = request.env.ref('kami_form.financeiro_team')

        type_id = request.env.ref('kami_form.financeiro_solicitacaopagamento')

        bank_account = f"""{post.get('bank_name')}<br></br> <strong>Numero do Banco</strong> : {post.get('bank_number')}<br></br> <strong>Agência</strong> : {post.get('agency')}<br></br> <strong>Conta Corrente</strong> : {post.get('curreny_account')}"""


        description = f"""
                <strong>Empresa:</strong> {post.get('company')} <br></br>
                <strong>Área:</strong> {post.get('area')} <br></br>
                <strong>Descrição do Serviço:</strong> {post.get('product_description')} <br></br>
                <strong>Necessidade do Pagamento:</strong> {post.get('payment_description')} <br></br>
                <strong>Moeda:</strong> {post.get('moeda')} <br></br>
                <strong>Valor:</strong> {post.get('valor')} <br></br>
                <strong>Data do Vencimento:</strong> {post.get('data_vencimento')} <br></br>
                <strong>Data do Recebimento:</strong> {post.get('data_recebimento')} <br></br>
                <strong>CPF ou CNPJ:</strong> {post.get('natureza')} <br></br>
                <strong>Número:</strong> {post.get('cpf') if post.get('cpf') else post.get('cnpj')} <br></br>
                <strong>Método de Pagamento:</strong> {post.get('payment_method')} <br></br>
                <strong>Dados de Recebimento:</strong> {post.get('pix_key') if post.get('pix_key') else  bank_account} <br></br>
                
        """

        vals = {
            "name": "Solicitação de Pagamento",
            "type_id" : type_id.id,
            "user_id" : partner.id,
            "team_id" : team_id.id,
            "category_id": category.id,
            "company_id": category.company_id.id or partner.company_id.id,
            "description": description,
            "channel_id": request.env["helpdesk.ticket.channel"]
            .sudo()
            .search([("name", "=", "Web")])
            .id,
            "partner_id": request.env.user.partner_id.id,
            "partner_name": request.env.user.partner_id.name,
            "partner_email": request.env.user.partner_id.email,
        }

        new_ticket = request.env["helpdesk.ticket"].sudo().create(vals)
        if 'nf' in http.request.params:
            for c_file in request.httprequest.files.getlist("nf"):
                data = c_file.read()
                if c_file.filename:
                    request.env["ir.attachment"].sudo().create(
                        {
                            "name": c_file.filename,
                            "datas": base64.b64encode(data),
                            "res_model": "helpdesk.ticket",
                            "res_id": new_ticket.id,
                        }
                    )
        elif 'boleto' in http.request.params:
            for c_file in request.httprequest.files.getlist("boleto"):
                data = c_file.read()
                if c_file.filename:
                    request.env["ir.attachment"].sudo().create(
                        {
                            "name": c_file.filename,
                            "datas": base64.b64encode(data),
                            "res_model": "helpdesk.ticket",
                            "res_id": new_ticket.id,
                        }
                    )
        
        return http.request.render('kami_form.forms_success_page')
    
    

