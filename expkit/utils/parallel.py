import multiprocessing as mp
from .arguments import star_wrap


def pmap(function, iterable, n_jobs=-1):
    if n_jobs == -1:
        pool = mp.Pool()
    else:
        pool = mp.Pool(n_jobs)

    for i in pool.imap_unordered(star_wrap(function), iterable):
        yield i


def papply(function, iterable, n_jobs=-1):
    tuple(pmap(function, iterable, n_jobs))
