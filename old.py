import discord
from discord.ext import commands

TOKEN = "Discord Bot Token"

client = discord.Client()

@client.event
async def on_ready():
    print("ready")
    # with open('channels.txt') as temp_f:
    #     datafile = temp_f.readlines()
    #     for line in datafile:
    #         print(line)

@client.event
async def on_message(msg):
    if msg.content.startswith("vc추가"):
        if msg.author.guild_permissions.administrator:
            try:
                vc = msg.content.split(" ")[1]
            except:
                return await msg.channel.send("> 추가할 보이스채널 id를 작성해주세요")
            if vc:
                y = open("voice.txt", 'a')
                y.write(f"\n{vc}")
                await msg.channel.send(f"<#{vc}> 채널이 추가되었습니다.")
            else:
                return await msg.channel.send("> 추가할 보이스채널 id를 작성해주세요")
        else:
            return
    if msg.content.startswith("vc삭제"):
        if msg.author.guild_permissions.administrator:
            try:
                vc = msg.content.split(" ")[1]
            except:
                return await msg.channel.send("> 삭제할 보이스채널 id를 작성해주세요")
            if vc:
                with open("voice.txt", "r") as f: lines = f.readlines()
                with open("voice.txt", "w") as f: 
                    for line in lines: 
                        if line.strip("\n") != vc:
                            f.write(line)
                await msg.channel.send(f"<#{vc}> 채널이 삭제되었습니다.")
            else:
                return await msg.channel.send("> 삭제할 보이스채널 id를 작성해주세요")
        else:
            return
    if msg.content.startswith("vc도움말"):
        e = discord.Embed(
            title="Command LIst",
            description="사용해주셔서 감사합니다!",
            color=0x2F3136
        )
        e.add_field(
            name="채널 추가하기",
            value="vc추가 <보이스채널 아이디>"
        )
        e.add_field(
            name="채널 삭제하기",
            value="vc삭제 <보이스채널 아이디>"
        )
        e.set_author(name="Operated by Grander#5023")
        await msg.channel.send(embed=e)

@client.event
async def on_voice_state_update(member, before, after):
    try:
        try:
            c = before.channel.id
            with open('channels.txt') as temp_f:
                datafile = temp_f.readlines()
            for line in datafile:
                if f"{before.channel.id}" in line:
                    chnnel = client.get_channel(c)
                    members = len(chnnel.members)
                    if members == 0:
                        with open("channels.txt", "r") as f: lines = f.readlines()
                        with open("channels.txt", "w") as f: 
                            for line in lines: 
                                if line.strip("\n") != before.channel.id:
                                    f.write(line)
                        await before.channel.delete()
        except:
            pass
        try:
            with open('voice.txt') as temp_f:
                datafile = temp_f.readlines()
            for line in datafile:
                if f"{after.channel.id}" in line:
                    overwrites = {
                        member: discord.PermissionOverwrite(manage_channels=True)
                    }
                    vc = await member.guild.create_voice_channel(name="[🎙️] - 채널을 설정해주세요.", category=member.voice.channel.category, overwrites=overwrites)
                    await member.move_to(vc)
                    chennel = vc.id
                    y = open("channels.txt", 'a')
                    y.write(f"\n{chennel}")
            else:
                pass
        except:
            pass
    except:
        pass


client.run(TOKEN)
