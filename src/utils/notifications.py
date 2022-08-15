# https://github.com/Reecepbcups/minecraft-panel/blob/main/src/utils/notifications.py
# https://github.com/Reecepbcups/validator-stats-notifs/blob/main/src/utils/notifications.py

from discord_webhook import DiscordWebhook, DiscordEmbed

def discord_notification(url="", title="", description="", color="ffffff", values={}, imageLink="", footerText=""):
    webhook = DiscordWebhook(url=url)
    
    embed = DiscordEmbed(
        title=title, 
        description=description, 
        color=color
    )   
    # # set thumbnail
    embed.set_thumbnail(url=imageLink)
    
    embed.set_footer(text=footerText)
    # embed.set_timestamp()

    if len(values.items()) > 0:
        for k, v in values.items():
            embed.add_embed_field(name=k, value=v[0], inline=v[1])

    webhook.add_embed(embed)
    response = webhook.execute()


if __name__ == "__main__":
    discord_notification(
        "https://discord.com/api/webhooks/000/kkkkkkk",
        "Oni Validator Stats",
        "desc",
        "D04045",
        {"test": ["value", False]},
        "https://pbs.twimg.com/profile_images/1522666990170746881/OHpOzKDD_400x400.jpg",
        "The Oni Protectorate ⚛️\nValidator for the Cosmos. Friend to the Cosmonaut."
    )
    pass