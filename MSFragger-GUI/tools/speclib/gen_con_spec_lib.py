#!/usr/bin/env python3
import datetime
import enum
import glob
import itertools
import logging
import os
import pathlib
import re
import shlex
import shutil
import subprocess
import sys
import time
import timeit

import lxml.etree
import numpy as np
import pandas as pd
import scipy.interpolate

from common_funcs import (str_to_path, name_no_ext, os_fspath)

lg = logging.getLogger(__name__)
delete_temp_files: bool = False


def configure_logger(log: logging.Logger) -> None:
	log.handlers.clear()
	ch = logging.StreamHandler(stream=sys.stdout)
	ch.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(message)s'))
	# ch.setLevel(logging.NOTSET)
	log.addHandler(ch)

lg.setLevel(logging.DEBUG)
configure_logger(lg)

START = timeit.default_timer()
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

assert len(sys.argv) >= 8 and sys.argv[7].casefold() == 'use_easypqp'

class Irt_choice(enum.Enum):
	no_iRT = enum.auto()
	iRT = enum.auto()
	ciRT = enum.auto()
	Pierce_iRT = enum.auto()
	userRT = enum.auto()

class Im_choice(enum.Enum):
	no_im = enum.auto()
	userIM = enum.auto()


def cpu_count() -> int:
	try:
		return len(os.sched_getaffinity(0))
	except AttributeError:
		return os.cpu_count() if os.cpu_count() else 1

# https://github.com/python/cpython/issues/76623
def resolve_mapped(path) -> str:
	path = pathlib.Path(path).resolve()
	mapped_paths = []
	for drive in 'ZYXWVUTSRQPONMLKJIHGFEDCBA':
		root = pathlib.Path('{}:/'.format(drive))
		try:
			mapped_paths.append(root / path.relative_to(root.resolve()))
		except (ValueError, OSError):
			pass
	return os.fspath(min(mapped_paths, key=lambda x: len(str(x)), default=path))


nproc0 = int(sys.argv[9]) if len(sys.argv) >= 10 else 0
nproc = max(cpu_count() - 1, 1) if nproc0 <= 0 else nproc0
if len(sys.argv) >= 9:
	rta, ima = sys.argv[8].split(os.pathsep)
	no_iRT = rta.casefold() == 'noirt'
	is_iRT = rta.casefold() == 'irt'
	is_ciRT = rta.casefold() == 'cirt'
	is_Pierce_iRT = rta.casefold() == 'Pierce_iRT'.casefold()
	is_userRT = pathlib.Path(rta).exists()
	userRT_file = pathlib.Path(rta).resolve(strict=True) if is_userRT else None
	no_im = ima.casefold() == 'noim'
	is_userIM = pathlib.Path(ima).exists()
	userIM_file = pathlib.Path(ima).resolve(strict=True) if is_userIM else None
irt_choice = Irt_choice.no_iRT if no_iRT else \
	Irt_choice.iRT if is_iRT else \
		Irt_choice.ciRT if is_ciRT else \
			Irt_choice.Pierce_iRT if is_Pierce_iRT else \
				Irt_choice.userRT if userRT_file else \
					None
if irt_choice is None:
	raise RuntimeError('invalid iRT')
im_choice = Im_choice.no_im if no_im else \
	Im_choice.userIM if userIM_file else \
		None
if im_choice is None:
	raise RuntimeError('invalid IM')
easypqp_convert_extra_args = shlex.split(sys.argv[10]) if len(sys.argv) >= 11 else []
easypqp_library_extra_args = shlex.split(sys.argv[11]) if len(sys.argv) >= 12 else []
spectra_files0 = sorted(pathlib.Path(e) for e in sys.argv[3].split(os.pathsep))
if len(sys.argv) >= 13 and sys.argv[12] == 'delete_intermediate_files':
	delete_temp_files = True
if spectra_files0 == [pathlib.Path('unused')] and len(sys.argv) >= 14:
	spectra_files0 = [pathlib.Path(e) for e in sys.argv[13:]]
	if len(spectra_files0) >= 1 and spectra_files0[0].name.endswith('.txt'): # check if file is a file list
		filelist_str = pathlib.Path(spectra_files0[0]).read_text('utf-8').splitlines()
		filelist = list(map(pathlib.Path, filelist_str))
		if all(e.exists() for e in filelist):
			print("File list provided")
			spectra_files0 = filelist


def get_bin_path_pip_main(dist: str, bin_stem: str) -> pathlib.Path:
	'''
	get binary path for a package with binary stem
	:param dist: package name
	:param bin_stem: name of binary without extension
	:return: None if not found, binary path if found.
	'''
	import io, re, pathlib, contextlib, pip.__main__
	with contextlib.redirect_stdout(io.StringIO()) as f:
		pip.__main__._main(['show', '--files', dist])
	stdout = f.getvalue()
	location = pathlib.Path(re.compile('^Location: (.+)$', re.MULTILINE).search(stdout).group(1))
	a = re.compile('''^Files:(?:
  .+)+''', re.MULTILINE)
	files = [location / e[2:] for e in a.search(stdout).group().splitlines()[1:]]
	rel_loc, = [e for e in files if pathlib.Path(e).stem == bin_stem]
	return (pathlib.Path(location) / rel_loc).resolve()

def get_bin_path_pip_CLI(dist: str, bin_stem: str) -> pathlib.Path:
	'''
	get binary path for a package with binary stem
	:param dist: package name
	:param bin_stem: name of binary without extension
	:return: None if not found, binary path if found.
	'''
	import subprocess, sys, re, pathlib, io
	stdout = subprocess.run([sys.executable, '-m', 'pip', 'show', '--files', dist], capture_output=True,
							check=True).stdout
	stdout = io.TextIOWrapper(io.BytesIO(stdout), newline=None).read()
	location = pathlib.Path(re.compile('^Location: (.+)$', re.MULTILINE).search(stdout).group(1))
	a = re.compile('^Files:(?:\n  .+)+', re.MULTILINE)
	files = [location / e[2:] for e in a.search(stdout).group().splitlines()[1:]]
	rel_loc, = [e for e in files if pathlib.Path(e).stem == bin_stem]
	return (pathlib.Path(location) / rel_loc).resolve()


def get_bin_path_pip_private_API(dist: str, bin_stem: str) -> pathlib.Path:
	'''
	get binary path for a package with binary stem
	:param dist: package name
	:param bin_stem: name of binary without extension
	:return: None if not found, binary path if found.
	'''
	import pip._internal.commands.show
	import pathlib
	dist, = list(pip._internal.commands.show.search_packages_info([dist]))
	files, location = (dist.get('files'), dist['location']) \
		if isinstance(dist, dict) else \
		(dist.files, dist.location)
	if files is None and sys.platform == "win32":
		script_path = (pathlib.Path(sys.executable).resolve().parent / "Scripts").resolve()
		return (pathlib.Path(script_path) / (bin_stem + ".py")).resolve()
	else:
		rel_loc, = [e for e in files if pathlib.Path(e).stem == bin_stem]
	return (pathlib.Path(location) / rel_loc).resolve()

get_bin_path = get_bin_path_pip_CLI

script_dir = pathlib.Path(__file__).resolve().parent
if script_dir.suffix == '.pyz':
	script_dir = script_dir.parent

fasta = str_to_path(sys.argv[1]).resolve(strict=True)
iproph_RT_aligned = str_to_path(sys.argv[2]).resolve(strict=True)
workdir = str_to_path(sys.argv[4])
overwrite: bool = False
if len(sys.argv) >= 6:
	if sys.argv[5].casefold() == 'true':
		overwrite = True

if 'PATHEXT' in os.environ:
	os.environ['PATHEXT'] = '.py' + os.pathsep + os.environ['PATHEXT']
os.environ['PATH'] = os.getcwd() + os.pathsep + os.environ['PATH']

easypqp = get_bin_path('easypqp', 'easypqp')

CWD = os.getcwd()

def get_window_setup(p: pathlib.Path):
	"""return a list of pairs of window centers and wideness"""
	l = []
	window_desc = []
	first_precursorScanNum = None
	with p.open("rb") as f:
		# https://bugs.python.org/issue18304
		context = lxml.etree.iterparse(f, events=("start",), tag="{*}precursorMz")
		for action, elem in context:
			precursorScanNum = int(elem.attrib["precursorScanNum"])
			if first_precursorScanNum is None:
				first_precursorScanNum = precursorScanNum
			if first_precursorScanNum != precursorScanNum:
				break

			windowWideness = float(elem.attrib['windowWideness'])
			windowcenter = float(elem.text)

			# https://stackoverflow.com/questions/7171140/using-python-iterparse-for-large-xml-files/7171543
			elem.clear()
			for ancestor in elem.xpath('ancestor-or-self::*'):
				while ancestor.getprevious() is not None:
					del ancestor.getparent()[0]

			window_desc.append((windowcenter, windowWideness))
		del context
	return window_desc


iproph_pep_xmls0 = sorted(e.resolve() for e in iproph_RT_aligned.glob("*.pep.xml"))
iproph_pep_mod_xmls = sorted(e.resolve() for e in iproph_RT_aligned.glob("*.mod.pep.xml"))
iproph_pep_xmls = iproph_pep_mod_xmls if iproph_pep_mod_xmls else iproph_pep_xmls0
assert len(iproph_pep_xmls) > 0, iproph_RT_aligned

### RT alignment with common peptides
# https://github.com/msproteomicstools/msproteomicstools/blob/17e9c2bf43/analysis/spectral_libs/spectrast2spectrast_irt.py#L331
biognosys_rtkit = {'LGGNEQVTR': -28.3083, 'GAGSSEPVTGLDAK': 0.227424, 'VEATFGVDESNAK': 13.1078, 'YILAGVENSK': 22.3798, 'TPVISGGPYEYR': 28.9999, 'TPVITGAPYEYR': 33.6311, 'DGLDAASYYAPVR': 43.2819, 'ADVTPADFSEWSK': 54.969, 'GTFIIDPGGVIR': 71.3819, 'GTFIIDPAAVIR': 86.7152, 'LFLQFGAQGSPFLK': 98.0897}
import operator

biognosys_rtkit_sorted = sorted(biognosys_rtkit.items(), key=operator.itemgetter(1))
"""
Identification of a Set of Conserved Eukaryotic Internal Retention Time Standards for Data-independent Acquisition Mass Spectrometry.
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4597153/
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4597153/bin/supp_O114.042267_mcp.O114.042267-2.txt
"""
ciRT_rtkit_str = "ADTLDPALLRPGR:35.987015,AFEEAEK:-21.35736,AFLIEEQK:22.8,AGFAGDDAPR:-9.819255,AGLQFPVGR:37.04898,AILGSVER:5.415375,APGFGDNR:-15.63474,AQIWDTAGQER:16.854875,ATAGDTHLGGEDFDNR:3.185526667,ATIGADFLTK:43.837285,AVANQTSATFLR:19.24765,AVFPSIVGRPR:34.03497,C[160]ATITPDEAR:-10.13943,DAGTIAGLNVLR:59.03744667,DAHQSLLATR:-3.25497,DELTLEGIK:39.132035,DLMAC[160]AQTGSGK:0.306955,DLTDYLMK:60.01111111,DNIQGITKPAIR:12.598125,DNTGYDLK:-9.39721,DSTLIMQLLR:103.65,DSYVGDEAQSK:-15.509125,DVQEIFR:29.61571,DWNVDLIPK:70.53546,EAYPGDVFYLHSR:46.35,EC[160]ADLWPR:28.711905,EDAANNYAR:-23.23042,EGIPPDQQR:-15.8411,EHAALEPR:-22.61094,EIAQDFK:-4.04913,EIQTAVR:-17.07064,ELIIGDR:11.56179,ELISNASDALDK:23.50069,EMVELPLR:47.96546,ESTLHLVLR:28.54494,EVDIGIPDATGR:37.10299,FDDGAGGDNEVQR:-11.31703,FDLMYAK:38.2,FDNLYGC[160]R:9.6064,FEELC[160]ADLFR:73.5,FELSGIPPAPR:52.5,FELTGIPPAPR:53.1,FPFAANSR:18.76225,FQSLGVAFYR:60.2276,FTQAGSEVSALLGR:61.450335,FTVDLPK:37.86026,FVIGGPQGDAGLTGR:40.551975,GC[160]EVVVSGK:-15.49014,GEEILSGAQR:-1.811165,GILFVGSGVSGGEEGAR:51.15,GILLYGPPGTGK:45.36582,GIRPAINVGLSVSR:37.98295,GNHEC[160]ASINR:-23.57003,GVC[160]TEAGMYALR:31.20584,GVLLYGPPGTGK:28.11667,GVLMYGPPGTGK:28.20674,HFSVEGQLEFR:41.108635,HITIFSPEGR:22.39813,HLQLAIR:9.42694,HLTGEFEK:-13.72484,HVFGQAAK:-24.54245,IC[160]DFGLAR:28.009545,IC[160]GDIHGQYYDLLR:50.34788,IETLDPALIRPGR:43.43414,IGGIGTVPVGR:21.9,IGLFGGAGVGK:43.285185,IGPLGLSPK:29.48313,IHETNLK:-25.53888,IINEPTAAAIAYGLDK:65.72006667,IYGFYDEC[160]K:31.695135,KPLLESGTLGTK:9.057185,LAEQAER:-25.089125,LGANSLLDLVVFGR:134.00759,LIEDFLAR:56.93148,LILIESR:28.145215,LPLQDVYK:29.2,LQIWDTAGQER:36.28872,LVIVGDGAC[160]GK:10.8,LVLVGDGGTGK:12.022895,LYQVEYAFK:46.26582,MLSC[160]AGADR:-15.49156,NILGGTVFR:49.61455,NIVEAAAVR:5.73971,NLLSVAYK:34.34229,NLQYYDISAK:25.8,NMSVIAHVDHGK:-5.36295,QAVDVSPLR:11.34271,QTVAVGVIK:9.9,SAPSTGGVK:-27.56682,SGQGAFGNMC[160]R:0.790505,SNYNFEKPFLWLAR:96.01717,STELLIR:18.1,STTTGHLIYK:-9.48751,SYELPDGQVITIGNER:67.30002,TIAMDGTEGLVR:32.822885,TIVMGASFR:29.53023,TLSDYNIQK:4.35,TTIFSPEGR:15.183785,TTPSYVAFTDTER:33.79824667,TTVEYLIK:30.16799,VAVVAGYGDVGK:15.331395,VC[160]ENIPIVLC[160]GNK:49.065875,VLPSIVNEVLK:83.750085,VPAINVNDSVTK:17.70942,VSTEVDAR:-20.136945,VVPGYGHAVLR:8.61752,WPFWLSPR:98.382385,YAWVLDK:41.6,YDSTHGR:-57.05955,YFPTQALNFAFK:95.4,YLVLDEADR:27.6947,YPIEHGIVTNWDDMEK:56.9,YTQSNSVC[160]YAK:-12.794935"
ciRT_rtkit = {e.split(":")[0]: float(e.split(":")[1]) for e in ciRT_rtkit_str.split(",")}
ciRT_rtkit_sorted = sorted(ciRT_rtkit.items(), key=operator.itemgetter(1))
len(biognosys_rtkit), len(ciRT_rtkit)
combined_rtkit_str = ",".join(a+":"+str(b) for a,b in sorted({**biognosys_rtkit,**ciRT_rtkit}.items(), key=operator.itemgetter(1)))
rtkit_str = ",".join(a + ":" + str(b) for a, b in sorted({**biognosys_rtkit}.items(), key=operator.itemgetter(1)))

if len(spectra_files0) == 1 and not spectra_files0[0].exists():
	mzXMLs = sorted(e.resolve() for e in iproph_RT_aligned.glob('*.mzXML'))
	mzMLs = sorted(e.resolve() for e in iproph_RT_aligned.glob('*.mzML'))
	mgfs = sorted(e.resolve() for e in iproph_RT_aligned.glob('*.mgf'))
	if len(mzXMLs) > 0:
		spectra_files = mzXMLs
	elif len(mzMLs) > 0:
		spectra_files = mzMLs
	else:
		spectra_files = mgfs
else:
	spectra_files = [e.resolve(strict=True) for e in spectra_files0 if e.exists()]
	if all([os.fspath(e).endswith('calibrated.mzML') for e in spectra_files0]):
		print('Using (un)calibrated.mzML files.')
	if len(spectra_files) == 0:
		raise RuntimeError([os.fspath(e) for e in iproph_RT_aligned.iterdir()])
psm_tsv_file = iproph_RT_aligned / 'psm.tsv'
peptide_tsv_file = iproph_RT_aligned / 'peptide.tsv'
'easypqp convert --pepxml interact.pep.xml --spectra 1.mgf --unimod unimod.xml --exclude-range -1.5,3.5'

dd = [pd.DataFrame({'modified_peptide': [e[0] for e in biognosys_rtkit_sorted],
					'precursor_charge': np.repeat(i, len(biognosys_rtkit_sorted)),
					'irt': [e[1] for e in biognosys_rtkit_sorted]
					# 'im':
					})
	  for i in range(1, 8)]
irt_df = pd.concat(dd).reset_index(drop=True)
irt_file = workdir / 'irt.tsv'
im_file = workdir / 'im.tsv'
# https://github.com/grosenberger/easypqp/blob/master/easypqp/data/unimod.xml?raw=true
# http://www.unimod.org/xml/unimod.xml
from typing import List
def pairing_pepxml_spectra_v3(spectras: List[pathlib.PurePath], pep_xmls: List[pathlib.PurePath]):
	rec = re.compile('(.+?)(?:_(?:un)?calibrated)?')
	spectra_files_basename = [rec.fullmatch(e.stem)[1] for e in spectras]
	assert len(set(spectra_files_basename)) == len(spectras), [sorted(set(spectra_files_basename)), sorted(spectras)]
	if len(pep_xmls) == 1:
		return list(zip(spectra_files_basename, [''] * len(spectras), spectras, pep_xmls * len(spectras)))
	rec2 = re.compile('(?:interact-)?(.+?)(?:_rank[0-9]+)?')
	pepxml_basename = [
		rec2.fullmatch(name_no_ext(e))[1] for e in
		pep_xmls]
	l = [[p for p, bn in zip(pep_xmls, pepxml_basename) if e.casefold() == bn.casefold()] for e in spectra_files_basename]

	def get_rank(name: pathlib.PurePath) -> str:
		mo = re.compile('_rank[0-9]+$').search(name_no_ext(name))
		return '' if mo is None else mo[0]

	l2 = [(basename, get_rank(p), s, p) for basename, s, ps in zip(spectra_files_basename, spectras, l) for p in ps]
	return l2
runname_rank_spectra_pepxml = pairing_pepxml_spectra_v3(spectra_files, iproph_pep_xmls)
runname_rank_spectra_pepxml_collapse_rank = list((k[0], '', k[1], [ee[3] for ee in v]) for k, v in itertools.groupby(runname_rank_spectra_pepxml, key=lambda e: (e[0], e[2])))
convert_outs = [f'{basename}{rank}' for basename, rank, _, _ in runname_rank_spectra_pepxml_collapse_rank]
easypqp_convert_cmds = [[resolve_mapped(easypqp), 'convert', *easypqp_convert_extra_args,'--enable_unannotated', '--pepxml', repr([resolve_mapped(pep_xml).replace("'","\\'") for pep_xml in pep_xmls]), '--spectra', resolve_mapped(spectra), '--exclude-range', '-1.5,3.5',
						 '--psms', f'{outfiles}.psmpkl', '--peaks', f'{outfiles}.peakpkl']
						for (_, _, spectra, pep_xmls), outfiles in zip(runname_rank_spectra_pepxml_collapse_rank, convert_outs)]
easypqp_library_infiles = [workdir / (e + '.psmpkl') for e in convert_outs] + \
													[workdir / (e + '.peakpkl') for e in convert_outs]
easyPQP_tempfiles = easypqp_library_infiles + \
										[workdir / (e + '_run_peaks.tsv') for e in convert_outs] + \
										[workdir / 'easypqp_lib_openswath.tsv']
filelist_easypqp_library = workdir / 'filelist_easypqp_library.txt'
filelist_easypqp_library.write_text('\n'.join(map(os.fspath, easypqp_library_infiles)))
use_iRT = irt_choice is not Irt_choice.no_iRT
use_im = im_choice is not Im_choice.no_im
filelist_arg = [resolve_mapped(filelist_easypqp_library)]


def easypqp_library_cmd(use_irt: bool, use_im: bool) -> list[str]:
	return [resolve_mapped(easypqp), 'library',
			'--psmtsv', resolve_mapped(psm_tsv_file), '--peptidetsv', resolve_mapped(peptide_tsv_file), ] + \
		   (['--rt_reference', resolve_mapped(irt_file)] if use_irt else []) + \
		   (['--im_reference', resolve_mapped(im_file)] if use_im else []) + \
		   ['--out', 'easypqp_lib_openswath.tsv'] + easypqp_library_extra_args + filelist_arg


easypqp_cmds = '\n'.join(' '.join(map(shlex.quote, e)) for e in easypqp_convert_cmds) + '\n' + \
			   ' '.join(map(lambda x: shlex.quote(os.fspath(x)), easypqp_library_cmd(use_iRT, use_im)))

allcmds = easypqp_cmds


def main_easypqp() -> None:
	workdir.mkdir(exist_ok=overwrite)
	output_directory = workdir / 'easypqp_files'
	output_directory.mkdir(exist_ok=overwrite)
	if irt_choice is Irt_choice.iRT:
		irt_df.to_csv(irt_file, index=False, sep='\t', lineterminator='\n')
	elif irt_choice is Irt_choice.ciRT:
		shutil.copyfile(script_dir / 'hela_irtkit.tsv', irt_file)
	elif irt_choice is Irt_choice.Pierce_iRT:
		shutil.copyfile(script_dir / 'Pierce_iRT.tsv', irt_file)
	elif irt_choice is Irt_choice.userRT:
		shutil.copyfile(userRT_file, irt_file)
	if im_choice is Im_choice.userIM:
		shutil.copyfile(userIM_file, im_file)
	print(f'''Spectral library building
Commands to execute:
{allcmds}
{'~' * 69}''', flush=True)
	(output_directory / 'cmds.txt').write_text(allcmds)
	subprocess.run([os.fspath(easypqp), '--version'], check=True)
	parallel_convert = False
	procs = []
	if parallel_convert:
		for i, e in enumerate(easypqp_convert_cmds):
			while sum(p.poll() is None for p in procs) >= nproc:
				time.sleep(1)
			procs.append(subprocess.Popen(e, cwd=os_fspath(workdir), stdout=open(output_directory / f'easypqp_convert_{i}.log', 'w'), stderr=subprocess.STDOUT))
			print(f'Executing {e}')
	else:
		for i, e in enumerate(easypqp_convert_cmds):
			print(f'Executing {e}')
			subprocess.run(e, cwd=os_fspath(workdir))

	for p in procs:
		p.wait()
	for i, p in enumerate(procs):
		if p.returncode != 0:
			print("EasyPQP convert error BEGIN")
			try:
				print(open(output_directory / f'easypqp_convert_{i}.log').read(), end="")
			except OSError as e:
				print(e)
			print(f'exit status: {p.returncode}')
			print("EasyPQP convert error END")
	assert all(p.returncode == 0 for p in procs)
	p = subprocess.run(easypqp_library_cmd(use_iRT, use_im), cwd=os_fspath(workdir), check=False)
	if p.returncode != 0 and not use_iRT:
		print('''Not enough peptides could be found for alignment.
Using ciRT for alignment''')
		shutil.copyfile(script_dir / 'hela_irtkit.tsv', irt_file)
		p = subprocess.run(easypqp_library_cmd(True, use_im), cwd=os_fspath(workdir), check=False)
	if p.returncode != 0:
		print('''Library not generated, not enough peptides could be found for alignment.
Please try using other options for alignment (e.g. ciRT if used other options)''')
		sys.exit('Library not generated, not enough peptides could be found for alignment.')



##### multiple protein assignment to peptide reduced to single protein
# https://github.com/Nesvilab/Protid_largedatasets/blob/master/protxmlDtFdr.R

def format_con_lib_for_DIA_NN(t: pd.DataFrame):
	return t.rename({'Protein ID':'UniprotID',
			  'Entry Name':'ProteinName',
			  'ProteinName':'ProteinId'}, axis=1, inplace=False, errors='raise')


def easypqp_lib_export(lib_type: str) -> None:
	import pandas as pd

	easypqp_lib = pd.read_csv('easypqp_lib_openswath.tsv', sep='\t')

	frag_df = easypqp_lib['Annotation'].str.extract(r'^([abcxyz])(\d{1,2})(?:-(.*))?\^(\d+)$')
	frag_df.columns = 'FragmentType', 'FragmentSeriesNumber', 'FragmentLossType', 'FragmentCharge'
	frag_df = frag_df.reindex(columns=['FragmentType', 'FragmentCharge', 'FragmentSeriesNumber', 'FragmentLossType'], copy=False)

	def interp(t):
		return scipy.interpolate.interp1d(t.iloc[:, 1], t.iloc[:, 0], bounds_error=False)

	rt = easypqp_lib['NormalizedRetentionTime'].squeeze()
	align_files = list(pathlib.Path().glob('easypqp_rt_alignment_*.alignment_pkl'))
	avg_experimental_rt0 = np.nanmean([interp(pd.read_pickle(f))(rt) for f in align_files], axis=0)
	for e in align_files:
		e.unlink()
	avg_experimental_rt = pd.Series(avg_experimental_rt0, name='AverageExperimentalRetentionTime')
	if lib_type == 'Spectronaut':
		easypqp_lib['ModifiedPeptideSequence'] = easypqp_lib['ModifiedPeptideSequence'].str.replace('.(UniMod:', '(UniMod:', regex=False)
	pd.concat([easypqp_lib, frag_df, avg_experimental_rt], axis=1).to_csv(f'library.tsv', sep='\t', index=False)


main_easypqp()
os.chdir(os_fspath(workdir))
easypqp_lib_export('Spectronaut')
cwd = pathlib.Path()
if delete_temp_files:
	for f in easyPQP_tempfiles:
		try:
			f.unlink()
		except FileNotFoundError as e:
			lg.info(f'{f} does not exist')
os.chdir(CWD)

# Move alignment PDF files to easypqp_files directory
output_directory = os.path.join(workdir, "easypqp_files")
if not os.path.exists(output_directory):
	os.makedirs(output_directory)

for tt in glob.glob('easypqp_rt_alignment_*.pdf'):
	os.replace(os.path.join(workdir, tt), os.path.join(output_directory, tt))

for tt in glob.glob('easypqp_im_alignment_*.pdf'):
	os.replace(os.path.join(workdir, tt), os.path.join(output_directory, tt))


print('Done generating spectral library')
lg.info(f'took {datetime.timedelta(seconds=timeit.default_timer() - START)}')
# if __name__=='__main__':
# 	main()

