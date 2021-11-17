import argparse

parser = argparse.ArgumentParser()

parser.add_argument("name", help="user name", type=str)
parser.add_argument("--dev", help="enables dev mode", action="store_true")


args = parser.parse_args()

if args.dev:
    DEV = True
else:
    DEV = False

NAME = args.name

if __name__ == '__main__':
    print(f"dev mode : {DEV}")
    print(f'name : {NAME}')
