import urllib.request
import json
import itertools
from _md5 import md5
import os.path

class PokeapiProvider:
    
    def __init__(self):
        self.__url = "http://pokeapi.co/api/v2/%s/%s"
        self.__user_agent = " Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0"
        self.__charset = "utf-8"
    
    def __call(self, url):
        print("Call : " + url)
        
        if not os.path.exists("cache"):
            os.makedirs("cache")
        
        cache_name = "cache/"+ md5(url.encode("utf-8")).hexdigest()
        
        response = ""
        if not os.path.isfile(cache_name):
            request = urllib.request.Request(url=url, headers={'User-Agent': self.__user_agent})
            handler = urllib.request.urlopen(request)
            response = handler.read().decode("utf-8")
        
            with open(cache_name, "w") as cache:
                cache.write(response)
        
        else:
            with open(cache_name, "r") as cache:
                response = cache.read()
            
        
        return json.loads(response)
    
    def __get_language(self, languages, field, lang):
        text = ""
        for languages in languages:
            if languages["language"]["name"] == lang:
                text = languages[field]
                break
        return text        
        
    def get(self, what, api_id):
        return self.__call(self.__url % (what, api_id))
    
    def get_types(self):
        types = {}
        
        for i in range(1,19):
            pokemon_type = self.get("type", i)
            
            
            types[pokemon_type["name"]] = {
                "id" : i,
                "name" : self.__get_language(pokemon_type["names"], "name", "fr"),
                "damage_relations" : pokemon_type["damage_relations"]
            }
        
        return types
    
    def get_abilities(self):
        abilities = {}
        
        for i in range(1,192):
            ability = self.get("ability", i)
            
            
            #est ce que je dois prendre en compte le version group ???
            #on va dire que non
            
            abilities[ability["name"]] = {
                "name" : self.__get_language(ability["names"], "name", "fr"),
                "id" : ability["id"],
                "flavor_text" : self.__get_language(ability["flavor_text_entries"], "flavor_text", "fr"),
            }
        
        return abilities
        
    def get_egg_groups(self):
        egg_groups = {}
        
        for i in range (1,16):
            
            egg_group = self.get("egg-group", i)
            egg_groups[egg_group["name"]] = {
                "id" : egg_group["id"],
                "name" : self.__get_language(egg_group["names"], "name", "fr"),
            }
        
        
        return egg_groups
    
    def get_stats(self):
        stats = {}
        
        for i in range(1,9):
            stat = self.get("stat", i)
            
            stats[stat["name"]] = {
                "id" : stat["id"],
                "name" : self.__get_language(stat["names"], "name", "fr"),
                "battle_only" : stat["is_battle_only"],
            }
        
        return stats
    
    def get_pokemon(self):
        pokemons = {}
        
        for i in itertools.chain(range(1,722), range(10001,10091)):
            pokemon = self.get("pokemon", i)
            pokemon_spece = self.get("pokemon-species", pokemon["species"]["name"])
            
            
            pokemons[pokemon_spece["id"]] = {
                "id" : pokemon_spece["id"],
                "name" : self.__get_language(pokemon_spece["names"], "name", "fr"),
                "types" : pokemon["types"],
                "stats" : pokemon["stats"],
            }
            
        return pokemons
        