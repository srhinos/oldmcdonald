import asyncio
import random
import aiohttp
import discord

class OldMcDonald(discord.Client):
    def __init__(self):
        super().__init__()
        self.prefix = '!'
        self.ready = False
        self.target_discrims = ['0001', '6969', '1337']
        self.preferred_name = "ENTER USERNAME HERE"
        self.token = "ENTER TOKEN HERE"
        self.password = "ENTER PASSWORD HERE"
        self.servers_to_join = ['GZQg2Eg', 'overwatch', 'wow', 'GVEkq8q', 'DestinyReddit']
        self.x_context_properties = 'eyJMb2NhdGlvbiI6IkpvaW4gYSBTZXJ2ZXIgTW9kYWwifQ=='
        self.x_super_properties = 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjAuMC4yOTgiLCJvc192ZXJzaW9uIjoiMTAuMC4xNDM5MyJ9'
        self.headers = {'x-context-properties': self.x_context_properties,
                          'origin': 'https://discordapp.com',
                          'accept-language': 'en-US',
                          'x-super-properties': self.x_super_properties,
                          'accept': '*/*',
                          'referer': 'https://discordapp.com/channels/@me',
                          'authority': 'discordapp.com',
                          'user-agent': 'Mozilla/5.0 (Windows NT 10.0;) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.298 Chrome/56.0.2924.87 Discord/1.6.11 Safari/537.36',
                          'content-length': '0',
                          'authorization': self.token,
                          'accept-encoding': 'gzip, deflate'}
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
                await asyncio.sleep(10)
                if self.user.discriminator in self.target_discrims:
                    print('target discriminator \'%s\' gotten! GLHF!' % self.user.discriminator)
                    return
                
                print('discrim is now \'%s\', waiting 24 hrs to change again' % self.user.discriminator)
                await self.edit_profile(password=self.password, username=self.preferred_name)
                
            except discord.HTTPException:
                print('Discrim change locked, gonna wait 24 hrs anyway!')
                if self.user.name != self.preferred_name:
                    try:
                        await self.edit_profile(password=self.password, username=self.preferred_name)
                    except:
                        print('\nTarget username "%s" appears to be taken causing you to be locked out till tomorrow! Sorry! Choose a new username that isn\'t locked or wait till tomorrow!' % self.preferred_name)
                
            await asyncio.sleep(86400)
    
    async def ghetto_join_server(self, invite_id):
         with aiohttp.ClientSession() as session:
            async with session.post('https://discordapp.com/api/v6/invite/{}'.format(invite_id), headers=self.headers) as r:
                assert r.status == 200
                

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
                print(final)
                server = random.choice(self.servers_to_join)
                invite = await self.get_invite(server)
                if not invite.server.id in [servers.id for servers in self.servers]:
                    await self.ghetto_join_server(server)
                    print('Missing %s discriminators, joining %s' % (len(final), server))
                    await asyncio.sleep(5)
            else:
                break
            
        print('Done!\nDiscrim farming for\n\t%s\n' % self.target_discrims)
        self.ready = True
        print('~\n')
if __name__ == '__main__':
    bot = OldMcDonald()
    bot.run()
