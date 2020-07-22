'''
using discord.py version 1.0.0a
'''
import discord
import asyncio
import re
import multiprocessing
import threading
import concurrent

BOT_OWNER_ROLE = 'RUNNER' # change to what you need




oot_channel_id_list = [
"731946765141540995","732405414901317752","732405726252630026","731946765141540995","735234693175181364","730596073109848065","733762526038327416","735088771439263834","699218106144522280","699218251787534377","733413539771056148","733413471483330601"

]


answer_pattern = re.compile(r'(not|n)?([1-3]{1})(\?)?(cnf)?(\?)?$', re.IGNORECASE)

apgscore = 550
nomarkscore = 245
markscore = 134

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
        self.embed=discord.Embed(title="Connected With <a:emoji_66:715435468732497940>",description = '**<a:emoji_66:715435468732497940> Google Search Results! 🔎**',colour = discord.Colour.purple())
        self.embed.add_field(name="**__<a:emoji_27:698185546845126737> Option 1__**", value="0", inline=False)
        self.embed.add_field(name="**__<a:emoji_27:698185546845126737> Option 2__**", value="0", inline=False)
        self.embed.add_field(name="**__<a:emoji_27:698185546845126737> Option 3__**", value="0", inline=False)
        self.embed.set_footer(text='Developed By ꧁☬⋆ТᎻᎬ༒ᏦᎥᏁᏳ⋆☬꧂#3939',icon_url = "https://cdn.discordapp.com/attachments/731002183893647442/731840103479246909/images_18.jpeg")
        self.embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/731002183893647442/731840103479246909/images_18.jpeg')
        

        #await self.bot.add_reaction(embed,':spy:')


    async def clear_results(self):
        for i in range(len(self.answer_scores)):
            self.answer_scores[i]=0

    async def update_embeds(self):
      #  global wrong



        one_check = ""
        two_check = ""
        three_check = ""
        best_answer = ' <a:emoji_67:715533775802466437> '


        lst_scores = list(self.answer_scores)


        highest = max(lst_scores)
        best_answer = ' :hourglass: '
        lowest = min(lst_scores)
        answer = lst_scores.index(highest)+1
        #global wrong

        if highest > 0:
            if answer == 1:
                one_check = "<a:emoji_green:703812286107877456>"
                best_answer = '<a:emoji_67:715533775802466437>'
            else:
                one_check = " "

            if answer == 2:
                two_check = "<a:emoji_green:703812286107877456>"
                best_answer = '<a:emoji_67:715533775802466437>'
            else:
                two_check = " "

            if answer == 3:
                three_check = "<a:emoji_green:703812286107877456>"
                best_answer = '<a:emoji_67:715533775802466437>'
            else:
                three_check = " "



        #if lowest < 0:
            #if answer == 1:
                #one_cross = ":x:"
            #if answer == 2:
                #two_cross = ":x:"
            #if answer == 3:
                #three_cross = ":x:"

        self.embed.set_field_at(0, name="**__Option 1__**", value="**{0}**{1}".format(lst_scores[0], one_check))
        self.embed.set_field_at(1, name="**__Option 2__**", value="**{0}**{1}".format(lst_scores[1], two_check))
        self.embed.set_field_at(2, name="**__Option 3__**", value="**{0}**{1}".format(lst_scores[2], three_check))
        self.embed.set_footer(text='Developed By ꧁☬⋆ТᎻᎬ༒ᏦᎥᏁᏳ⋆☬꧂#3939',icon_url = "https://cdn.discordapp.com/attachments/731002183893647442/731840103479246909/images_18.jpeg")
        self.embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/731002183893647442/731840103479246909/images_18.jpeg')
        self.embed.set_image(url = 'https://cdn.discordapp.com/attachments/539493605493178388/726323830754115615/b6fW3cI.gif')
                             
        


        if self.embed_msg is not None:
            await self.embed_msg.edit(embed=self.embed)

    async def on_ready(self):
        print("==============")
        print("Connected to discord.")
        print("User: " + self.user.name)
        print("ID: " + str(self.user.id))

        await self.clear_results()
        await self.update_embeds()
        #await self.change_presence(activity=discord.Game(name='with '+str(len(set(self.get_all_members())))+' users'))
        await self.change_presence(activity=discord.Game(name='All Ans || +'))

    async def on_message(self, message):

        # if message is private
        if message.author == self.user or message.guild == None:
            return

        if message.content.lower() == "+":
            await message.delete()
            if BOT_OWNER_ROLE in [role.name for role in message.author.roles]:
                self.embed_msg = None
                await self.clear_results()
                await self.update_embeds()
                self.embed_msg = \
                    await message.channel.send('',embed=self.embed)
                await self.embed_msg.add_reaction("<a:emoji_67:715533775802466437>")
                #await self.embed_msg.add_reaction("âœ”")
                await self.embed_msg.add_reaction("❌")
                self.embed_channel_id = message.channel.id
            else:
                await message.channel.send("**lol😉** You Do Not Have permission To Use This **cmd!** :stuck_out_tongue_winking_eye:")
            return




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
    loop.create_task(bot.start('NzM1MzkxMTA1MTc2MzA1NzI1.XxfkdQ.1Fb6eYgsM44wMMvQpcmiy4mY8JM'))
    loop.run_forever()


def selfbot_process(update_event, answer_scores):

    selfbot = SelfBot(update_event, answer_scores)

    loop = asyncio.get_event_loop()
    loop.create_task(selfbot.start('NjQwMTUxMjI1OTgzMTcyNjA4.XxAJYQ.vHzi-udBKKZSqzaeUwChUP-61OR',
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
