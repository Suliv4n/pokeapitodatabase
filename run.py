import pokesql.builder
import pokeapi.provider

provider = pokeapi.provider.PokeapiProvider()


type_max = 17


print("Conecting to database...")
builder = pokesql.builder.PokeSQLBuilder("localhost", "root", "yourpassword", "pokemon")
print("Database connected !")

print("Start building database...")
builder.build_data_base()


print("Database built !")

print("Populating type table and references...")
types = provider.get_types()
builder.populate_type(types)