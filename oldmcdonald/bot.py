import asyncio
import random
import discord

class OldMcDonald(discord.Client):
    def __init__(self):
        super().__init__()
        self.prefix = '!'
        self.ready = False
        self.target_discrims = ['0001', '6969', '1337']
        self.preferred_name = 'ENTER USERNAME HERE'
        self.token = 'ENTER TOKEN HERE'
        self.password = 'ENTER PASSWORD HERE'
        self.servers_to_join = ['discord.gg/GZQg2Eg', 'discord.gg/overwatch', 'discord.gg/wow', 'discord.gg/discord-developers', 'discord.gg/rainbow6']
        print('init')

    # noinspection PyMethodOverriding
    def run(self):
        try:
            loop = asyncio.get_event_loop()
            loop.create_task(self.discrim_farming())
            loop.run_until_complete(self.start(self.token, bot=False))
            loop.run_until_complete(self.connect())
        except Exception as e:
            print(e)
            loop.run_until_complete(self.close())
        finally:
            loop.close()

    
    async def discrim_farming(self):
        while not self.ready: await asyncio.sleep(1)
        while not self.is_closed:
            new_name = random.choice([member.name for member in self.get_all_members() if (member.discriminator == self.user.discriminator and member.id != '77511942717046784')])
            try:
                await self.edit_profile(password=self.password, username=new_name)
                
                if server.me.discriminator in self.target_discrims:
                    print('target discriminator \'%s\' gotten! GLHF!' % server.me.discriminator)
                    return
                
                await asyncio.sleep(2)
                print('discrim is now \'%s\', waiting 24 hrs to change again' % server.me.discriminator)
                await self.edit_profile(password=self.password, username=self.preferred_name)
                
            except discord.HTTPException:
                print('Discrim change locked, gonna wait 24 hrs anyway!')
                if self.user.name != self.preferred_name:
                    await self.edit_profile(password=self.password, username=self.preferred_name)
                
            await asyncio.sleep(86400)

    async def on_ready(self):

        print('Connected!\n')
        print('Checking for missing discriminators...\n')
        while True:
            unique_discrims = list(set([member.discriminator for member in self.get_all_members()]))
            final = []
            for x in range(1, 10000):
                if str(x).zfill(4) not in unique_discrims:
                    final.append(str(x).zfill(4))
            if final:
                server = random.choice(self.servers_to_join)
                await self.accept_invite(server)
                print('Missing %s discriminators, joining %s' % (len(final), server))
            else:
                break
            
        print('Done!\nDiscrim farming for\n\t%s\n' % self.target_discrims)
        self.ready = True
        print('~\n')
if __name__ == '__main__':
    bot = OldMcDonald()
    bot.run()
