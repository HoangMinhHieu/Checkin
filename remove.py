import glob, os, argparse

parser = argparse.ArgumentParser()
parser.add_argument('--id', type=int, default=63, help='id to remove')
args = parser.parse_args()
dump = 'encode/{}/*'.format(args.id)

r = glob.glob(dump)
for i in r:
   os.remove(i)

