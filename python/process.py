#python python/process.py
import json
import os
from os import listdir
from pathlib import Path
import shutil
import subprocess
import argparse
import urllib
import threading

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", default = './svg_hard')
parser.add_argument("--output", "-o", default = './svg_output')
args = parser.parse_args()


def process_single(path_name):
	name = path_name.name.split('.')[0]   # without suffix
	folder = os.path.dirname(f)
	# convert input svg to scap
	# python ./visualization/scap_to_svg.py  path/to/.scap  ./output.svg
	scap_file = "{}.scap".format(name)
	cmd_scap = ['python', './visualization/svg_to_scap_width_exact.py', str(f), '-o', "{}/{}".format(folder, scap_file)]
	subprocess.run(cmd_scap, cwd="{}/{}".format(os.getcwd(), "python")) 
	# run strip maker
	# python3 ./python/launching/run_prediction.py ./data/inputs_test.yml --exe path/to/build/clustering-solve,path/to/build/clustering-endend --output ./snapshot/stripmaker_test.pdf --spiral
	cmd_strip_maker = ['python', './python/launching/run_prediction.py', "{}/{}".format(folder, scap_file), '--exe', '{}/build/clustering-solve,{}/build/clustering-endend'.format(os.getcwd(), os.getcwd()), '--output', './snapshot/stripmaker_{}.pdf'.format(name), '--spiral']
	subprocess.run(cmd_strip_maker, cwd=os.getcwd())
	# convert output scap to svg
	final_scap = "{}_final_out.scap".format(name)
	final_svg = "{}_final_out.svg".format(name)
	out_name = "{}/{}".format(os.getcwd(), "python")
	cmd_svg = ['python', './visualization/scap_to_svg.py', "{}/snapshot/{}/{}".format(os.getcwd(), name, final_scap), "{}/snapshot/{}/{}".format(os.getcwd(), name, final_svg)]
	subprocess.run(cmd_svg, cwd="{}/{}".format(os.getcwd(), "python")) 


# for f in Path(args.input).glob('*_final.svg'):
for f in Path(args.input).glob('*.svg'):
	thread = threading.Thread(target=process_single, args=(f,))
	thread.start()


