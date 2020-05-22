import sqlite3,json,os,sys
file_term = "../Entry Level Computer Programmer"
url = "localhost:8080"


from sys import getsizeof, stderr
from itertools import chain
from collections import deque
try:
    from reprlib import repr
except ImportError:
    pass

import requests

def total_size(o, handlers={}, verbose=False):
    """ Returns the approximate memory footprint an object and all of its contents.

    Automatically finds the contents of the following builtin containers and
    their subclasses:  tuple, list, deque, dict, set and frozenset.
    To search other containers, add handlers to iterate over their contents:

        handlers = {SomeContainerClass: iter,
                    OtherContainerClass: OtherContainerClass.get_elements}

    """
    dict_handler = lambda d: chain.from_iterable(d.items())
    all_handlers = {tuple: iter,
                    list: iter,
                    deque: iter,
                    dict: dict_handler,
                    set: iter,
                    frozenset: iter,
                   }
    all_handlers.update(handlers)     # user handlers take precedence
    seen = set()                      # track which object id's have already been seen
    default_size = getsizeof(0)       # estimate sizeof object without __sizeof__

    def sizeof(o):
        if id(o) in seen:       # do not double count the same object
            return 0
        seen.add(id(o))
        s = getsizeof(o, default_size)

        if verbose:
            print(s, type(o), repr(o), file=stderr)

        for typ, handler in all_handlers.items():
            if isinstance(o, typ):
                s += sum(map(sizeof, handler(o)))
                break
        return s

    return sizeof(o)



if __name__ == '__main__':
    with sqlite3.connect(os.path.join(os.getcwd(), file_term, f'{file_term}.db')) as connection:
        cur = connection.cursor()
        data = cur.execute(
            "SELECT training.unique_id,metadata.search_term,training.job_title,training.description,training.label,metadata.link,metadata.location FROM training LEFT JOIN  metadata ON training.unique_id = metadata.unique_id").fetchall()
        data = list(zip(*data))
        catagories = ['unique_id', 'search_term', 'job_title', 'description', 'label','link', 'location',
                      'company', 'date_posted']
        data = {cat:(data if cat != 'search_term' else ["Entry Level Computer Programmer",]*len(data)) for cat, data in zip(catagories, data)}
        transferable_data = json.dumps(data)
        print(sys.getsizeof(transferable_data))
    print(total_size(data, verbose=False))

    r = requests.post("http://127.0.0.1:8000/submit",json=transferable_data)
    print(r)
    re = requests.get("http://127.0.0.1:8000/submit",params={"search_term":file_term})
    print(json.loads(re.content))
    print(total_size(json.loads(re.content), verbose=False))