from spiders.steam_spider import SteamSpider #ok
from spiders.nuuven_spider import NuuvemSpider # ok

if __name__ == '__main__':
    steam = SteamSpider('https://store.steampowered.com/', 101, level = 1)
    steam.run()
    
    #nuuvem = NuuvemSpider('https://www.nuuvem.com/', 101, 1)
    #nuuvem.run()
 
    pass