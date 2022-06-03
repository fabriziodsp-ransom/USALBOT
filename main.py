import asyncio
import discord
from discord.ext import commands
from discord.ext.tasks import loop
import datetime
import time

bot = commands.Bot(command_prefix='/', description="Ejecuta acciones del bot.")
reminders = {}


def unix_to_human(unixtimestamp):
    return time.mktime(unixtimestamp)


def human_timestamp(month, day):
    return datetime.date(int(datetime.date.today().year), month, day)


def unix_timestamp(human):
    return time.mktime(human.timetuple())


@loop(count=None, seconds=20)
async def check_calendar(ctx):
    count = 0
    print("I'm checking")
    for date in reminders.keys():
        count += 1
        if date <= time.time():
            ctx.send("Se acerca la evaluación de {}".format(reminders.get(count)))


@check_calendar.before_loop
async def before_check_calendar():
    await bot.wait_until_ready()


@bot.command(name="ayuda")
async def ayuda(ctx):
    await ctx.send("""
        COMANDOS:
            /list_people <- LISTA LOS USUARIOS DEL CANAL ACTUAL
            /set_evaluacion <- CREA UN RECORDATORIO PARA LA EVALUACION
    """)


@bot.command(name="listar_gente")
async def list_people(ctx):
    members = bot.get_all_members()
    await ctx.send("Listando todos los miembros... ")
    for member in members:
        await ctx.send(member)


@bot.command(name="set_evaluacion")
async def set_evaluacion(ctx):
    await ctx.send("¿Para cuando? ¿Qué materia?")
    await ctx.send("FORMATO: DD/MM materia\nEjemplo: 23/04 Analisis I")
    try:
        msg = await bot.wait_for("message", timeout=30)
        msg_content = msg.content.strip().split()
        if len(msg_content) > 0:
            day = 0
            month = 0
            if (int(msg_content[0][:2])-5) <= 0:
                day = (int(msg_content[0][:2])-5) % 30
                month = (int(msg_content[0][3:]) - 1) % 12
            else:
                day = (int(msg_content[0][:2])-5) % 30
                month = int(msg_content[0][3:])
            date = human_timestamp(month, day)
            unix_date = unix_timestamp(date)
            await ctx.send("Registrado.")
            await ctx.send("""
            El recordatorio fue programado para 5 días antes de la fecha.
            -> {} AAAA/MM/DD
            """.format(date))
            reminders.update({
                "Materia": msg_content[1],
                "Fecha": unix_date
            })
            print(reminders)
    except asyncio.TimeoutError:
        await ctx.send("Dos cosas: O no entendí o no enviaste un mensaje")


async def on_ready():
    await bot.wait_until_ready()
    game = discord.Game("#USALizate\n/ayuda")
    await bot.change_presence(status=discord.Status.idle, activity=game)

bot.run('token')
