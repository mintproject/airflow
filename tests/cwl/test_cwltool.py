from cwltool import main

#parse arguments
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("spec", help="spec cwl file")
parser.add_argument("values", help="values of the cwl file")
args = parser.parse_args()


main.run(["--debug", args.spec, args.values])