import cProfile
from pstats import Stats, SortKey

from protocol_parsers import MosffParser
from pprint import pprint


#URL='https://mosff.ru/match/34549'
#URL='https://mosff.ru/match/38876' CUP
#URL='https://mosff.ru/match/38860' #CUP 2009
URL='https://mosff.ru/match/34540' #no minute for autogoals, add to tests



run_script=MosffParser(URL).to_rbdata


if __name__ == '__main__':
    do_profiling = True
    if do_profiling:
        with cProfile.Profile() as pr:
            run_script()

        with open('profiling_stats.txt', 'w') as stream:
            stats = Stats(pr, stream=stream)
            stats.strip_dirs()
            stats.sort_stats('time')
            stats.dump_stats('.prof_stats')
            stats.print_stats()
    else:
        start_game()