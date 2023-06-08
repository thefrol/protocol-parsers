class RbdataTounament:
    """a class returning tournament names in style of Rbdata hub
    
    like MФФ ЛПМ U10(2013)
    MФФ ЛПМ U11(2012)
    and others"""
    #TODO Зимнее первенство, указать в названии что это чисто по мфф турнирам, слеш годы 2022/2023
    def __init__(self, team_year, tournament_year, is_cup=False):
        """
        team year - year team born at
        tournament year - date when it passed"""
        self.team_year=team_year
        self.tournament_year=tournament_year
        self.is_cup=is_cup
        try:
            self.U_number=self.tournament_year-self.team_year # ex. U10, U11, U12
        except Exception:
            self.U_number=None
    
    @property
    def rbdata_name(self):
        if self.team_year is None or self.tournament_year is None:
            print('cant create tournament name, one of parameters is none')
            return None
        #TODO check if strange data <0 >20
        
        return f'MФФ ЛПМ U{self.U_number}({self.team_year})' if self.is_cup else f'Кубок МФФ U{self.U_number}({self.team_year})'
    
    @property
    def match_time(self):
        'returns a match time played based on a league'
        if self.U_number is None:
            print('cant define match time, using standart')
            return 60
        if self.U_number<11:
            return 50
        elif self.U_number<13:
            return 60 
        elif self.U_number<14:
            return 70
        else: # U15 and more
            return 80