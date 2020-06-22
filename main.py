
'''
using discord.py version 1.0.0a
'''
import discord
import asyncio
import re
import multiprocessing
import threading
import concurrent

BOT_OWNER_ROLE = 'THP RUNNER' # change to what you need
#BOT_OWNER_ROLE_ID = "658721047729668116" 
  
 

 
oot_channel_id_list = [
'702726686344609852','689311945345859795','691011674181992518','722080589997539368'
]


answer_pattern = re.compile(r'(not|n|e)?([1-3]{1})(\?)?(cnf)?(\?)?$', re.IGNORECASE)

apgscore = 400
nomarkscore = 250
markscore = 156

async def update_scores(content, answer_scores):
    global answer_pattern

    m = answer_pattern.match(content)
    if m is None:
        return False

    ind = int(m[2])-1

    if m[1] is None:
        if m[3] is None:
            if m[4] is None:
                answer_scores[ind] += nomarkscore
            else: # apg
                if m[5] is None:
                    answer_scores[ind] += apgscore
                else:
                    answer_scores[ind] += markscore

        else: # 1? ...
            answer_scores[ind] += markscore

    else: # contains not or n
        if m[3] is None:
            answer_scores[ind] -= nomarkscore
        else:
            answer_scores[ind] -= markscore

    return True

class SelfBot(discord.Client):

    def __init__(self, update_event, answer_scores):
        super().__init__()
        global oot_channel_id_list
        #global wrong
        self.oot_channel_id_list = oot_channel_id_list
        self.update_event = update_event
        self.answer_scores = answer_scores

    async def on_ready(self):
        print("======================")
        print("Nelson Trivia Self Bot")
        print("Connected to discord.")
        print("User: " + self.user.name)
        print("ID: " + str(self.user.id))

    # @bot.event
    # async def on_message(message):
    #    if message.content.startswith('-debug'):
    #         await message.channel.send('d')

        def is_scores_updated(message):
            if message.guild == None or \
                str(message.channel.id) not in self.oot_channel_id_list:
                return False

            content = message.content.replace(' ', '').replace("'", "")
            m = answer_pattern.match(content)
            if m is None:
                return False

            ind = int(m[2])-1

            if m[1] is None:
                if m[3] is None:
                    if m[4] is None:
                        self.answer_scores[ind] += nomarkscore
                    else: # apg
                        if m[5] is None:
                            self.answer_scores[ind] += apgscore
                        else:
                            self.answer_scores[ind] += markscore

                else: # 1? ...
                    self.answer_scores[ind] += markscore

            else: # contains not or n
                if m[3] is None:
                    self.answer_scores[ind] -= nomarkscore
                else:
                    self.answer_scores[ind] -= markscore

            return True

        while True:
            await self.wait_for('message', check=is_scores_updated)
            self.update_event.set()

class Bot(discord.Client):

    def __init__(self, answer_scores):
        super().__init__()
        self.bot_channel_id_list = []
        self.embed_msg = None
        self.embed_channel_id = None
        #global wrong
        self.answer_scores = answer_scores

        # embed creation
        self.embed=discord.Embed(title="**__TRIVIA 𝙷𝙰𝙲𝙺 || ᴘʀᴏ__**", description="**Crowd Search Result!**")
        self.embed.set_author(name ='',url=' ',icon_url='https://images-ext-2.discordapp.net/external/aMZ8_Dhu3Cib5U1l--xzP6QVgEV6bzjPDLMC-gNawWY/https/cdn.discordapp.com/attachments/577373201164795904/585046581506605076/ezgif-2-2f5a82b8174f.gif?width=225&height=225')
        self.embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/721639910745964574/722504944481206342/images_3.jpeg")
        self.embed.add_field(name="__Answer1⃣__", value="✔", inline=False)
        self.embed.add_field(name="__Answer2⃣__", value="✔", inline=False)
        self.embed.add_field(name="__Answer3⃣__", value="✔", inline=False)
        self.embed.set_footer(text=f"Developed By ✞'☬Attitude boy☬✞#1645",\
            icon_url="https://cdn.discordapp.com/avatars/658721047729668116/918ede5902973c5ffeeb397a8c2386ae.png?size=1024")
        self.embed.add_field(name="**Answer:-**:-", value="100", inline=True)

        #await self.bot.add_reaction(embed,':spy:')


    async def clear_results(self):
        for i in range(len(self.answer_scores)):
            self.answer_scores[i]=0

    async def update_embeds(self):
      #  global wrong

         

        one_check = ""
        two_check = ""
        three_check = ""
        best_answer = ' :arrows_counterclockwise: '
        

        lst_scores = list(self.answer_scores)
        

        highest = max(lst_scores)
        best_answer = ' :arrows_counterclockwise: '
        lowest = min(lst_scores)
        answer = lst_scores.index(highest)+1
        #global wrong             

        if highest > 0:
            if answer == 1:
                one_check = "<:white_check_mark:601397380507500549>"
                best_answer = ':one:'
            else:
                one_check = "<:x:600303220417626120>"

            if answer == 2:
                two_check = "<:white_check_mark:601397380507500549>"
                best_answer = ':two:'
            else:
                two_check = "<:x:600303220417626120>"

            if answer == 3:
                three_check = "<:white_check_mark:601397380507500549>"
                best_answer =  ':three:'
            else:
                three_check = "<:x:600303220417626120>"

            

        #if lowest < 0:
            #if answer == 1:
                #one_cross = ":x:"
            #if answer == 2:
                #two_cross = ":x:"
            #if answer == 3:
                #three_cross = ":x:"            
 
        self.embed.set_field_at(0, name="__Answer1⃣__", value="**{0}**{1}".format(lst_scores[0], one_check))
        self.embed.set_field_at(1, name="__Answer2⃣__", value="**{0}**{1}".format(lst_scores[1], two_check))
        self.embed.set_field_at(2, name="__Answer3⃣__", value="**{0}**{1}".format(lst_scores[2], three_check))
        self.embed.set_field_at(3, name="**__Google Answer:-__**", value=best_answer, inline= True)


        if self.embed_msg is not None:
            await self.embed_msg.edit(embed=self.embed)

    async def on_ready(self):
        print("==============")
        print("Nelson Trivia")
        print("Connected to discord.")
        print("User: " + self.user.name)
        print("ID: " + str(self.user.id))

        await self.clear_results()
        await self.update_embeds()
        #await self.change_presence(activity=discord.Game(name='with '+str(len(set(self.get_all_members())))+' users'))
        await self.change_presence(activity=discord.Activity(type=1,name="Vedantu Trivia || v ||"))

    async def on_message(self, message):

        # if message is private
        if message.author == self.user or message.guild == None:
            return

        if message.content.lower() == "v":
            #await message.delete()
           # if BOT_OWNER_ROLE in []:
            self.embed_msg = None
            await self.clear_results()
            await self.update_embeds()
            self.embed_msg = \
                await message.channel.send('',embed=self.embed)
                #await self.embed_msg.add_reaction("✔️")
                #await self.embed_msg.add_reaction("✖️")
            self.embed_channel_id = message.channel.id
            #else:
                #await message.channel.send("**Lol** You Not Have permission To Use This **cmd!** :stuck_out_tongue_winking_eye:")
            #return

          

        # process votes
        if message.channel.id == self.embed_channel_id:
            content = message.content.replace(' ', '').replace("'", "")
            updated = await update_scores(content, self.answer_scores)
            if updated:
                await self.update_embeds()

def bot_with_cyclic_update_process(update_event, answer_scores):

    def cyclic_update(bot, update_event):
        f = asyncio.run_coroutine_threadsafe(bot.update_embeds(), bot.loop)
        while True:
            update_event.wait()
            update_event.clear()
            f.cancel()
            f = asyncio.run_coroutine_threadsafe(bot.update_embeds(), bot.loop)
            #res = f.result()

    bot = Bot(answer_scores)

    upd_thread = threading.Thread(target=cyclic_update, args=(bot, update_event))
    upd_thread.start()

    loop = asyncio.get_event_loop()
    loop.create_task(bot.start('NzI0NjcwOTk3NTEyMzIzMDk2.XvDkiQ.lTNoF779KAIq3ULwEoXqqfygL5o'))
    loop.run_forever()


def selfbot_process(update_event, answer_scores):

    selfbot = SelfBot(update_event, answer_scores)

    loop = asyncio.get_event_loop()
    loop.create_task(selfbot.start('NDg5NzI0OTk4ODMxOTY0MTcw.XunCAg.eYTMvfYpIWK-Rvm0oZtSKlZZFvU',
                                   bot=False))
    loop.run_forever()

if __name__ == '__main__':

    # running bot and selfbot in separate OS processes

    # shared event for embed update
    update_event = multiprocessing.Event()

    # shared array with answer results
    answer_scores = multiprocessing.Array(typecode_or_type='i', size_or_initializer=3)

    p_bot = multiprocessing.Process(target=bot_with_cyclic_update_process, args=(update_event, answer_scores))
    p_selfbot = multiprocessing.Process(target=selfbot_process, args=(update_event, answer_scores))

    p_bot.start()
    p_selfbot.start()

    p_bot.join()
    p_selfbot.join()




 
 
