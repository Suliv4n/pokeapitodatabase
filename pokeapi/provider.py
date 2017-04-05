import urllib.request
import json
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
    
    
    def get(self, what, api_id):
        return self.__call(self.__url % (what, api_id))
    
    def get_types(self):
        types = {}
        
        for i in range(1,19):
            pokemon_type = self.get("type", i)
            

            for lang in pokemon_type["names"]:
                if lang["language"]["name"] == "fr":
                    name = lang["name"]
                    break
            
            types[pokemon_type["name"]] = {
                "id" : i,
                "name" : name,
                "damage_relations" : pokemon_type["damage_relations"]
            }
        
        return types
    
    def get_abilities(self):
        abilities = {}
        
        for i in range(1,10):
            ability = self.get("ability", i)
            
            ability_name = ""
            for name in ability["names"]:
                if name["language"]["name"] == "fr":
                    ability_name = name["name"]
                    break
            
            #est ce que je dois prendre en compte le version group ???
            #on va dire que non
            ability_text = ""
            for text in ability["flavor_text_entries"]:
                if text["language"]["name"] == "fr":
                    ability_text = text["flavor_text"]
                    break
            
            
            abilities[ability["name"]] = {
                "name" : ability_name,
                "id" : ability["id"],
                "flavor_text" : ability_text,
            }
        
        return abilities
        