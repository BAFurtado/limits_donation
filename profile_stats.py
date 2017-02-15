import pstats
p = pstats.Stats('profile.stats')
p.sort_stats('tottime')
p.print_stats(10)

# In terminal. Decorate function to be evaluated @profile
# python C:\Users\r1702898\AppData\Local\Continuum\Anaconda3\Lib\site-packages\kernprof.py -l -v main.py
#
# python -m line_profiler script_to_profile.py.lprof