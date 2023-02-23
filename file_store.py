import pickle

store_file = 'store.pickle'

def load_store():
    try:
        with open(store_file, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return {}
    
def save_store(store):
    with open(store_file, 'wb') as f:
        pickle.dump(store, f)