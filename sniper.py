import re, discum, httpx, json, time
from colorama import init, Fore

init()

# open config
with open("config.json") as f:
    config = json.load(f)
token = config["token"]
webhook = config["webhook"]

# create a regex to match codes
regex = re.compile(
    "(discord.com/gifts/|discordapp.com/gifts/|discord.gift/)([a-zA-Z0-9]+)"
)

# create a discord client
sniper = discum.Client(token=token, log=False)


@sniper.gateway.command
def sniping(resp):
    if resp.event.ready_supplemental:
        user = sniper.gateway.session.user
        print(
            Fore.GREEN
            + """
░█▀▀▄ ▀█▀ ░█▀▀▀█ ░█▀▀█ ░█─░█ ░█▀▄▀█ ── ░█▀▀▀█ ░█▄─░█ ▀█▀ ░█▀▀█ ░█▀▀▀ ░█▀▀█  by github.com/Mewzax
░█─░█ ░█─ ─▀▀▀▄▄ ░█─── ░█─░█ ░█░█░█ ▀▀ ─▀▀▀▄▄ ░█░█░█ ░█─ ░█▄▄█ ░█▀▀▀ ░█▄▄▀ 
░█▄▄▀ ▄█▄ ░█▄▄▄█ ░█▄▄█ ─▀▄▄▀ ░█──░█ ── ░█▄▄▄█ ░█──▀█ ▄█▄ ░█─── ░█▄▄▄ ░█─░█"""
            + Fore.RESET
        )
        print(
            Fore.LIGHTCYAN_EX
            + "Sniping on {}#{} on {} servers 🎯\n".format(
                user["username"],
                user["discriminator"],
                len(sniper.gateway.session.guilds),
            )
            + Fore.RESET
        )
    if resp.event.message:
        m = resp.parsed.auto()
        user = sniper.gateway.session.user
        guildID = m["guild_id"] if "guild_id" in m else None
        channelID = m["channel_id"]

        if guildID:
            guild = sniper.gateway.session.guild(guildID)
            guildName = guild.name
            channel = sniper.getChannel(channelID).json()
            channelName = channel["name"]

        username = m["author"]["username"]
        discriminator = m["author"]["discriminator"]
        content = m["content"]

        startTime = time.time()

        if regex.search(content):
            code = regex.search(content).group(2)

            if len(code) < 16 or len(code) > 24:
                if "guild_id" in m:
                    print(
                        Fore.LIGHTRED_EX
                        + "[-] Fake Code: "
                        + Fore.RED
                        + code
                        + Fore.LIGHTRED_EX
                        + " from "
                        + username
                        + "#"
                        + discriminator
                        + Fore.RESET
                        + " Delay: "
                        + Fore.LIGHTGREEN_EX
                        + str(time.time() - startTime)
                        + "s"
                        + Fore.CYAN
                        + " ["
                        + guildName
                        + " > "
                        + channelName
                        + "]"
                        + Fore.RESET
                    )
                    # send a webhook with embed
                    httpx.post(
                        webhook,
                        json={
                            "username": user["username"],
                            "embeds": [
                                {
                                    "title": "Fake Code",
                                    "description": code,
                                    "color": 0xFFA500,
                                    "footer": {
                                        "text": "Sniper: "
                                        + user["username"]
                                        + "#"
                                        + user["discriminator"]
                                        + " | Author: "
                                        + username
                                        + "#"
                                        + discriminator
                                    },
                                    "fields": [
                                        {
                                            "name": "User",
                                            "value": "{}#{}".format(
                                                username, discriminator
                                            ),
                                            "inline": False,
                                        },
                                        {
                                            "name": "Guild",
                                            "value": guildName,
                                            "inline": False,
                                        },
                                        {
                                            "name": "Channel",
                                            "value": channelName,
                                            "inline": False,
                                        },
                                        {
                                            "name": "Delay",
                                            "value": str(time.time() - startTime) + "s",
                                            "inline": False,
                                        },
                                    ],
                                }
                            ],
                        },
                    )

                else:
                    print(
                        Fore.LIGHTRED_EX
                        + "Fake Code: "
                        + Fore.RED
                        + code
                        + Fore.LIGHTRED_EX
                        + " from "
                        + username
                        + "#"
                        + discriminator
                        + Fore.RESET
                        + " Delay: "
                        + Fore.LIGHTGREEN_EX
                        + str(time.time() - startTime)
                        + "s"
                        + Fore.CYAN
                        + " [DMs]"
                        + Fore.RESET
                    )

                    # send a webhook with embed
                    httpx.post(
                        webhook,
                        json={
                            "username": user["username"],
                            "embeds": [
                                {
                                    "title": "Fake Code",
                                    "description": code,
                                    "color": 0xFFA500,
                                    "footer": {
                                        "text": "Sniper: "
                                        + user["username"]
                                        + "#"
                                        + user["discriminator"]
                                        + " | Author: "
                                        + username
                                        + "#"
                                        + discriminator
                                    },
                                    "fields": [
                                        {
                                            "name": "User",
                                            "value": "{}#{}".format(
                                                username, discriminator
                                            ),
                                            "inline": False,
                                        },
                                        {
                                            "name": "Channel",
                                            "value": "DMs",
                                            "inline": False,
                                        },
                                        {
                                            "name": "Delay",
                                            "value": str(time.time() - startTime) + "s",
                                            "inline": False,
                                        },
                                    ],
                                }
                            ],
                        },
                    )

            else:

                # get the response
                try:
                    response = httpx.post(
                        "https://discord.com/api/v8/entitlements/gift-codes/{}/redeem".format(
                            code
                        ),
                        headers={
                            "Authorization": token,
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9004 Chrome/91.0.4472.164 Electron/13.6.6 Safari/537.36",
                            "Content-Type": "application/json",
                            "Accept": "*/*",
                            # tired to write more headers lol
                        },
                        json={
                            "channel_id": channelID,
                        },
                    )
                    delay = time.time() - startTime

                except httpx.HTTPError as e:
                    print(e)

                # check if code is valid
                if guildID:
                    if "nitro" in str(response.content):
                        print(
                            Fore.LIGHTGREEN_EX
                            + "[=] Sniped Code: "
                            + Fore.GREEN
                            + code
                            + Fore.LIGHTGREEN_EX
                            + " from "
                            + username
                            + "#"
                            + discriminator
                            + Fore.RESET
                            + " Delay: "
                            + Fore.LIGHTGREEN_EX
                            + str(delay)
                            + "s"
                            + Fore.CYAN
                            + " ["
                            + guildName
                            + " > "
                            + channelName
                            + "]"
                            + Fore.RESET
                        )

                        httpx.post(
                            webhook,
                            json={
                                "username": user["username"],
                                "embeds": [
                                    {
                                        "title": "Sniped Code",
                                        "description": code,
                                        "color": 0x00A000,
                                        "footer": {
                                            "text": "Sniper: "
                                            + user["username"]
                                            + "#"
                                            + user["discriminator"]
                                            + " | Author: "
                                            + username
                                            + "#"
                                            + discriminator
                                        },
                                        "fields": [
                                            {
                                                "name": "User",
                                                "value": "{}#{}".format(
                                                    username, discriminator
                                                ),
                                                "inline": False,
                                            },
                                            {
                                                "name": "Guild",
                                                "value": guildName,
                                                "inline": False,
                                            },
                                            {
                                                "name": "Channel",
                                                "value": channelName,
                                                "inline": False,
                                            },
                                            {
                                                "name": "Delay",
                                                "value": str(delay) + "s",
                                                "inline": False,
                                            },
                                        ],
                                    }
                                ],
                            },
                        )

                    elif "Unknown Gift Code" in str(response.content):
                        print(
                            Fore.LIGHTRED_EX
                            + "[x] Invalid Code: "
                            + Fore.RED
                            + code
                            + Fore.LIGHTRED_EX
                            + " from "
                            + username
                            + "#"
                            + discriminator
                            + Fore.RESET
                            + " Delay: "
                            + Fore.LIGHTGREEN_EX
                            + str(delay)
                            + "s"
                            + Fore.CYAN
                            + " ["
                            + guildName
                            + " > "
                            + channelName
                            + "]"
                            + Fore.RESET
                        )

                        # send webhook with embed
                        httpx.post(
                            webhook,
                            json={
                                "username": user["username"],
                                "embeds": [
                                    {
                                        "title": "Invalid Code",
                                        "description": code,
                                        "color": 0xFF0000,
                                        "footer": {
                                            "text": "Sniper: "
                                            + user["username"]
                                            + "#"
                                            + user["discriminator"]
                                            + " | Author: "
                                            + username
                                            + "#"
                                            + discriminator
                                        },
                                        "fields": [
                                            {
                                                "name": "User",
                                                "value": "{}#{}".format(
                                                    username, discriminator
                                                ),
                                                "inline": False,
                                            },
                                            {
                                                "name": "Guild",
                                                "value": guildName,
                                                "inline": False,
                                            },
                                            {
                                                "name": "Channel",
                                                "value": channelName,
                                                "inline": False,
                                            },
                                            {
                                                "name": "Delay",
                                                "value": str(delay) + "s",
                                                "inline": False,
                                            },
                                        ],
                                    }
                                ],
                            },
                        )

                    elif "This gift has been redeemed already." in str(response.content):
                        print(
                            Fore.LIGHTRED_EX
                            + "[-] Already Redeemed: "
                            + Fore.RED
                            + code
                            + Fore.LIGHTRED_EX
                            + " from "
                            + username
                            + "#"
                            + discriminator
                            + Fore.RESET
                            + " Delay: "
                            + Fore.LIGHTGREEN_EX
                            + str(delay)
                            + "s"
                            + Fore.CYAN
                            + " ["
                            + guildName
                            + " > "
                            + channelName
                            + "]"
                            + Fore.RESET
                        )

                        httpx.post(
                            webhook,
                            json={
                                "username": user["username"],
                                "embeds": [
                                    {
                                        "title": "Already Redeemed",
                                        "description": code,
                                        "color": 0xFFA500,
                                        "footer": {
                                            "text": "Sniper: "
                                            + user["username"]
                                            + "#"
                                            + user["discriminator"]
                                            + " | Author: "
                                            + username
                                            + "#"
                                            + discriminator
                                        },
                                        "fields": [
                                            {
                                                "name": "User",
                                                "value": "{}#{}".format(
                                                    username, discriminator
                                                ),
                                                "inline": False,
                                            },
                                            {
                                                "name": "Guild",
                                                "value": guildName,
                                                "inline": False,
                                            },
                                            {
                                                "name": "Channel",
                                                "value": channelName,
                                                "inline": False,
                                            },
                                            {
                                                "name": "Delay",
                                                "value": str(delay) + "s",
                                                "inline": False,
                                            },
                                        ],
                                    }
                                ],
                            },
                        )

                else:
                    if "nitro" in str(response.content):
                        print(
                            Fore.LIGHTGREEN_EX
                            + "[=] Sniped Code: "
                            + Fore.GREEN
                            + code
                            + Fore.LIGHTGREEN_EX
                            + " from "
                            + username
                            + "#"
                            + discriminator
                            + Fore.RESET
                            + " Delay: "
                            + Fore.LIGHTGREEN_EX
                            + str(delay)
                            + "s"
                            + Fore.CYAN
                            + " [DMs]"
                            + Fore.RESET
                        )
                        httpx.post(
                            webhook,
                            json={
                                "username": user["username"],
                                "embeds": [
                                    {
                                        "title": "Sniped Code",
                                        "description": code,
                                        "color": 0x00A000,
                                        "footer": {
                                            "text": "Sniper: "
                                            + user["username"]
                                            + "#"
                                            + user["discriminator"]
                                            + " | Author: "
                                            + username
                                            + "#"
                                            + discriminator
                                        },
                                        "fields": [
                                            {
                                                "name": "User",
                                                "value": "{}#{}".format(
                                                    username, discriminator
                                                ),
                                                "inline": False,
                                            },
                                            {
                                                "name": "Channel",
                                                "value": "DMs",
                                                "inline": False,
                                            },
                                            {
                                                "name": "Delay",
                                                "value": str(delay) + "s",
                                                "inline": False,
                                            },
                                        ],
                                    }
                                ],
                            },
                        )

                    elif "Unknown Gift Code" in str(response.content):
                        print(
                            Fore.LIGHTRED_EX
                            + "[x] Invalid Code: "
                            + Fore.RED
                            + code
                            + Fore.LIGHTRED_EX
                            + " from "
                            + username
                            + "#"
                            + discriminator
                            + Fore.RESET
                            + " Delay: "
                            + Fore.LIGHTGREEN_EX
                            + str(delay)
                            + "s"
                            + Fore.CYAN
                            + " [DMs]"
                            + Fore.RESET
                        )
                        httpx.post(
                            webhook,
                            json={
                                "username": user["username"],
                                "embeds": [
                                    {
                                        "title": "Invalid Code",
                                        "description": code,
                                        "footer": {
                                            "text": "Sniper: "
                                            + user["username"]
                                            + "#"
                                            + user["discriminator"]
                                            + " | Author: "
                                            + username
                                            + "#"
                                            + discriminator
                                        },
                                        "color": 0xFF0000,
                                        "fields": [
                                            {
                                                "name": "User",
                                                "value": "{}#{}".format(
                                                    username, discriminator
                                                ),
                                                "inline": False,
                                            },
                                            {
                                                "name": "Channel",
                                                "value": "DMs",
                                                "inline": False,
                                            },
                                            {
                                                "name": "Delay",
                                                "value": str(delay) + "s",
                                                "inline": False,
                                            },
                                        ],
                                    }
                                ],
                            },
                        )

                    elif "This gift has been redeemed already." in str(response.content):
                        print(
                            Fore.LIGHTRED_EX
                            + "[-] Already Redeemed: "
                            + Fore.RED
                            + code
                            + Fore.LIGHTRED_EX
                            + " from "
                            + username
                            + "#"
                            + discriminator
                            + Fore.RESET
                            + " Delay: "
                            + Fore.LIGHTGREEN_EX
                            + str(delay)
                            + "s"
                            + Fore.CYAN
                            + " [DMs]"
                            + Fore.RESET
                        )

                        httpx.post(
                            webhook,
                            json={
                                "username": user["username"],
                                "embeds": [
                                    {
                                        "title": "Already Redeemed",
                                        "description": code,
                                        "footer": {
                                            "text": "Sniper: "
                                            + user["username"]
                                            + "#"
                                            + user["discriminator"]
                                            + " | Author: "
                                            + username
                                            + "#"
                                            + discriminator
                                        },
                                        "color": 0xFFA500,
                                        "fields": [
                                            {
                                                "name": "User",
                                                "value": "{}#{}".format(
                                                    username, discriminator
                                                ),
                                                "inline": False,
                                            },
                                            {
                                                "name": "Channel",
                                                "value": "DMs",
                                                "inline": False,
                                            },
                                            {
                                                "name": "Delay",
                                                "value": str(delay) + "s",
                                                "inline": False,
                                            },
                                        ],
                                    }
                                ],
                            },
                        )


sniper.gateway.run(auto_reconnect=True)
