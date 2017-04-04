class PokemonType:
	def __init__(self, type_id, name):
		self.__id = type_id
		self.__name = name
		self.__type_affinities = {
			'double_to' : [],
			'double_from' : [],
			'half_to': [],
			'half_from' : [],
			'zero_to' : [],
			'zero_from' : [],
		}
		
	def add_double_damage_to(self, pokemon_type):
		if pokemon_type not in self.__type_affinities['double_to']:
			if pokemon_type in self.__type_affinities['half_to']: 
				self.__type_affinities['half_to'].remove(pokemon_type)
			if pokemon_type in self.__type_affinities['zero_to']:
				self.__type_affinities['zero_to'].remove(pokemon_type)
			self.__type_affinities['double_to'].append(pokemon_type)
		
		if self not in pokemon_type.__type_affinities['double_from']:
			if self in pokemon_type.__type_affinities['half_from']:
				pokemon_type.__type_affinities['half_from'].remove(self)
			if self in pokemon_type.__type_affinities['zero_from']:
				pokemon_type.__type_affinities['zero_from'].remove(self)
			pokemon_type.__type_affinities['double_from'].append(self)



	def add_double_damage_from(self, pokemon_type):
		pokemon_type.add_double_damage_to(self)


	def add_half_damage_to(self, pokemon_type):
		if pokemon_type not in self.__type_affinities['half_to']:
			if pokemon_type in self.__type_affinities['double_to']:
				self.__type_affinities['double_to'].remove(pokemon_type)
			if pokemon_type in self.__type_affinities['zero_to']:
				self.__type_affinities['zero_to'].remove(pokemon_type)
			self.__type_affinities['half_to'].append(pokemon_type)
		
		if self not in pokemon_type.__type_affinities['half_from']:
			if self in pokemon_type.__type_affinities['double_from']:
				pokemon_type.__type_affinities['double_from'].remove(self)
			if self in pokemon_type.__type_affinities['zero_from']:
				pokemon_type.__type_affinities['zero_from'].remove(self)
			pokemon_type.__type_affinities['half_from'].append(self)
			

	def add_half_damage_from(self, pokemon_type):
		pokemon_type.add_half_damage_to(self)
		
	
	def add_zero_damage_to(self, pokemon_type):
		if pokemon_type not in self.__type_affinities['zero_to']:
			if pokemon_type in self.__type_affinities['double_to']:
				self.__type_affinities['double_to'].remove(pokemon_type)
			if pokemon_type in self.__type_affinities['half_to']:
				self.__type_affinities['half_to'].remove(pokemon_type)
			self.__type_affinities['zero_to'].append(pokemon_type)
		
		if self not in pokemon_type.__type_affinities['zero_from']:
			if self in pokemon_type.__type_affinities['double_from']:
				pokemon_type.__type_affinities['double_from'].remove(self)
			if self in pokemon_type.__type_affinities['half_from']:
				pokemon_type.__type_affinities['half_from'].remove(self)
			pokemon_type.__type_affinities['zero_from'].append(self)
			
	def add_zero_damage_from(self, pokemon_type):
		pokemon_type.add_zero_damage_to(self)

	def get_type_affinities(self):
		return self.__type_affinities.copy()
	
	def __str__(self):
		return self.__name