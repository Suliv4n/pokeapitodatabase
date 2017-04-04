import MySQLdb
from model import pokemon_type

class PokeSQLBuilder:
    
    def __init__(self, host, user, password, database):
        self.__connection = MySQLdb.Connect(host=host, user=user, passwd=password, db=database, charset='utf8')
        self.__connection.autocommit(True)
    
    def populate_type(self, types):
        values = []
        for type_id in types:
            pokemon_type = types[type_id]
            values.append([pokemon_type["id"], pokemon_type["name"]]);
        
        self.__insert_into("type", ["id","name"], values)
            
        
    
    
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
                sql += "constraint " + key["name"] + " foreign key (" + key["from"] + ") references " + key["table"] + "(" + key["column"] + "),"

        sql = sql[:-1]
        
        sql += ")"
        
        print(sql)
        
        self.__connection.query(sql)


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
        "zero_damage", 
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