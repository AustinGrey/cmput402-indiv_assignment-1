import pickle

def main():

    with open('stats.pkl', 'rb') as stats:
        stats = pickle.load(stats)

    print('loaded stats')

if __name__ == '__main__':
    main()