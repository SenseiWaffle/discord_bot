# bot.py
import os       # Mostly for .env functions
import ast      # Secure dictionary evaluation
import sys      # Shutdown functionality
import json     # Reading JSON files
import locale   # Currency formatting
import random   # RNG
import discord  # Discord references
import requests # URL requests
import youtube_synopsis # Synopsis

from dotenv import load_dotenv        # Load .env file
from contextlib import suppress       # Supression of errors
from discord.ext import commands      # Discord command module
from datetime import datetime, date   # Date and time
from multipledispatch import dispatch # Easy function overloading

# Load sensitive variables from .env file
load_dotenv()
ACC_ID = os.getenv( 'ACC_ID' )
TOKEN = os.getenv( 'DISCORD_TOKEN' )
TENOR_KEY = os.getenv( 'TENOR_KEY' )

# Create bot, specify command prefix, and disable default help command
bot = commands.Bot( command_prefix = '.', help_command = None )

# Set currancy locale
locale.setlocale( locale.LC_ALL, '' )

# Variables
stats = {}              # Initial placeholder for stats
file_name = "stats.txt" # File to store long term variables
bard_audio_max = 23     # Current highest audio file number
tenor_limit = 50        # Only search for and chose from the top 'n' gifs

bard_audio_path = '.\\boop\\'
#synopsis_path ='..\\Synopsis\\src\\synopsis_tfeng001.py'

boba_dict = { # Used in costofliving, list of "known" bobas
    "almond black milk tea" : 3.85,
    "honey green milk tea" : 3.60,
    "thai milk tea" : 3.85,
    "mango green milk tea" : 3.85,
    "peach green milk tea" : 3.85,
    "royal milk tea" : 4.00,
    "taro milk tea" : 3.85,
    "classic black milk tea" : 3.60,
    "green milk tea" : 3.60
    }

ss_vc_IDs = [             # Sweat Squad voice channel IDs
    "717465012989591607", # army
    "721194405205114970", # once
    "721234377568419892", # moomoo
    "721234507964874754", # midzy
    "721234872534040576", # blink
    "721234943337824337", # monbebe
    "782467719852589098"  # uaena
    ]

welcome_messages = [
        'i\'m not stuck in here with you, you\'re stuck iN HERE WITH ME',
        'FIVE MINUTES IN THE RING',
        'UAV online',
        'tfti'
        ]

purdue_messages = [
    'https://engineering.purdue.edu/ECN/Support/KB/Docs/PurduePeteHistory/face1.jpg',
    'https://engineering.purdue.edu/ECN/Support/KB/Docs/PurduePeteHistory/indexLogo.jpg',
    'https://theblacksheeponline.com/wp-content/uploads/2015/09/Screen-Shot-2015-09-22-at-11.17.56-AM.png',
    'https://cdn1.vox-cdn.com/uploads/chorus_asset/file/4140050/PurduePete_Full.0.jpg',
    'https://www.purduealumnus.org/wp-content/uploads/Mascot_750x400.jpg',
    'https://www3.pictures.gi.zimbio.com/Big+Ten+Tournament+Semifinals+c_B5No4pWRxm.jpg'
    ]

iu_messages = [
    'https://media1.tenor.com/images/7535bc73b7f9220c980f3edacee9261e/tenor.gif?itemid=16215337',
    'https://media1.tenor.com/images/c3af172b51545156d7d211a2d07455a4/tenor.gif?itemid=17223449',
    'https://media1.tenor.com/images/30582683d7d4a6663c08dbeefba0413b/tenor.gif?itemid=5548690',
    'https://media1.tenor.com/images/45084a59437e75ec384fd806cf8ba874/tenor.gif?itemid=14988718',
    'https://media1.tenor.com/images/91cb4020e87338310c955ae1a71b3189/tenor.gif?itemid=14994446',
    'https://media1.tenor.com/images/239125fca9610c77011cc9658cf06fc4/tenor.gif?itemid=11159215',
    'https://media1.tenor.com/images/fc74d265bbdc0ab56ff4c2f43bff45f8/tenor.gif?itemid=15704317',
    'https://media1.tenor.com/images/6a41c6f89e91f88ed50db1d3d1ed3303/tenor.gif?itemid=17236541',
    'https://media1.tenor.com/images/9ef1b4893d5f9126a1a8ed1ba008adb4/tenor.gif?itemid=17223801',
    'https://media1.tenor.com/images/25a341ea280e366874f142b7465aa5f2/tenor.gif?itemid=15066004'
    ]

dynamite_triggers = [
    'dynamite', 'milk', 'rock', 'roll',
    'kong', 'stone',
    'sing', 'song', 'home',
    'lebron', 'ding', 'dong',
    'ping', 'pong'
]

dynamite_copypasta = '𝓢𝓱𝓸𝓮𝓼 𝓸𝓷, 𝓰𝓮𝓽 𝓾𝓹 𝓲𝓷 𝓽𝓱𝓮 𝓶𝓸𝓻𝓷\'\n\
𝓒𝓾𝓹 𝓸𝓯 𝓶𝓲𝓵𝓴, 𝓵𝓮𝓽\'𝓼 𝓻𝓸𝓬𝓴 𝓪𝓷𝓭 𝓻𝓸𝓵𝓵\n\
𝓚𝓲𝓷𝓰 𝓚𝓸𝓷𝓰, 𝓴𝓲𝓬𝓴 𝓽𝓱𝓮 𝓭𝓻𝓾𝓶, 𝓻𝓸𝓵𝓵𝓲𝓷𝓰 𝓸𝓷 𝓵𝓲𝓴𝓮 𝓪 𝓡𝓸𝓵𝓵𝓲𝓷𝓰 𝓢𝓽𝓸𝓷𝓮\n\
𝓢𝓲𝓷𝓰 𝓼𝓸𝓷𝓰 𝔀𝓱𝓮𝓷 𝓘\'𝓶 𝔀𝓪𝓵𝓴𝓲𝓷𝓰 𝓱𝓸𝓶𝓮\n\
𝓙𝓾𝓶𝓹 𝓾𝓹 𝓽𝓸 𝓽𝓱𝓮 𝓽𝓸𝓹, 𝓛𝓮𝓑𝓻𝓸𝓷\n\
𝓓𝓲𝓷𝓰 𝓭𝓸𝓷𝓰, 𝓬𝓪𝓵𝓵 𝓶𝓮 𝓸𝓷 𝓶𝔂 𝓹𝓱𝓸𝓷𝓮\n\
𝓘𝓬𝓮 𝓽𝓮𝓪 𝓪𝓷𝓭 𝓪 𝓰𝓪𝓶𝓮 𝓸𝓯 𝓹𝓲𝓷𝓰 𝓹𝓸𝓷𝓰'

twitch_prime_copypasta = 'DID YOU KNOW YOU CAN USE YOUR AMAZON PRIME ACCOUNT \
TO SUB TO YOUR FAVORITE STREAMER ON http://TWITCH.TV ?! #PrimeDay'

not_a_bot = 'but could a bot do this?\n\
```⊂_ヽ\n\
　 ＼＼ ＿\n\
　　 ＼(　•_•) F\n\
　　　 <　⌒ヽ A\n\
　　　/ 　 へ＼ B\n\
　　 /　　/　＼＼ U\n\
　　 ﾚ　ノ　　 ヽ_つ L\n\
　　/　/ O\n\
　 /　/| U\n\
　(　(ヽ S\n\
　|　|、＼\n\
　| 丿 ＼ ⌒)\n\
　| |　　) /\n\
`ノ )　　Lﾉ\n\
(_／```'

threat_messages = [
    '(っ◔◡◔)っ ♥ *bard noise* ♥',
    '𝕙𝕒𝕙𝕒 𝕔𝕙𝕚𝕞𝕖𝕤',
    '*bₐᵣdᵢₙg ᵢₙₜₑₙₛᵢfᵢₑₛ*',
    'me when i collect chimes: (ﾉ◕ヮ◕)ﾉ*❤:♡ﾟ ✧ﾟ･',
    '```  ▄▄                               ▄▄  \n\
 ▄██                             ▀███  \n\
  ██                               ██  \n\
  ██▄████▄ ▀███▄███ ▄█▀██▄    ▄█▀▀███  \n\
  ██    ▀██  ██▀ ▀▀██   ██  ▄██    ██  \n\
  ██     ██  ██     ▄█████  ███    ██  \n\
  ██▄   ▄██  ██    ██   ██  ▀██    ██  \n\
  █▀█████▀ ▄████▄  ▀████▀██▄ ▀████▀███▄\n```'
    ]



""" Connected to Discord """
@bot.event
async def on_ready():
    # Connection confirmation message
    print( "{} - {} has connected to Discord".format( timestamp(), bot.user.name ) )

    # Open and locally store data for stats and send confirmation message
    file = open( file_name, 'r' )
    global stats
    stats = ast.literal_eval( file.read() )
    file.close
    print( "{} - bard remembered".format( timestamp() ) )



class Text( commands.Cog ):
    """ Personalized embedded help message """
    @commands.command( name = 'help' )
    async def help( self, ctx ):
        # Create embedded message with title and discription
        help_msg = discord.Embed( title = "how to play bard", description = "step 1: staying bot is optional\nstep 2:", color = 0xFFEBA4 )

        # Format:
        # help_msg.add_field( name = "", value = "", inline = True )

        # Text commands
        help_msg.add_field( name = "stats", value = "Displays how many chimes bard has collected and who owes who boba.", inline = True )
        help_msg.add_field( name = "boba", value = "Updates who owes who boba (Cha for Tea or Sharetea only).", inline = True )
        help_msg.add_field( name = "costofliving", value = "How much it would cost to pay off the boba debt?\
        If given an amount and drink, barista bard will calculate the total. Type \".costofliving drinks\" for a list of available drinks.", inline = True )

        # Voice commands
        help_msg.add_field( name = "invade", value = "Joins the user's voice channel.", inline = True )
        help_msg.add_field( name = "int", value = "Leaves the voice channel.", inline = True )
        help_msg.add_field( name = "boop", value = "Plays a bard noise.", inline = True )
        help_msg.add_field( name = "tunnel", value = "Moves the user to a different voice channel.", inline = True )

        # [REDACTED]
        help_msg.add_field( name = "|| [REDACTED] ||", value = "Authorizes use of || [REDACTED] ||. Last recorded use: || ／ ／ ||." )

        # Footer
        help_msg.set_footer( text = "Some commands or messages will have additional effects. Use bard at your own discretion." )

        # Send help message then log action
        await ctx.channel.send( embed = help_msg )
        log( "help", ctx.message.author )

    """ Stats command """
    @commands.command( name = 'stats', pass_context = True )
    async def stats( self, ctx ):
        increase_chimes()

        # Read from file
        #file = open( file_name, 'r' )
        #stats = ast.literal_eval( file.read() )

        # Formatted stats message
        stats_msg = "bard has collected {} chimes. {} needs to buy {} {} bobas.".format( stats[ 'chimes' ], stats[ 'boba_loser' ], stats[ 'boba_winner' ], stats[ 'boba_count' ] )

        # Send message and log
        await ctx.send( stats_msg )
        log( "stats", ctx.message.author )

    """ Boba tracker """
    @commands.command( name = 'boba', pass_context = True )
    async def boba( self, ctx, loser, winner ):
        increase_chimes()

        # Open file and read data
        #file = open( file_name, 'r' )
        #stats = ast.literal_eval( file.read() )

        # Set new values
        stats[ 'boba_winner' ] = winner
        stats[ 'boba_loser' ] = loser
        stats[ 'boba_count' ] = stats[ 'boba_count' ] * 2

        # Record new values
        file = open( file_name, "w" )
        file.write( repr( stats ) )

        # Send update message and log
        await ctx.send( "now {} owes {} {} bobas".format( stats[ 'boba_loser' ], stats[ 'boba_winner' ], stats[ 'boba_count' ] ) )
        log( "boba update", ctx.message.author )

    """ Boba cost calculator """
    @commands.command( name = 'costofliving', pass_context = True )
    async def costofliving( self, ctx, *args ):
        increase_chimes()

        # Variables
        boba_num = 0
        boba_type = "classic black milk tea"
        location = "cha for tea"
        boba_cost = 3.60
        tota_cost = 0
        boba_response = ""

        if( len( args ) == 2 and args[ 1 ] in boba_dict ): # If two arguments passed and drink recognized
            boba_type = args[ 1 ]
            boba_cost = boba_dict[ boba_type ]
            boba_num = int( args[ 0 ] )
        elif( len( args ) == 1 and args[ 0 ] == "drinks" ): # If help argument passed
            await ctx.channel.send( "here are the available drinks:\n" + ", ".join( boba_dict.keys() ) )
            return
        elif( len( args ) <= 0 ): # If no arguments passed
            boba_num = stats[ 'boba_count' ]
        else: # All other cases
            boba_response = "ngl not sure what you just said to me but here are the drinks I recognize:\n" + ", ".join( boba_dict.keys() )
            await ctx.channel.send( boba_response )
            return

        # Calculate total based on given arguments and format response
        total_cost = locale.currency( boba_num * boba_cost, grouping = True )
        boba_response = "{} {}s at {} would cost {} before tax".format( boba_num, boba_type, location, total_cost )

        # Send message and log
        await ctx.channel.send( boba_response )
        log( "cost of living", ctx.message.author )

    """ Synopsis """
    @commands.command( name = 'synopsis', pass_context = True )
    async def synopsis( self, ctx, *args ):
        #command = 'python {} '.format( synopsis_path )
        syn_args = []

        if len( args ) == 1:   # If only serach phrase given
            syn_args.extend( ( args[0], ' 100 rec' ) )
        elif len( args ) == 3: # If all arguments given
            syn_args.extend( ( args[0], args[1], args[2] ) )
        else:
            await ctx.channel.send( "the sysnopsis command accepts a **'search phrase'** (in 'single quotes') or **'search phrase' number_of_lines format**." )
            return
        print( syn_args )
        await ctx.channel.send( file=discord.File( await youtube_synopsis.youtube_synopsis.main(syn_args) ) ) # Call synopsis
        log( "synopsis", ctx.message.author )

    """ Shutdown command """
    @commands.command( name = 'shutdown', pass_context = True )
    async def shutdown( self, ctx ):
        if( ctx.author.id == int( ACC_ID ) ):
            log( "shutdown", ctx.message.author )
            sys.exit( "bard main successful shutdown." )

    """ On_message procs """
    @commands.Cog.listener()
    async def on_message( self, message ):
        # Ignore own messages
        if( message.author == bot.user ):
            return

        # Store message.content.lower() in a variables
        original_msg = message.content
        lowered_msg = message.content.lower()

        # Purdue procs
        if( 'purdue' in lowered_msg ):
            await message.channel.send( random.choice( purdue_messages ) )
            log( message.author, "purdue" )

        # IU procs
        if( 'iu' in lowered_msg ):
            await message.channel.send( get_gif( "iu" ) )
            log( message.author, "iu" )

        # val when
        if( 'val when' in lowered_msg ):
            await message.channel.send( "ok getting on rn" )
            log( message.author, '"val when"' )

        # you're finally awake
        if( 'awake' in lowered_msg ):
            await message.channel.send( 'You were trying to cross the border, right? Walked right into that Imperial ambush, same as us, and that thief over there.' )
            log( message.author, "\"you're finally awake\"" )

        # dynamite triggers
        if( any( word in lowered_msg for word in dynamite_triggers ) ):
            if( random.randint( 0, 1 ) == 0 ):
                await message.channel.send( dynamite_copypasta )
            else:
                await message.channel.send( get_gif( "bts dynamite" ) )
            log( message.author, "dynamite" )

        # twitch prime
        if( 'babiemouse' in lowered_msg or 'twitch' in lowered_msg ):
            await message.channel.send( twitch_prime_copypasta )
            log( message.author, "twitch prime" )

        # but could a bot do this?
        if( 'bot' in lowered_msg ):
            await message.channel.send( not_a_bot )
            log( message.author, "not a bot" )

        # AAA
        #if( lowered_msg.count( 'a' ) == 3 ):
        #    await message.channel.send( original_msg.replace( "a", "A" ) )
        #    log( message.author, "aaa" )

        # chime react
        if( random.randint( 0, 19 ) == 0 ):
            emoji = discord.utils.get( message.guild.emojis, name = 'chime' )
            await message.add_reaction( emoji )
            log( message.author, "chime" )

        # Random message proc. Messages chosen from 'threat_messages'
        if( random.randint( 0, 199 ) == 0 ):
            await message.channel.send( random.choice( threat_messages ) )
            log( message.author, "hidden message" )



class Voice( commands.Cog ):
    """ Join user's voice channel """
    @commands.command( name = 'invade', help = 'Join the current voice channel', pass_context = True )
    async def invade( self, ctx ):
        increase_chimes()
        channel = ctx.message.author.voice.channel

        await channel.connect()
        log( "invade", ctx.message.author )

    """ Leave user's voice channel. Activated with '!int' but function is called 'leave' """
    @commands.command( name = 'int', help = 'Leave the current voice channel' )
    async def leave( self, ctx ):
        increase_chimes()
        server = ctx.message.guild.voice_client

        await server.disconnect()
        log( "int", ctx.message.author )

    """ Play Bard audio clips """
    @commands.command( name = 'boop', help = 'Plays Bard noises' )
    async def boop( self, ctx ):
        # Get a random audio file each time
        file_number = str( random.randint( 1, bard_audio_max ) )
        audio_file = bard_audio_path + file_number + ".mp3"

        source = discord.PCMVolumeTransformer( discord.FFmpegPCMAudio( audio_file ) )

        ctx.voice_client.play( source )
        if( int( file_number ) > 20 ):
            log( ctx.message.author, "special boop" )
        else:
            log( "boop", ctx.message.author )

    """ Move bard and another user to a random different voice channel """
    @commands.command( name = 'tunnel', help = 'Bard creates a tunnel to a different voice channel' )
    async def tunnel( self, ctx ):
        # Get all voice channel IDs
        voice_channels = ctx.guild.voice_channels

        # If the server has 1 or less voice channels, return
        if( len( voice_channels ) <= 1 ):
            return

        # Get the voice channel of the author
        target_user = ctx.message.author
        member_vc = target_user.voice.channel

        # Randomly select a voice channel and ensure it is different
        target_voice_channel = random.choice( voice_channels )
        while( target_voice_channel == member_vc ):
            target_voice_channel = random.choice( voice_channels )

        # Get a list of users in the voice channel and randomly select one, 10% chance to proc
        if( random.randint( 1, 10 ) == 1 ):
            member_list = member_vc.voice_states.keys()
            target_user = ctx.guild.get_member( random.choice( list( member_list ) ) )

            await target_user.move_to( target_voice_channel )
            log( "tunnel", ctx.message.author, target_user ) # Special log
        else:
            log( "tunnel", ctx.message.author )
            await target_user.move_to( target_voice_channel ) # Normal log

""" TenorGIF retriever """
def get_gif( target ):
    gif = requests.get( "https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s" % ( target, TENOR_KEY, tenor_limit ) )

    response = json.loads( gif.content )
    with suppress( Exception, discord.HTTPException ):
        return response[ 'results' ][ random.randint( 0, 49 ) ][ 'media' ][ 0 ][ 'gif' ][ 'url' ]

""" Increase chime number by one """
def increase_chimes():
    #file = open( file_name, 'r' )
    #stats = ast.literal_eval( file.read() )
    stats[ 'chimes' ] = stats[ 'chimes' ] + 1

    file = open( file_name, 'w' )
    file.write( repr( stats ) )
    file.close

""" Formatted local date and time """
def timestamp():
    today = date.today()
    time = datetime.now()

    current_date = today.strftime( "%Y-%b-%d " )
    current_time = time.strftime( "%H:%M:%S" )

    return current_date + current_time

""" Print formatted log of time and command run """
@dispatch( str, discord.Member )
def log( command, member ):
    print( "{} - {} run by {}".format( timestamp(), command, member ) )

""" Special log for member activated RNG """
@dispatch( str, discord.Member, discord.Member )
def log( command, member, fool ):
    print( "{} - {} run by {}, additional proc on {}".format( timestamp(), command, member, fool ) )

""" Special log for passive RNG """
@dispatch( discord.Member, str )
def log( member, command ):
    print( "{} - {} procced by {}".format( timestamp(), command, member ) )

bot.add_cog( Text( bot ) )
bot.add_cog( Voice( bot ) )
bot.run(TOKEN)
