import pickle

default_store_file = 'store.pickle'

def load_store(store_file = default_store_file):
    try:
        with open(store_file, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return {}
    
def save_store(store, store_file = default_store_file):
    with open(store_file, 'wb') as f:
        pickle.dump(store, f)