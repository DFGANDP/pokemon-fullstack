
    def get_pokemon_list(
        self, 
        limit: int = 50, 
        offset: int = 0, 
        generation: Optional[str] = None, 
        type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get list of Pokemon with optional filtering"""
        with Session(self.engine) as session:
            query = select(Pokemon)
            
            if generation:
                query = query.where(Pokemon.generation == generation)
            
            if type:
                query = query.join(PokemonType).where(PokemonType.pokemon_type == type)
            
            query = query.offset(offset).limit(limit)
            pokemon_list = session.exec(query).all()
            
            return [pokemon.dict() for pokemon in pokemon_list]

    def get_pokemon_by_id(self, pokemon_id: int) -> Optional[Dict[str, Any]]:
        """Get specific Pokemon by ID"""
        with Session(self.engine) as session:
            pokemon = session.get(Pokemon, pokemon_id)
            return pokemon.dict() if pokemon else None

    def get_pokemon_details(self, pokemon_id: int) -> Optional[Dict[str, Any]]:
        """Get detailed Pokemon information including stats, moves, abilities"""
        with Session(self.engine) as session:
            pokemon = session.get(Pokemon, pokemon_id)
            if not pokemon:
                return None
            
            # Get types
            types = session.exec(
                select(PokemonType.pokemon_type).where(PokemonType.pokemon_number == pokemon_id)
            ).all()
            
            # Get stats
            stats = session.exec(
                select(PokemonStat).where(PokemonStat.pokemon_number == pokemon_id)
            ).all()
            
            # Get moves
            moves = session.exec(
                select(PokemonMove.pokemon_move).where(PokemonMove.pokemon_number == pokemon_id)
            ).all()
            
            # Get abilities
            abilities = session.exec(
                select(PokemonAbility.pokemon_ability).where(PokemonAbility.pokemon_number == pokemon_id)
            ).all()
            
            return {
                **pokemon.dict(),
                "types": types,
                "stats": [stat.dict() for stat in stats],
                "moves": moves,
                "abilities": abilities
            }

    def search_pokemon_by_name(self, name: str) -> List[Dict[str, Any]]:
        """Search Pokemon by name (case-insensitive)"""
        with Session(self.engine) as session:
            query = select(Pokemon).where(Pokemon.name.ilike(f"%{name}%"))
            pokemon_list = session.exec(query).all()
            return [pokemon.dict() for pokemon in pokemon_list]

    def get_all_types(self) -> List[str]:
        """Get list of all available Pokemon types"""
        with Session(self.engine) as session:
            types = session.exec(select(PokemonType.pokemon_type).distinct()).all()
            return sorted(types)

    def get_all_generations(self) -> List[str]:
        """Get list of all available Pokemon generations"""
        with Session(self.engine) as session:
            generations = session.exec(select(Pokemon.generation).distinct()).all()
            return sorted(generations)

    def get_database_summary(self) -> Dict[str, Any]:
        """Get overall database summary"""
        with Session(self.engine) as session:
            total_pokemon = session.exec(select(Pokemon)).all()
            total_types = session.exec(select(PokemonType.pokemon_type).distinct()).all()
            total_generations = session.exec(select(Pokemon.generation).distinct()).all()
            
            return {
                "total_pokemon": len(total_pokemon),
                "total_types": len(total_types),
                "total_generations": len(total_generations),
                "generations": sorted(total_generations),
                "types": sorted(total_types)
            }

    def get_generations_summary(self) -> List[Dict[str, Any]]:
        """Get summary by Pokemon generations"""
        with Session(self.engine) as session:
            # Count Pokemon per generation
            generations = session.exec(select(Pokemon.generation).distinct()).all()
            summary = []
            
            for generation in generations:
                count = session.exec(
                    select(Pokemon).where(Pokemon.generation == generation)
                ).all()
                summary.append({
                    "generation": generation,
                    "count": len(count)
                })
            
            return sorted(summary, key=lambda x: x["generation"])

    def get_types_summary(self) -> List[Dict[str, Any]]:
        """Get summary by Pokemon types"""
        with Session(self.engine) as session:
            # Count Pokemon per type
            types = session.exec(select(PokemonType.pokemon_type).distinct()).all()
            summary = []
            
            for pokemon_type in types:
                count = session.exec(
                    select(PokemonType).where(PokemonType.pokemon_type == pokemon_type)
                ).all()
                summary.append({
                    "type": pokemon_type,
                    "count": len(count)
                })
            
            return sorted(summary, key=lambda x: x["type"])
