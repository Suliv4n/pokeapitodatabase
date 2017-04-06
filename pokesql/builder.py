import MySQLdb

class PokeSQLBuilder:
    
    def __init__(self, host, user, password, database):
        self.__connection = MySQLdb.Connect(host=host, user=user, passwd=password, db=database, charset='utf8')
        self.__connection.autocommit(True)
    
    def populate_type(self, types):
        values = []
        type_affinities = {
            'half_damage_to' : [],
            'double_damage_to' : [],
            'no_damage_to' : [],
        }
        
        for type_id in types:
            
            pokemon_type = types[type_id]
            values.append([pokemon_type["id"], pokemon_type["name"]]);
            
            for relation_id in pokemon_type["damage_relations"]:
                
                relations = pokemon_type["damage_relations"][relation_id]
                
                if relation_id in type_affinities:
                    
                    for type_to in relations:
                        type_affinities[relation_id].append([pokemon_type["id"],types[type_to["name"]]["id"]])
                    
        
        print(str(type_affinities))
        
        self.__insert_into("type", ["id","name"], values)
        
        
        tables_affinity = {
            "double_damage_to" : "double_damage",
            "half_damage_to" : "half_damage",
            "no_damage_to" : "no_damage",
        }
        
        for type_affinity in type_affinities:
            self.__insert_into(tables_affinity[type_affinity], ["type_from", "type_to"], type_affinities[type_affinity])

        
    
    def populate_ability(self, abilities):
        values = []
        for key in abilities:
            ability = abilities[key]
            values.append([ability["id"], ability["name"], ability["flavor_text"]])
    
        self.__insert_into("ability", ["id", "name", "flavor_text"], values)
    
    def populate_egg_groups(self, egg_groups):
        values = []
        for egg_group in egg_groups:
            values.append([egg_groups[egg_group]["id"], egg_groups[egg_group]["name"]])
            
        self.__insert_into("egg_group", ["id", "name"], values)
    
    def __insert_into(self, table, columns, values):
        sql = "insert into " + table + "( " + ",".join(columns) + ") values"
        
        for value in values:
            
            sql += "("  + ",".join("\"" + str(x) + "\"" for x in value) + "),"
        
        sql = sql[:-1]
        
        print(sql)
        self.__connection.query(sql)

            
    
    def __create_table(self, name, columns = []):
        sql = "create table if not exists " + name + " ("
        
        foreign_keys = []
        
        for column in columns:
            sql += column["name"] + " " + column["type"] + " "
            
            if "options" in column:
                sql += column["options"]
            sql += ","
            
            if "reference" in column:
                fk_name = "FK_"+name+"_"+column["name"]+"__"+column["reference"]["table"]+"_"+column["reference"]["column"]
                foreign_keys.append({"name" : fk_name, "table" : column["reference"]["table"], "column": column["reference"]["column"] , "from" : column["name"]})
            
        if len(foreign_keys):
            
            for key in foreign_keys:
                sql += "constraint " + key["name"] + " foreign key (" + key["from"] + ") references " + key["table"] + "(" + key["column"] + ") on delete cascade,"

        sql = sql[:-1]
        
        sql += ")"
        
        
        print(sql)
        
        self.__connection.query(sql)
        self.__connection.query("delete from " + name)

    def build_data_base(self):
        #TYPE
        self.__create_table(
        "type", 
        [
            {
                "name" : "id",
                "type" : "int",
                "options" : "not null primary key"
            },
            {
                "name" : "name", 
                "type" : "varchar(64)",
            },
        ]        
        )
        
        #DOUBLE_DAMAGE
        self.__create_table(
        "double_damage", 
        [
            {
                "name" : "type_from",
                "type" : "int",
                "options" : "not null",
                "reference" : {
                    "table" : "type",
                    "column" : "id",
                }
            },
            {
                "name" : "type_to",
                "type" : "int",
                "options" : "not null",
                "reference" : {
                    "table" : "type",
                    "column" : "id",
                }
            },
        ]        
        )
        
        #HALF_DAMAGE
        self.__create_table(
        "half_damage", 
        [
            {
                "name" : "type_from",
                "type" : "int",
                "options" : "not null",
                "reference" : {
                    "table" : "type",
                    "column" : "id",
                }
            },
            {
                "name" : "type_to",
                "type" : "int",
                "options" : "not null",
                "reference" : {
                    "table" : "type",
                    "column" : "id",
                }
            },
        ]        
        )
        
        #ZERO_DAMAGE
        self.__create_table(
        "no_damage", 
        [
            {
                "name" : "type_from",
                "type" : "int",
                "options" : "not null",
                "reference" : {
                    "table" : "type",
                    "column" : "id",
                }
            },
            {
                "name" : "type_to",
                "type" : "int",
                "options" : "not null",
                "reference" : {
                    "table" : "type",
                    "column" : "id",
                }
            },
        ]    
        )
        
        #ABILTY
        self.__create_table("ability", [
            {
                "name" : "id",
                "type" : "int",
                "options" : "not null primary key"
            },
            {
                "name" : "name",
                "type" : "varchar(64)",
                "options" : "not null",
            },
            {
                "name" : "flavor_text",
                "type" : "varchar(255)",
            },
        ])
        
        #EGG_GROUP
        self.__create_table("egg_group", [
            {
                "name" : "id",
                "type" : "int",
                "options" : "not null primary key"
            },
            {
                "name" : "name",
                "type" : "varchar(64)",
                "options" : "not null",
            },
        ])