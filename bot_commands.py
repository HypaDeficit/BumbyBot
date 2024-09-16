import discord
from discord.ext import commands
import asyncio
import UserSocket

class RustCommands(commands.Cog): 

    UserData = {}

    def __init__(self, bot):
        #do mysql stuff later i dont feel like doing it now LMAOOOOOOOOOOOOOOO
        self.bot = bot
    
    @commands.command()
    async def Pair(self, ctx, *arg):
        if self.UserData.get(ctx.author.name):
            await ctx.send("You already have a Socket connected, remove it first before pairing again.")
            return
        if len(arg) == 0:
            embeded_msg = discord.Embed(title="Link to your pairing details", description="\n",color=discord.Color.brand_red(),url="https://companion-rust.facepunch.com/login")
            embeded_msg.add_field(name="Pairing", value="In order to pair yourself with rustplus, go to the link at the top and link your steam account.", inline=True)
            embeded_msg.add_field(name = "Sending a proper request", value="Then, copy your: IP, playerID, playerToken, and port. Send another pairing request in the form !pair IP, playerID, playerToken, port ", inline=False)
            embeded_msg.set_footer(text="Responding to " + ctx.author.name, icon_url=ctx.author.avatar)
            await ctx.send(embed=embeded_msg)
            return
        if len(arg) != 4:
            await ctx.send("Error: invalid parameters.")
            return
        currSocket = UserSocket.UserSocket(arg[0], arg[1], arg[2], arg[3])
        self.UserData[ctx.author.name] = currSocket
        await ctx.send("Socket created. If further commands don't work, unpair and pair again in the proper form. If a server wipes or you change server you will have to pair again.")
        
    @commands.command()
    async def send_message(self, ctx, *arg):
        message = ""
        if not(self.UserData.get(ctx.author.name)):
            await ctx.send("You do not have a socket connected. Pair and retry.")
            return
        for i in range(len(arg)):
            message += arg[0]
        socket = self.UserData.get(ctx.author.name)
        try:
            await socket.SendMessage(message, ctx.author.name)
        except:
            embed = discord.Embed(title="Message Failed", description="",color=discord.Color.brand_red())
            embed.add_field(name="",value="Message failed to send, websocket seems to be disconnected.")
            embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            return
        embed = discord.Embed(title="Message Sent", description="",color=discord.Color.brand_green())
        embed.add_field(name="",value="Message sent. If it doesn't appear in game, then your socket is expired.")
        embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)
        return
        
            