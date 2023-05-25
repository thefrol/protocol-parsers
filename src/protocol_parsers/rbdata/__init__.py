class RbdataTounament:
    """a class returning tournament names in style of Rbdata hub
    
    like MФФ ЛПМ U10(2013)
    MФФ ЛПМ U11(2012)
    and others"""
    #TODO Зимнее первенство, указать в названии что это чисто по мфф турнирам, слеш годы 2022/2023
    def __init__(self, team_year, tournament_year):
        """
        team year - year team born at
        tournament year - date when it passed"""
        self.team_year=team_year
        self.tournament_year=tournament_year
    
    @property
    def rbdata_name(self):
        if self.team_year is None or self.tournament_year is None:
            print('cant create tournament name, one of parameters is none')
            return None
        #TODO check if strange data <0 >20
        U_number=self.tournament_year-self.team_year
        return f'MФФ ЛПМ U{U_number}({self.team_year})'