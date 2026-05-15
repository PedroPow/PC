import discord
from discord.ext import commands
from discord.ui import View, Button, Select, Modal, TextInput
from discord import Embed
import asyncio
import aiohttp
import io
import os
from datetime import datetime

# ============================
#    CONFIGURAÇÕES DO SERVIDOR
# ============================
GUILD_ID = 1491438032203677819
VERIFY_CHANNEL_ID = 1496017827323318433
LOG_CHANNEL_ID = 1491438044660633604
ROLE_VERIFY_ID = 1504892436176961537
ROLE_AUTOROLE_ID = 1504883665040048148
ADMIN_ROLE_ID = 1491438032203677820
PAINEL_CHANNEL_ID = 1491438044660633602

# Advertências
ID_CARGO_ADV1 = 1491438032203677828
ID_CARGO_ADV2 = 1491438032203677827
ID_CARGO_ADV3 = 1491438032203677826
ID_CARGO_BANIDO = 1491438032220328056

CARGOS_AUTORIZADOS = [1491438032203677820]

# ================= CONFIG SET =================
CANALETA_SOLICITAR_SET_ID = 1491438033860427848
CARGO_NOVATO_ID = 1504883665040048148
CATEGORIA_TICKET_ID = 1504884604631257128
CANAL_LOGS_ROTA = 1491438033860427849
CARGO_ROTA_ID = 1491438032337895561

# ================= NOVA ESTRUTURA DE DADOS =================
# Agora as patentes estão dentro de cada Divisão (Companhia)
DIVISOES_DADOS = {
"PC": {
    "label": "Delegacia de Policia Civil - 1° DP",
    "role_id": 1491438032337895561, 
    "patentes": {
        "AGENTE 3° CLASSE": [1491438032337895563],
        "AGENTE 2° CLASSE": [1491438032337895564],
        "AGENTE 1° CLASSE": [1491438032354545774],
        "AGENTE CLASSE ESPECIAL": [1491438032354545775],
        "ESCRIVÃO": [1491438032354545776],
        "INVESTIGADOR": [1491438032354545777],
        "INVESTIGADOR CHEFE": [1491438032354545778],
        "PAPILOSCOPISTA": [1491438032354545779],
        "PERITO": [1491438032354545780],
        "PERITO CHEFE": [1491438032354545781],
        "DELEGADO ADJUNTO": [1491438032392421559],
        "DELEGADO GERAL": [1491438032392421560],
    }
},

"DOPE": {
    "label": "Departamento de Operações Policiais Estratégicas - DOPE",
    "role_id": 1491438032312860753,
    "patentes": { 
        "AGENTE 3° CLASSE": [1491438032337895563],
        "AGENTE 2° CLASSE": [1491438032337895564],
        "AGENTE 1° CLASSE": [1491438032354545774],
        "AGENTE CLASSE ESPECIAL": [1491438032354545775],
        "ESCRIVÃO": [1491438032354545776],
        "INVESTIGADOR": [1491438032354545777],
        "INVESTIGADOR CHEFE": [1491438032354545778],
        "PAPILOSCOPISTA": [1491438032354545779],
        "PERITO": [1491438032354545780],
        "PERITO CHEFE": [1491438032354545781],
        "DELEGADO ADJUNTO": [1491438032392421559],
        "DELEGADO DOPE": [1491438032384036970],
    }
},

"DECAP": {
    "label": "Polícia Judiciária da Capital - DECAP",
    "role_id": 1491438032337895558,
    "patentes": { 
        "AGENTE 3° CLASSE": [1491438032337895563],
        "AGENTE 2° CLASSE": [1491438032337895564],
        "AGENTE 1° CLASSE": [1491438032354545774],
        "AGENTE CLASSE ESPECIAL": [1491438032354545775],
        "ESCRIVÃO": [1491438032354545776],
        "INVESTIGADOR": [1491438032354545777],
        "INVESTIGADOR CHEFE": [1491438032354545778],
        "PAPILOSCOPISTA": [1491438032354545779],
        "PERITO": [1491438032354545780],
        "PERITO CHEFE": [1491438032354545781],
        "DELEGADO ADJUNTO": [1491438032392421559],
        "DELEGADO DECAP": [1491438032384036969],
    }
},    

"DHPP": {
    "label": "Homicídios e Proteção à Pessoa - DHPP",
    "role_id": 1491438032337895557,
    "patentes": {
        "AGENTE 3° CLASSE": [1491438032337895563],
        "AGENTE 2° CLASSE": [1491438032337895564],
        "AGENTE 1° CLASSE": [1491438032354545774],
        "AGENTE CLASSE ESPECIAL": [1491438032354545775],
        "ESCRIVÃO": [1491438032354545776],
        "INVESTIGADOR": [1491438032354545777],
        "INVESTIGADOR CHEFE": [1491438032354545778],
        "PAPILOSCOPISTA": [1491438032354545779],
        "PERITO": [1491438032354545780],
        "PERITO CHEFE": [1491438032354545781],
        "DELEGADO ADJUNTO": [1491438032392421559],
        "DELEGADO DHPP": [1491438032384036968],
    }
},     

"DEIC": {
    "label": "Investigações Criminais - DEIC",
    "role_id": 1491438032337895556,
    "patentes": {
        "AGENTE 3° CLASSE": [1491438032337895563],
        "AGENTE 2° CLASSE": [1491438032337895564],
        "AGENTE 1° CLASSE": [1491438032354545774],
        "AGENTE CLASSE ESPECIAL": [1491438032354545775],
        "ESCRIVÃO": [1491438032354545776],
        "INVESTIGADOR": [1491438032354545777],
        "INVESTIGADOR CHEFE": [1491438032354545778],
        "PAPILOSCOPISTA": [1491438032354545779],
        "PERITO": [1491438032354545780],
        "PERITO CHEFE": [1491438032354545781],
        "DELEGADO ADJUNTO": [1491438032392421559],
        "DELEGADO DEIC": [1491438032384036967],
    }
}, 

"GOE": {
    "label": "Grupo de Operações Especiais - G.O.E",
    "role_id": 1491438032312860750,
    "patentes": { 
        "AGENTE 3° CLASSE": [1491438032337895563],
        "AGENTE 2° CLASSE": [1491438032337895564],
        "AGENTE 1° CLASSE": [1491438032354545774],
        "AGENTE CLASSE ESPECIAL": [1491438032354545775],
        "ESCRIVÃO": [1491438032354545776],
        "INVESTIGADOR": [1491438032354545777],
        "INVESTIGADOR CHEFE": [1491438032354545778],
        "PAPILOSCOPISTA": [1491438032354545779],
        "PERITO": [1491438032354545780],
        "PERITO CHEFE": [1491438032354545781],
        "DELEGADO ADJUNTO": [1491438032392421559],
        "DELEGADO GOE": [1491438032384036966],
    }
},   

"SAT": {
    "label": "Serviço Aerotático - SAT",
    "role_id": 1491438032312860749,
    "patentes": {
        "AGENTE 3° CLASSE": [1491438032337895563],
        "AGENTE 2° CLASSE": [1491438032337895564],
        "AGENTE 1° CLASSE": [1491438032354545774],
        "AGENTE CLASSE ESPECIAL": [1491438032354545775],
        "ESCRIVÃO": [1491438032354545776],
        "INVESTIGADOR": [1491438032354545777],
        "INVESTIGADOR CHEFE": [1491438032354545778],
        "PAPILOSCOPISTA": [1491438032354545779],
        "PERITO": [1491438032354545780],
        "PERITO CHEFE": [1491438032354545781],
        "DELEGADO ADJUNTO": [1491438032392421559],
        "DELEGADO SAT": [1491438032384036965],
    }
},   

"GARRA": {
    "label": "Repressão a Roubos - GARRA",
    "role_id": 1491438032312860752,
    "patentes": {
        "AGENTE 3° CLASSE": [1491438032337895563],
        "AGENTE 2° CLASSE": [1491438032337895564],
        "AGENTE 1° CLASSE": [1491438032354545774],
        "AGENTE CLASSE ESPECIAL": [1491438032354545775],
        "ESCRIVÃO": [1491438032354545776],
        "INVESTIGADOR": [1491438032354545777],
        "INVESTIGADOR CHEFE": [1491438032354545778],
        "PAPILOSCOPISTA": [1491438032354545779],
        "PERITO": [1491438032354545780],
        "PERITO CHEFE": [1491438032354545781],
        "DELEGADO ADJUNTO": [1491438032392421559],
        "DELEGADO GARRA": [1491438032384036964],
    }
},   

"GER": {
    "label": "Grupo Especial de Reação - G.E.R",
    "role_id": 1491438032312860751,
    "patentes": {
        "AGENTE 3° CLASSE": [1491438032337895563],
        "AGENTE 2° CLASSE": [1491438032337895564],
        "AGENTE 1° CLASSE": [1491438032354545774],
        "AGENTE CLASSE ESPECIAL": [1491438032354545775],
        "ESCRIVÃO": [1491438032354545776],
        "INVESTIGADOR": [1491438032354545777],
        "INVESTIGADOR CHEFE": [1491438032354545778],
        "PAPILOSCOPISTA": [1491438032354545779],
        "PERITO": [1491438032354545780],
        "PERITO CHEFE": [1491438032354545781],
        "DELEGADO ADJUNTO": [1491438032392421559],
        "DELEGADO GER": [1491438032354545783],
    }
},              
}

solicitacoes_abertas = {}

# ================= BOT + INTENTS =================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

TOKEN = os.getenv("TOKEN_PC")  # Certifique-se de definir a variável de ambiente TOKEN_PC com o token do seu bot para segurança
if not TOKEN:
    print("❌ Erro: TOKEN_PC não definido nas variáveis de ambiente.")
    exit(1)

# ================= HELPERS =================
async def enviar_log_embed(guild, embed):
    if not guild: return
    canal = guild.get_channel(LOG_CHANNEL_ID)
    if canal:
        try: await canal.send(embed=embed)
        except: pass

async def enviar_log(guild, titulo, descricao, cor=discord.Color.green()):
    canal = guild.get_channel(LOG_CHANNEL_ID) if guild else None
    if canal:
        embed = discord.Embed(title=titulo, description=descricao, color=cor)
        embed.set_footer(text="Sistema de Logs - Policia Civil® ")
        try: await canal.send(embed=embed)
        except: pass

def has_authorized_role(member):
    return any(role.id in CARGOS_AUTORIZADOS for role in member.roles)

async def require_authorized(interaction):
    if not has_authorized_role(interaction.user):
        await interaction.response.send_message("❌ Você não tem permissão.", ephemeral=True)
        return False
    return True

# ================= COMANDOS SLASH =================
@bot.tree.command(name="clearall", description="Apaga mensagens.", guild=discord.Object(id=GUILD_ID))
async def clearall(interaction):
    if not await require_authorized(interaction): return
    await interaction.response.send_message("🧹 Limpando canal...", ephemeral=True)
    await interaction.channel.purge(limit=None)
    await interaction.channel.send(embed=discord.Embed(title="🧹 Canal Limpo", color=discord.Color.green()))

class MensagemModal(Modal, title="📢 Enviar Mensagem"):
    conteudo = TextInput(label="Conteúdo", style=discord.TextStyle.paragraph, required=True)
    async def on_submit(self, interaction):
        await interaction.response.send_message("⏳ Enviando...", ephemeral=True)
        await interaction.channel.send(self.conteudo.value)

@bot.tree.command(name="mensagem", description="Enviar mensagem como o bot.", guild=discord.Object(id=GUILD_ID))
async def mensagem(interaction):
    if not await require_authorized(interaction): return
    await interaction.response.send_modal(MensagemModal())

@bot.tree.command(name="adv", description="Aplica advertência.", guild=discord.Object(id=GUILD_ID))
async def adv(interaction, membro: discord.Member, motivo: str):
    if not await require_authorized(interaction): return
    adv1, adv2, adv3, banido = [interaction.guild.get_role(r) for r in [ID_CARGO_ADV1, ID_CARGO_ADV2, ID_CARGO_ADV3, ID_CARGO_BANIDO]]
    if adv2 in membro.roles: await membro.remove_roles(adv2); await membro.add_roles(adv3); msg="⚠ 3ª ADV!"
    elif adv1 in membro.roles: await membro.remove_roles(adv1); await membro.add_roles(adv2); msg="⚠ 2ª ADV!"
    else: await membro.add_roles(adv1); msg="⚠ 1ª ADV!"
    await interaction.response.send_message(msg, ephemeral=True)

@bot.tree.command(name="ban", description="Bane um membro.", guild=discord.Object(id=GUILD_ID))
async def ban(interaction, membro: discord.Member, motivo: str):
    if not await require_authorized(interaction): return
    await membro.ban(reason=motivo)
    await interaction.response.send_message(f"🔨 {membro.mention} banido!", ephemeral=True)

# ================= NOVO SISTEMA DE TICKET (INVERTIDO) =================

class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Solicitar Funcional", style=discord.ButtonStyle.secondary, emoji="<:PC:1504874625790644385>", custom_id="ticket_abrir")
    async def abrir_ticket(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id in solicitacoes_abertas:
            return await interaction.response.send_message("⚠️ Você já possui um ticket aberto.", ephemeral=True)

        guild = interaction.guild
        user = interaction.user
        category = guild.get_channel(CATEGORIA_TICKET_ID)
        overwrites = {guild.default_role: discord.PermissionOverwrite(read_messages=False), user: discord.PermissionOverwrite(read_messages=True, send_messages=True)}
        canal = await guild.create_text_channel(name=f"ticket-{user.name}", category=category, overwrites=overwrites)
        
        solicitacoes_abertas[user.id] = {"canal_id": canal.id}

        view = View()
        view.add_item(SelectCIA(user.id)) # CHAMA CIA PRIMEIRO

# --- NOVA LÓGICA AQUI ---
        # Criamos o Embed
        embed = discord.Embed(
            title="Ticket Criado 🎫", 
            description=f"> Seu canal de atendimento foi gerado com sucesso.\n\n"
            f"> Por favor, clique no botão abaixo para acessar seu ticket e seguir com o processo de solicitação de funcional.", 
            color=discord.Color.yellow()
        )
        
        # Criamos a View com o Botão de Redirecionamento
        view_redirect = View()
        btn_ir_para_ticket = Button(
            label="Ir para o Ticket", 
            url=f"https://discord.com/channels/{guild.id}/{canal.id}", # Link direto para o canal
            emoji="<:PC:1504874625790644385>"
        )
        view_redirect.add_item(btn_ir_para_ticket)

        # Enviamos a resposta para o usuário (em ephemeral para não poluir o chat público)
        await interaction.response.send_message(embed=embed, view=view_redirect, ephemeral=True)

        # Mensagem inicial dentro do canal do ticket com o menu de Cias
        view_cia = View()
        view_cia.add_item(SelectCIA(user.id))
        await canal.send(f"{user.mention}, bem-vindo! Selecione sua **Divisão de Atuação** abaixo para prosseguir:", view=view_cia)

class SelectCIA(Select):
    def __init__(self, user_id):
        self.user_id = user_id
        options = [discord.SelectOption(label=d["label"], value=k) for k, d in DIVISOES_DADOS.items()]
        super().__init__(placeholder="Escolha sua divisão de atuação", options=options)

    async def callback(self, interaction: discord.Interaction):
        cia_key = self.values[0]
        view = View()
        view.add_item(SelectPatenteDinamica(self.user_id, cia_key))
        await interaction.response.send_message(f"Divisão selecionada. Agora escolha sua **Patente**:", view=view, ephemeral=True)

class SelectPatenteDinamica(Select):
    def __init__(self, user_id, cia_key):
        self.user_id = user_id
        self.cia_key = cia_key
        patentes = DIVISOES_DADOS[cia_key]["patentes"]
        options = [discord.SelectOption(label=p, value=p) for p in patentes.keys()]
        super().__init__(placeholder="Selecione sua patente", options=options)

    async def callback(self, interaction: discord.Interaction):
        patente_nome = self.values[0]
        patente_ids = DIVISOES_DADOS[self.cia_key]["patentes"][patente_nome]
        await interaction.response.send_modal(DadosPessoaisModal(self.user_id, patente_nome, patente_ids, self.cia_key))

class DadosPessoaisModal(Modal, title="Registro do Policial"):
    nome = TextInput(label="Nome e Sobrenome", required=True)
    passaporte = TextInput(label="Identificação (ID)", required=True)

    def __init__(self, user_id, patente_nome, patente_id, cia):
        super().__init__()
        self.user_id, self.patente_nome, self.patente_id, self.cia = user_id, patente_nome, patente_id, cia

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        solicitacoes_abertas[self.user_id].update({"patente_id": self.patente_id, "nome": self.nome.value, "passaporte": self.passaporte.value, "cia": self.cia})
        
        embed = Embed(title="Solicitação de Funcional", description=f"**Solicitante:** {interaction.user.mention}\n**Nome:** {self.nome.value}\n**R.E:** {self.passaporte.value}\n**Companhia:** {self.cia}\n**Patente:** {self.patente_nome}", color=discord.Color.yellow())

        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1444735189765849320/1504862661383553024/PC.png")

        embed.set_image(url="https://cdn.discordapp.com/attachments/1444735189765849320/1504901482137260193/FAIXA_PC_2.png?ex=6a08ac39&is=6a075ab9&hm=01c672c3a89f1e6e781db301a6998e0b4ebd690081b2e12ccca4e29bd00dc2b3&")

        embed.set_footer(text="Delegacia de Policia Civil® - Todos direitos reservados.")
        
        canal_logs = await interaction.client.fetch_channel(CANAL_LOGS_ROTA)
        await canal_logs.send(embed=embed, view=ConfirmarOuFecharView(self.user_id))
        await interaction.followup.send("✅ Solicitação enviada.", ephemeral=True)

class ConfirmarOuFecharView(View):

    def __init__(self, user_id):

        super().__init__(timeout=None)

        self.user_id = user_id



    @discord.ui.button(

            label="Aceitar Funcional",

            style=discord.ButtonStyle.gray,

            emoji="<:AMARELO:1495480160319836412> ",

            custom_id="confirmar_set"

            )

    async def confirmar(self, interaction: discord.Interaction, button: Button):
        dados = solicitacoes_abertas.pop(self.user_id, None)
        if not dados:
            await interaction.response.send_message("❌ Solicitação não encontrada.", ephemeral=True)
            return

        membro = interaction.guild.get_member(self.user_id)
        if not membro:
            return await interaction.response.send_message("❌ Membro não encontrado no servidor.", ephemeral=True)

        # --- LÓGICA DO NOME (NICKNAME) ---
        # Pegamos o label da divisão (ex: 1° DP em vez de PC)
        cia_key = dados.get('cia')
        label_divisao = DIVISOES_DADOS.get(cia_key, {}).get("label", cia_key)
        
        # Se o label for muito grande (ex: "Delegacia de Policia Civil - 1° DP"), 
        # vamos tentar extrair apenas o final ou usar uma versão curta para não estourar os 32 caracteres do Discord
        if "1° DP" in label_divisao:
            div_nome = "1° DP"
        elif "GARRA" in label_divisao:
            div_nome = "GARRA"
        else:
            div_nome = cia_key # Fallback para a sigla caso seja outra

        novo_apelido = f"{div_nome} | {dados['nome'].upper()} - {dados['passaporte']}"

        try:
            # O Discord limita nicks a 32 caracteres. 
            # O [:32] garante que o bot não quebre se o nome for longo.
            await membro.edit(nick=novo_apelido[:32])
        except discord.Forbidden:
            print(f"Erro: Sem permissão para mudar o nick de {membro.name}. O cargo do bot deve estar acima do dele.")
        except Exception as e:
            print(f"Erro ao mudar apelido: {e}")

        # --- RESTANTE DA LOGICA DE CARGOS ---
        novato = interaction.guild.get_role(CARGO_NOVATO_ID)
        if novato and novato in membro.roles:
            await membro.remove_roles(novato)

        cargos = []
        # Cargos da Patente
        for role_id in dados['patente_id']:
            role = interaction.guild.get_role(role_id)
            if role: cargos.append(role)

        # Cargo da Divisão (Role Fixa)
        if cia_key in DIVISOES_DADOS:
            id_da_divisao = DIVISOES_DADOS[cia_key].get("role_id")
            role_divisao = interaction.guild.get_role(id_da_divisao)
            if role_divisao: cargos.append(role_divisao)

        if cargos:
            await membro.add_roles(*cargos)

        # --- ATUALIZAÇÃO DO EMBED ---
        agora = datetime.now().strftime("%d/%m/%Y às %H:%M")
        embed = interaction.message.embeds[0]
        embed.color = discord.Color.green()
        embed.title = "✅ SOLICITAÇÃO APROVADA"
        
        # Limpa fields antigos se necessário e adiciona os novos
        embed.add_field(name="Aprovado por:", value=interaction.user.mention, inline=True)
        embed.add_field(name="ID aprovador:", value=f"`{interaction.user.id}`", inline=True)
        embed.add_field(name="Data:", value=f"`{agora}`", inline=False)

        await interaction.message.edit(embed=embed, view=None)
        await interaction.response.send_message(f"✅ Set de {membro.mention} realizado com sucesso!", ephemeral=True)

        # Deletar canal do ticket
        canal = interaction.guild.get_channel(dados["canal_id"])
        if canal:
            await asyncio.sleep(5)
            await canal.delete()

    @discord.ui.button(

            label="Recusar Funcional",

            style=discord.ButtonStyle.gray,

            emoji="<:x1:1495508233647952062>",

            custom_id="recusar_set"

            )

    async def cancelar(self, interaction: discord.Interaction, button: Button):



        dados = solicitacoes_abertas.pop(self.user_id, None)



        embed = interaction.message.embeds[0]

        embed.color = discord.Color.red()

        embed.description += f"\n\n❌ **Cancelado por:** {interaction.user.mention}"



        await interaction.message.edit(embed=embed, view=None)



        await interaction.response.send_message("🗑️ Solicitação cancelada.", ephemeral=True)



        if dados:

            canal = interaction.guild.get_channel(dados["canal_id"])

            if canal:

                await asyncio.sleep(5)

                await canal.delete()



# ================= READY =================

@bot.event
async def on_ready():
    print(f"🔥 Bot conectado como {bot.user}")

    bot.add_view(TicketView())
    bot.add_view(ConfirmarOuFecharView(user_id=0))  # user_id dummy    

    print("📡 Guilds que o bot está:")
    for g in bot.guilds:
        print(f"- {g.name} | ID: {g.id}")

    guild = discord.utils.get(bot.guilds, id=GUILD_ID)

    if not guild:
        print(f"❌ Guild {GUILD_ID} NÃO encontrada.")
        return

    print(f"✅ Guild encontrada: {guild.name}")

    # ================= PAINEL SET =================

    try:
        canal = guild.get_channel(CANALETA_SOLICITAR_SET_ID)

        if canal:
            # Apaga mensagens antigas do bot
            async for msg in canal.history(limit=10):
                if msg.author == bot.user:
                    await msg.delete()

        # 1️⃣ Criar
        embed = discord.Embed(
            title="Delegacia de Policia Civil | Solicitar Funcional",
            description=(
            "• Utilize o botão abaixo para solicitar sua funcional. Após enviar seus dados, aguarde receber a resposta em seu privado.\n\n"
            "> É necessario ter em mãos o seu:\n\n"   
            "> `Nome e Sobrenome:`\n"
            "> `Identificação (ID):`\n"    
            "> `Divisão de atuação:`\n"             
            ),
            color=discord.Color.yellow()
        )

        # 2️⃣ Configurar
        embed.set_image(url="https://cdn.discordapp.com/attachments/1444735189765849320/1504900670745215086/FAIXA_PC_1.png?ex=6a08ab77&is=6a0759f7&hm=aa4cd383f5b1da8839639f3657b0966477c4cf10e4017617d2a873b216c9177a&") # IMAGEM RETANGULAR ABAIXO
        

        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1444735189765849320/1504862661383553024/PC.png?ex=6a088811&is=6a073691&hm=ea556dd712f2a840f7dbac71ddd483e3e8f3b827a3d7962dd67e5844489fa7ab&\n") # IMAGEM QUADRADA A DIREITA


        embed.set_footer(text="Delegacia de Policia Civil® - Todos direitos reservados.")
        

        # 3️⃣ Enviar
        await canal.send(embed=embed, view=TicketView())



    except Exception as e:  
        print(f"Erro ao enviar painel SET: {e}")
    

    # ================= SYNC SLASH =================

    try:
        synced = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
        print(f"🔧 Slash Commands sincronizados: {[cmd.name for cmd in synced]}")
    except Exception as e:
        print(f"Erro ao sincronizar comandos: {e}")

    # ================= LOG DE START =================

    await enviar_log(guild, "🚀 Bot iniciado", "Sistema de SET e Slash Commands ativos.")

bot.run(TOKEN_PC)