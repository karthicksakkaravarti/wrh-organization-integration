

class RaceSeriesStandings(object):
    """ Calculates the points standings for a race series.
    given list of races and points matrix
    Points matrix will be somthing like 1st=20points, 2nd=15, 3rd=10, 4th=5, 5th=3, 6th=2, 7th=1
    race_list: List of results requires place column, and id_column
    id_col: column name for the id
    points: list of points for each place
    high: True if high number is better, False if low number is better
    """
        
    def race_results_csv(self, filenames: list[str, ...]):
        """ Load results from csv files
        Assumes they all have the same columns
        """
        # self.race_results = ...
        pass
    
    def calculate_standings(self, race_results: list[dict, ...], id_col: str, points: list[int, ...], high: bool = True):
        """ Calculate the standings for the series
        """
        results = dict()
        for race in race_results:
            for result in race:
                
                
            
        pass
