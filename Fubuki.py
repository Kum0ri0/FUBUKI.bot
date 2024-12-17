import discord
from discord import app_commands
from discord.ext import commands
import asyncio
from discord.ui import Button, View
import re
import random
from datetime import datetime, timedelta



TOKEN = "MTMwOTYzODU5MDM2NzY2NjI1Nw.GLR9kO.47lTRhC1ZO2IBp6UOq0a-AMDCQVuGpp8Uu-vMY"

# Configuration du bot avec intents
intents = discord.Intents.all()
intents.members = True  # S'assurer que l'intent 'members' est activé
bot = commands.Bot(command_prefix="-", intents=intents)




bot.event
async def on_ready():
    print(f"Bot connecté en tant que {bot.user}")

@bot.command()
async def salut(ctx):
    """Commande simple : répond 'Bonjour!' quand l'utilisateur tape '!salut'"""
    await ctx.send("Bonjour! 👋")

@bot.command()
async def addition(ctx, a: int, b: int):
    """Commande d'addition : '!addition 5 3' => 8"""
    resultat = a + b
    await ctx.send(f"Le résultat est : {resultat}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

  
    if bot.user.mentioned_in(message):
        await message.channel.send("Vous avez besoin d'aide? Tapez `!help` pour voir mes commandes!")
    

    await bot.process_commands(message)

# Événement : le bot est prêt
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot connecté en tant que {bot.user} et commandes slash synchronisées.")
 
# Commande slash pour mute un utilisateur avec une durée
@bot.tree.command(name="mute", description="Mute un membre avec une durée spécifiée.")
@app_commands.describe(member="Le membre à mute", duration="Durée (format : 1h, 30m, etc.)", reason="La raison du mute")
async def mute(interaction: discord.Interaction, member: discord.Member, duration: str, reason: str = "Aucune raison fournie"):
    # Vérification des permissions
    if not interaction.user.guild_permissions.moderate_members:
        await interaction.response.send_message(
            "❌ Vous n'avez pas la permission de mute des membres.", ephemeral=True
        )
        return

    # Calculer la durée du mute
    try:
        duration_mapping = {
            "h": lambda v: timedelta(hours=v),
            "m": lambda v: timedelta(minutes=v),
            "s": lambda v: timedelta(seconds=v),
            "j": lambda v: timedelta(days=v)
        }
        time_unit = duration[-1]
        time_value = int(duration[:-1])

        if time_unit not in duration_mapping:
            await interaction.response.send_message(
                "❌ Format de durée invalide. Utilisez par exemple : 1h, 30m, 10s, 1j.", ephemeral=True
            )
            return

        mute_time = duration_mapping[time_unit](time_value)
        until_time = discord.utils.utcnow() + mute_time
        await member.timeout(until_time, reason=reason)

        embed = discord.Embed(
            title="Utilisateur muté",
            description=f"{member.mention} a été mute pour {duration}.\n\n**Raison** : {reason}",
            color=discord.Color.purple()
        )
        embed.set_image(url="https://i.pinimg.com/originals/76/bb/a0/76bba03c99c07c3c7510c0b7f5d9a876.gif")  # Image par défaut pour le mute
        embed.set_footer(text=f"Muté par {interaction.user}")

        await interaction.response.send_message(embed=embed)

    except discord.Forbidden:
        await interaction.response.send_message(
            "❌ Je n'ai pas la permission de mute cet utilisateur.", ephemeral=True
        )
    except Exception as e:
        await interaction.response.send_message(
            f"❌ Une erreur est survenue : {e}", ephemeral=True
        )
   

# Commande slash pour unmute un utilisateur
@bot.tree.command(name="unmute", description="Dé-mute un membre.")
@app_commands.describe(member="Le membre à unmute", reason="La raison du unmute")
async def unmute(interaction: discord.Interaction, member: discord.Member, reason: str = "Aucune raison fournie"):
    # Vérification des permissions
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message(
            "❌ Vous n'avez pas la permission de gérer les messages (unmute).", ephemeral=True
        )
        return

    # Vérification : ne pas unmute soi-même ou le bot
    if member == interaction.user:
        await interaction.response.send_message(
            "❌ Vous ne pouvez pas vous unmute vous-même.", ephemeral=True
        )
        return
    if member == bot.user:
        await interaction.response.send_message(
            "❌ Vous ne pouvez pas unmute le bot.", ephemeral=True
        )
        return

    # Tentative de unmute
    try:
        # Retirer le rôle "Muted" du membre
        muted_role = discord.utils.get(interaction.guild.roles, name="Muted")
        if not muted_role:
            await interaction.response.send_message(
                "❌ Le rôle 'Muted' n'existe pas. Veuillez créer un rôle 'Muted' avec les bonnes permissions.", ephemeral=True
            )
            return

        await member.remove_roles(muted_role, reason=reason)
        embed = discord.Embed(
            title="Utilisateur unmute",
            description=f"{member.mention} a été unmute avec succès.\n\n**Raison** : {reason}",
            color=discord.Color.purple()
        )
        embed.set_image(url="https://i.pinimg.com/originals/8b/2a/5c/8b2a5cbe7b58d2c3f577235f805b6ef2.gif")
        embed.set_footer(text=f"Unmute par {interaction.user}")

        await interaction.response.send_message(embed=embed)
    except discord.Forbidden:
        await interaction.response.send_message(
            "❌ Je n'ai pas la permission de retirer ce rôle.", ephemeral=True
        )
    except Exception as e:
        await interaction.response.send_message(
            f"❌ Une erreur est survenue : {e}", ephemeral=True
        )


# Événement : le bot est prêt
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot connecté en tant que {bot.user} et commandes slash synchronisées.")

# Commande slash pour bannir un utilisateur
@bot.tree.command(name="ban", description="Bannir un membre du serveur.")
@app_commands.describe(member="Le membre à bannir", reason="La raison du bannissement")
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "Aucune raison fournie"):
    # Vérification des permissions
    if not interaction.user.guild_permissions.ban_members:
        await interaction.response.send_message(
            "❌ Vous n'avez pas la permission de bannir des membres.", ephemeral=True
        )
        return

    # Vérification : ne pas bannir soi-même ou le bot
    if member == interaction.user:
        await interaction.response.send_message(
            "❌ Vous ne pouvez pas vous bannir vous-même.", ephemeral=True
        )
        return
    if member == bot.user:
        await interaction.response.send_message(
            "❌ Vous ne pouvez pas bannir le bot.", ephemeral=True
        )
        return

    # Tentative de bannissement
    try:
        await member.ban(reason=reason)
        embed = discord.Embed(
            title="Utilisateur banni",
            description=f"{member.mention} a été banni avec succès.\n\n**Raison** : {reason}",
            color=discord.Color.purple()
        )
        # Image par défaut intégrée dans l'embed
        embed.set_image(url="https://i.pinimg.com/originals/44/ca/a3/44caa3a1f18ef057b7a3dabe994d1d56.gif")
        embed.set_footer(text=f"Banni par {interaction.user}")

        await interaction.response.send_message(embed=embed)
    except discord.Forbidden:
        await interaction.response.send_message(
            "❌ Je n'ai pas la permission de bannir cet utilisateur.", ephemeral=True
        )
    except Exception as e:
        await interaction.response.send_message(
            f"❌ Une erreur est survenue : {e}", ephemeral=True)
    







# Événement : le bot est prêt
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot connecté en tant que {bot.user} et commandes slash synchronisées.")

# Commande slash pour afficher les informations du serveur
@bot.tree.command(name="serverinfo", description="Affiche les informations du serveur.")
async def server_info(interaction: discord.Interaction):
    guild = interaction.guild  # Récupérer l'objet du serveur

    # Récupérer le propriétaire du serveur
    owner = guild.owner
    # Nombre de membres
    member_count = guild.member_count
    # Liste des emojis
    emojis = [emoji for emoji in guild.emojis]
    emoji_count = len(emojis)
    # Nombre de boosts
    boosts = guild.premium_subscription_count
    # Nombre de salons (textuels et vocaux)
    channels_count = len(guild.text_channels) + len(guild.voice_channels)
    # Nombre de bots
    bot_count = len([member for member in guild.members if member.bot])
    # Date de création
    created_at = guild.created_at.strftime("%d %B %Y à %H:%M:%S")
    # Liste des rôles (optionnel, vous pouvez afficher certains rôles si nécessaire)
    roles = [role.name for role in guild.roles]
    roles_count = len(roles)

    # Création de l'embed
    embed = discord.Embed(
        title=f"Informations du serveur : {guild.name}",
        color=discord.Color.purple()
    )
    embed.set_thumbnail(url=guild.icon.url if guild.icon else discord.Embed.Empty)
    embed.set_image(url="https://i.pinimg.com/originals/0f/54/ba/0f54babf7a9366335af1febf6e322c18.gif")
    
    embed.add_field(name="Propriétaire", value=f"{owner} (ID: {owner.id})", inline=False)
    embed.add_field(name="Date de création", value=created_at, inline=False)
    embed.add_field(name="Nombre de membres", value=member_count, inline=True)
    embed.add_field(name="Nombre d'emojis", value=emoji_count, inline=True)
    embed.add_field(name="Nombre de rôles", value=roles_count, inline=True)
    embed.add_field(name="Nombre de boosts", value=boosts, inline=True)
    embed.add_field(name="Nombre de salons", value=channels_count, inline=True)
    embed.add_field(name="Nombre de bots", value=bot_count, inline=True)
    
    if emoji_count > 0:
        embed.add_field(name="Liste des emojis", value=", ".join([str(emoji) for emoji in emojis[:5]]) + ("..." if emoji_count > 5 else ""), inline=False)
    
    embed.set_footer(text=f"Commande exécutée par {interaction.user}")

    # Envoi de l'embed
    await interaction.response.send_message(embed=embed)







# Commande slash pour supprimer un nombre spécifique de messages
@bot.tree.command(name="clearchat", description="Supprimer un certain nombre de messages.")
@app_commands.describe(amount="Le nombre de messages à supprimer")
async def clearchat(interaction: discord.Interaction, amount: int):
    # Vérification des permissions
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message(
            "❌ Vous n'avez pas la permission de gérer les messages.", ephemeral=True
        )
        return

    # Vérification si le nombre de messages est raisonnable
    if amount < 1 or amount > 100:
        await interaction.response.send_message(
            "❌ Vous devez spécifier un nombre de messages entre 1 et 100.", ephemeral=True
        )
        return

    # Tentative de suppression des messages
    try:
        deleted = await interaction.channel.purge(limit=amount)
        await interaction.response.send_message(
            f"✅ {len(deleted)} messages ont été supprimés.", ephemeral=True
        )
    except discord.Forbidden:
        await interaction.response.send_message(
            "❌ Je n'ai pas la permission de supprimer des messages dans ce canal.", ephemeral=True
        )
    except Exception as e:
        await interaction.response.send_message(
            f"❌ Une erreur est survenue : {e}", ephemeral=True
        )



# Commande slash pour créer un ticket
@bot.tree.command(name="ticket", description="Créer un ticket pour obtenir de l'aide.")
async def ticket(interaction: discord.Interaction):
    # Créer un canal privé pour le ticket
    guild = interaction.guild
    category = discord.utils.get(guild.categories, name="Tickets")

    if not category:
        category = await guild.create_category(name="Tickets")
    
    # Créer le canal du ticket
    ticket_channel = await guild.create_text_channel(
        name=f"ticket-{interaction.user.name}",
        category=category,
        overwrites={
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True)
        }
    )

    # Créer un bouton pour fermer le ticket
    close_button = Button(label="Fermer le ticket", style=discord.ButtonStyle.danger)

    # Vue pour le bouton
    async def close_ticket(interaction: discord.Interaction):
        # Vérifier que seul l'utilisateur ayant créé le ticket ou un administrateur peut fermer
        if interaction.user != ticket_channel.guild.owner and interaction.user != interaction.user:
            await interaction.response.send_message("❌ Vous n'avez pas la permission de fermer ce ticket.", ephemeral=True)
            return
        await ticket_channel.delete()
        await interaction.response.send_message("✅ Le ticket a été fermé.", ephemeral=True)

    close_button.callback = close_ticket
    view = View(timeout=None)
    view.add_item(close_button)

    # Créer un embed pour le ticket
    embed = discord.Embed(
        title="Ticket créé",
        description=f"Un ticket a été créé pour {interaction.user.mention}.",
        color=discord.Color.blue()
    )
    embed.set_image(url="https://i.pinimg.com/originals/1e/0c/a8/1e0ca8992fd175911ef40ccc66212c39.gif")
    embed.set_footer(text=f"Ticket créé par {interaction.user}")

    # Envoyer l'embed dans le canal du ticket
    await ticket_channel.send(embed=embed, view=view)

    # Confirmer à l'utilisateur que le ticket a été créé
    await interaction.response.send_message(f"✅ Votre ticket a été créé dans {ticket_channel.mention}.")

@bot.tree.command(name="regles", description="Affiche les règles du serveur avec une image.")
async def regles(interaction: discord.Interaction):
    # Définir le texte des règles
    regles_message = (
        "**Règles du serveur :**\n\n"
        "1. Soyez respectueux envers les autres membres.\n"
        "2. Pas de spam ou de contenu inapproprié.\n"
        "3. Suivez les consignes des modérateurs.\n"
        "4. Utilisez les salons selon leur objectif.\n"
        "5. Toute violation des règles peut entraîner des sanctions.\n\n"
        "6. Les rôles sont obligatoires.\n"
        "Merci de respecter ces règles pour maintenir une communauté saine !"
    )

    # Définir l'URL ou le fichier local de l'image des règles
    image_url = "https://i.pinimg.com/736x/9c/52/eb/9c52eb5ad87053b29cb121a89565a586.jpg"

    # Créer un embed pour afficher les règles et l'image
    embed = discord.Embed(
        title="Bienvenue sur Fubuki !",
        description=regles_message,
        color=discord.Color.purple()
    )
    embed.set_image(url=image_url)
    embed.set_footer(text=f"Commandé par {interaction.user}")

    # Envoyer l'embed dans le salon
    await interaction.response.send_message(embed=embed)


@bot.command(name="avatar", help="Afficher la photo de profil d'un membre.")
async def avatar(ctx, member: discord.Member = None):
    # Si aucun membre n'est mentionné, utiliser l'auteur de la commande
    if member is None:
        member = ctx.author

    # Créer un embed avec la photo de profil du membre
    embed = discord.Embed(
        title=f"Photo de profil de {member.display_name}",
        color=discord.Color.purple()
    )
    embed.set_image(url=member.avatar.url)  # Ajouter l'image de profil à l'embed

    # Envoyer l'embed dans le canal
    await ctx.send(embed=embed)


#Liste pour enregistrer les messages supprimés
deleted_messages = []

# Événement : lorsque un message est supprimé
@bot.event
async def on_message_delete(message: discord.Message):
    # Nous n'enregistrons pas les messages du bot ou les messages système
    if message.author.bot:
        return

    # Enregistrer le message supprimé dans la liste
    deleted_messages.append({
        'author': message.author.name,
        'content': message.content,
        'channel': message.channel.name,
        'timestamp': message.created_at.strftime('%Y-%m-%d %H:%M:%S')
    })

# Commande !logs pour voir les messages supprimés
@bot.command(name="snipe", help="Afficher les derniers messages supprimés.")
async def view_deleted_messages(ctx):
    # Vérifier si l'utilisateur a la permission d'accéder aux logs
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("❌ Vous n'avez pas la permission de voir les logs.")
        return

    # Vérifier s'il y a des messages supprimés
    if not deleted_messages:
        await ctx.send("❌ Aucun message supprimé à afficher.")
        return

    # Créer un message pour afficher les logs
    logs = ""
    for log in deleted_messages[-5:]:  # Afficher les 5 derniers messages supprimés
        logs += f"**{log['author']}** a écrit dans {log['channel']} :\n{log['content']}\n[Supprimé à {log['timestamp']}]\n\n"

    await ctx.send(f"**Derniers messages supprimés** :\n{logs}")

@bot.tree.command(name="unban", description="Débannir un utilisateur du serveur.")
@app_commands.describe(user="L'utilisateur à débannir (format : NomUtilisateur#Discriminateur)")
async def unban(interaction: discord.Interaction, user: str):
    # Vérification des permissions
    if not interaction.user.guild_permissions.ban_members:
        await interaction.response.send_message(
            "❌ Vous n'avez pas la permission de débannir des membres.", ephemeral=True
        )
        return

    # Recherche de l'utilisateur banni
    banned_users = await interaction.guild.bans()
    user_to_unban = None
    for ban_entry in banned_users:
        if str(ban_entry.user) == user:
            user_to_unban = ban_entry.user
            break

    if user_to_unban is None:
        await interaction.response.send_message(
            f"❌ Aucun utilisateur banni correspondant à {user}.", ephemeral=True
        )
        return

    # Tentative de débannissement
    try:
        await interaction.guild.unban(user_to_unban)
        embed = discord.Embed(
            title="Utilisateur débanni",
            description=f"{user_to_unban} a été débanni avec succès.",
            color=discord.Color.green()
        )
        embed.set_footer(text=f"Débanni par {interaction.user}")

        await interaction.response.send_message(embed=embed)
    except discord.Forbidden:
        await interaction.response.send_message(
            "❌ Je n'ai pas la permission de débannir cet utilisateur.", ephemeral=True
        )
    except Exception as e:
        await interaction.response.send_message(
            f"❌ Une erreur est survenue : {e}", ephemeral=True
        )

    # Commande slash pour calculer l'amour entre deux membres
@bot.tree.command(name="love", description="Calculer l'amour entre deux membres.")
@app_commands.describe(member1="Le premier membre", member2="Le deuxième membre")
async def love(interaction: discord.Interaction, member1: discord.Member, member2: discord.Member):
    # Calcul aléatoire du score d'amour (entre 0 et 100)
    love_score = random.randint(0, 100)

    # Créer un embed avec les photos de profil des deux membres et le score d'amour
    embed = discord.Embed(
        title="Calcul de l'amour 💖",
        description=f"Voici le score d'amour entre **{member1.display_name}** et **{member2.display_name}** :",
        color=discord.Color.purple()
    )
    
    # Ajouter les photos de profil des deux membres
    embed.set_thumbnail(url=member1.avatar.url)  # Photo de profil du premier membre
    embed.add_field(name=f"{member1.display_name} ❤️ {member2.display_name}", value=f"Score d'amour : **{love_score}%**", inline=False)
    embed.set_image(url=member2.avatar.url)  # Photo de profil du deuxième membre

    # Ajouter un footer avec un message amusant
    embed.set_footer(text="L'amour est dans l'air ✨")

    # Envoyer l'embed
    await interaction.response.send_message(embed=embed)




@bot.tree.command(name="sondage", description="Créer un sondage avec choix multiples.")
@app_commands.describe(question="La question du sondage", options="Les options du sondage séparées par des virgules", mention="Les utilisateurs à mentionner (optionnel)")
async def sondage(interaction: discord.Interaction, question: str, options: str, mention: str = None):
    # Découper les options et vérifier s'il y en a au moins deux
    options_list = [option.strip() for option in options.split(",")]
    if len(options_list) < 2:
        await interaction.response.send_message("❌ Le sondage doit avoir au moins deux options.", ephemeral=True)
        return

    # Créer un message avec la question et les options
    poll_message = f"**{question}**\n\n"
    for index, option in enumerate(options_list, start=1):
        poll_message += f"{index}. {option}\n"

    # Si une mention est fournie, l'ajouter au message
    if mention:
        poll_message = f"{mention} {poll_message}"

    # Envoyer le message du sondage
    poll_message_obj = await interaction.response.send_message(poll_message)

    # Ajouter des réactions correspondant aux options
    emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    for i in range(len(options_list)):
        await poll_message_obj.add_reaction(emojis[i])


# Commande !anime pour générer un personnage d'anime
@bot.command(name="anime")
async def anime(ctx):
    # Utilisation de l'API Multiavatar pour générer un personnage d'anime aléatoire
    # Vous pouvez changer l'URL pour toute autre source API d'avatar d'anime
    url = "https://api.multiavatar.com/your_unique_id.svg"  # Remplacez "your_unique_id" par un identifiant unique pour chaque requête

    # Envoyer l'image générée dans le channel
    embed = discord.Embed(title="Personnage d'Anime Aléatoire")
    embed.set_image(url=url)
    await ctx.send(embed=embed)


# Commande !activity pour changer l'activité du bot
@bot.command(name="activity")
async def activity(ctx, *, activity: str):
    # Modifier l'activité du bot
    await bot.change_presence(activity=discord.Game(name=activity))  # Peut être 'discord.Game', 'discord.Streaming', etc.
    
    # Répondre dans le chat pour confirmer le changement d'activité
    await ctx.send(f"Le statut du bot a été mis à jour : {activity}")


# Événement : quand un membre rejoint le serveur
@bot.event
async def on_member_join(member: discord.Member):
    # Envoie un message en pingant le membre qui vient de rejoindre
    channel = discord.utils.get(member.guild.text_channels, name="⛩・chat・話す")  # Assurez-vous que le salon "general" existe
    if channel:
        await channel.send(f"Bienvenue {member.mention}!comment vas-tu ?! J'espère que le serveur de plaira tu pourras faires tes rôles dans <#1285701721049403403> et accepter les <#1285712154053578904> . Merci d'avance et amuse toi bien ici !")


# Liste des utilisateurs et rôles autorisés
allowed_users = set()
allowed_roles = set()

# Vérification des permissions
async def check_permissions(ctx):
    if ctx.author.id in allowed_users:
        return True

    user_roles = {role.id for role in ctx.author.roles}
    if user_roles.intersection(allowed_roles):
        return True

    await ctx.send("❌ Vous n'êtes pas autorisé à utiliser ce bot.")
    return False

# Commande pour ajouter un utilisateur autorisé
@bot.command(name="adduser")
@commands.has_permissions(administrator=True)
async def add_user(ctx, user: discord.User):
    allowed_users.add(user.id)
    await ctx.send(f"✅ {user.mention} a été ajouté à la liste des utilisateurs autorisés.")

# Commande pour ajouter un rôle autorisé
@bot.command(name="addrole")
@commands.has_permissions(administrator=True)
async def add_role(ctx, role: discord.Role):
    allowed_roles.add(role.id)
    await ctx.send(f"✅ Le rôle `{role.name}` a été ajouté à la liste des rôles autorisés.")

# Commande pour retirer un utilisateur autorisé
@bot.command(name="removeuser")
@commands.has_permissions(administrator=True)
async def remove_user(ctx, user: discord.User):
    allowed_users.discard(user.id)
    await ctx.send(f"✅ {user.mention} a été retiré de la liste des utilisateurs autorisés.")

# Commande pour retirer un rôle autorisé
@bot.command(name="removerole")
@commands.has_permissions(administrator=True)
async def remove_role(ctx, role: discord.Role):
    allowed_roles.discard(role.id)
    await ctx.send(f"✅ Le rôle `{role.name}` a été retiré de la liste des rôles autorisés.")

# Exemple de commande protégée
@bot.command(name="secret")
async def secret_command(ctx):
    if not await check_permissions(ctx):
        return
    await ctx.send("✨ Voici un secret réservé aux utilisateurs autorisés !")

# Gestionnaire d'erreurs pour les commandes
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Vous n'avez pas les permissions nécessaires pour exécuter cette commande.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Il manque un argument obligatoire pour cette commande.")
    elif isinstance(error, commands.UserInputError):
        await ctx.send("❌ Entrée invalide. Vérifiez les arguments fournis.")
    else:
        await ctx.send("❌ Une erreur inattendue s'est produite.")



bot.run(TOKEN)
