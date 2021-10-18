import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--dev", help="enables dev mode", action="store_true")

args = parser.parse_args()

if args.dev:
    print("dev mode")
    DEV = True
else:
    DEV = False
