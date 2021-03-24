# Workflow: TMT16

AdjustFragIntensity=true
BoostComplementaryIon=false
CorrThreshold=0
DeltaApex=0.2
RFmax=500
RPmax=25
RTOverlap=0.3
SE.EstimateBG=false
SE.MS1PPM=10
SE.MS2PPM=20
SE.MassDefectFilter=true
SE.MinMSIntensity=1
SE.MinMSMSIntensity=1
SE.NoMissedScan=1
WindowSize=10
SE.SN=1.1
SE.MS2SN=1.1
SE.IsoPattern=0.3
SE.MassDefectOffset=0.1
ExportPrecursorPeak=false
Q1 = true
Q2 = true
Q3 = true
run-diaumpire=false
crystalc.run-crystalc=false
database.decoy-tag=rev_
freequant.mz-tol=10
freequant.rt-tol=0.4
freequant.run-freequant=false
ionquant.excludemods=
ionquant.heavy=
ionquant.imtol=0.05
ionquant.ionfdr=0.01
ionquant.light=
ionquant.mbr=0
ionquant.mbrimtol=0.05
ionquant.mbrmincorr=0
ionquant.mbrrttol=1
ionquant.mbrtoprun=10
ionquant.medium=
ionquant.minexps=1
ionquant.minfreq=0.5
ionquant.minions=2
ionquant.minisotopes=2
ionquant.minscans=3
ionquant.mztol=10
ionquant.normalization=1
ionquant.peptidefdr=1
ionquant.proteinfdr=1
ionquant.proteinquant=2
ionquant.requantify=1
ionquant.rttol=0.4
ionquant.run-ionquant=true
ionquant.tp=3
ionquant.writeindex=0
msfragger.data_type=0
msfragger.Y_type_masses=
msfragger.add_topN_complementary=0
msfragger.allow_multiple_variable_mods_on_residue=false
msfragger.allowed_missed_cleavage=2
msfragger.calibrate_mass=2
msfragger.clip_nTerm_M=true
msfragger.deisotope=1
msfragger.deneutralloss=1
msfragger.delta_mass_exclude_ranges=(-1.5,3.5)
msfragger.diagnostic_fragments=
msfragger.diagnostic_intensity_filter=0
msfragger.digest_max_length=50
msfragger.digest_min_length=7
msfragger.fragment_ion_series=b,y
msfragger.fragment_mass_tolerance=20
msfragger.fragment_mass_units=1
msfragger.intensity_transform=0
msfragger.ion_series_definitions=
msfragger.isotope_error=-1/0/1/2/3
msfragger.labile_search_mode=off
msfragger.localize_delta_mass=false
msfragger.mass_diff_to_variable_mod=0
msfragger.mass_offsets=0
msfragger.max_fragment_charge=2
msfragger.max_variable_mods_combinations=5000
msfragger.max_variable_mods_per_peptide=3
msfragger.min_fragments_modelling=2
msfragger.min_matched_fragments=4
msfragger.minimum_peaks=15
msfragger.minimum_ratio=0.01
msfragger.misc.fragger.clear-mz-hi=134.5
msfragger.misc.fragger.clear-mz-lo=125.5
msfragger.misc.fragger.digest-mass-hi=5000
msfragger.misc.fragger.digest-mass-lo=200
msfragger.misc.fragger.enzyme-dropdown=stricttrypsin
msfragger.misc.fragger.precursor-charge-hi=4
msfragger.misc.fragger.precursor-charge-lo=1
msfragger.misc.fragger.remove-precursor-range-hi=1.5
msfragger.misc.fragger.remove-precursor-range-lo=-1.5
msfragger.misc.slice-db=1
msfragger.num_enzyme_termini=2
msfragger.output_format=pepXML
msfragger.output_max_expect=50
msfragger.output_report_topN=1
msfragger.override_charge=false
msfragger.precursor_mass_lower=-20
msfragger.precursor_mass_mode=selected
msfragger.precursor_mass_units=1
msfragger.precursor_mass_upper=20
msfragger.precursor_true_tolerance=20
msfragger.precursor_true_units=1
msfragger.remove_precursor_peak=0
msfragger.report_alternative_proteins=false
msfragger.restrict_deltamass_to=all
msfragger.run-msfragger=true
msfragger.search_enzyme_butnotafter=
msfragger.search_enzyme_cutafter=KR
msfragger.search_enzyme_name=stricttrypsin
msfragger.table.fix-mods=0.000000,C-Term Peptide,true,-1; 0.000000,N-Term Peptide,true,-1; 0.000000,C-Term Protein,true,-1; 0.000000,N-Term Protein,true,-1; 0.000000,G (glycine),true,-1; 0.000000,A (alanine),true,-1; 0.000000,S (serine),true,-1; 0.000000,P (proline),true,-1; 0.000000,V (valine),true,-1; 0.000000,T (threonine),true,-1; 57.021460,C (cysteine),true,-1; 0.000000,L (leucine),true,-1; 0.000000,I (isoleucine),true,-1; 0.000000,N (asparagine),true,-1; 0.000000,D (aspartic acid),true,-1; 0.000000,Q (glutamine),true,-1; 304.207146,K (lysine),true,-1; 0.000000,E (glutamic acid),true,-1; 0.000000,M (methionine),true,-1; 0.000000,H (histidine),true,-1; 0.000000,F (phenylalanine),true,-1; 0.000000,R (arginine),true,-1; 0.000000,Y (tyrosine),true,-1; 0.000000,W (tryptophan),true,-1; 0.000000,B ,true,-1; 0.000000,J,true,-1; 0.000000,O,true,-1; 0.000000,U,true,-1; 0.000000,X,true,-1; 0.000000,Z,true,-1
msfragger.table.var-mods=15.994900,M,true,3; 42.010600,[^,true,1; 79.966330,STY,false,3; -17.026500,nQnC,false,1; -18.010600,nE,false,1; 304.207146,n^,true,1; 229.162930,S,false,1; 0.000000,site_08,false,1; 0.000000,site_09,false,1; 0.000000,site_10,false,1; 0.000000,site_11,false,1; 0.000000,site_12,false,1; 0.000000,site_13,false,1; 0.000000,site_14,false,1; 0.000000,site_15,false,1; 0.000000,site_16,false,1
msfragger.track_zero_topN=0
msfragger.use_topN_peaks=150
msfragger.write_calibrated_mgf=false
msfragger.zero_bin_accept_expect=0
msfragger.zero_bin_mult_expect=1
peptide-prophet.cmd-opts=--decoyprobs --ppm --accmass --nonparam --expectscore
peptide-prophet.combine-pepxml=false
peptide-prophet.run-peptide-prophet=true
phi-report.dont-use-prot-proph-file=false
phi-report.filter=--sequential --razor --picked --prot 0.01
phi-report.pep-level-summary=false
phi-report.print-decoys=false
phi-report.run-report=true
protein-prophet.cmd-opts=--maxppmdiff 2000000 --minprob 0.9
protein-prophet.run-protein-prophet=true
ptmprophet.cmdline=
ptmprophet.run-ptmprophet=false
ptmshepherd.annotation-common=false
ptmshepherd.annotation-custom=false
ptmshepherd.annotation-unimod=true
ptmshepherd.annotation_file=
ptmshepherd.annotation_tol=0.01
ptmshepherd.cap_y_ions=
ptmshepherd.diag_ions=
ptmshepherd.glyco_mode=false
ptmshepherd.histo_smoothbins=2
ptmshepherd.iontype_a=false
ptmshepherd.iontype_b=true
ptmshepherd.iontype_c=false
ptmshepherd.iontype_x=false
ptmshepherd.iontype_y=true
ptmshepherd.iontype_z=false
ptmshepherd.localization_background=4
ptmshepherd.output_extended=false
ptmshepherd.peakpicking_mass_units=0
ptmshepherd.peakpicking_promRatio=0.3
ptmshepherd.peakpicking_width=0.002
ptmshepherd.precursor_mass_units=0
ptmshepherd.precursor_tol=0.01
ptmshepherd.remainder_masses=
ptmshepherd.run-shepherd=false
ptmshepherd.spectra_maxfragcharge=2
ptmshepherd.varmod_masses=Failed_Carbamidomethylation:-57.021464
quantitation.run-label-free-quant=false
speclibgen.easypqp.extras.rt_lowess_fraction=0.01
speclibgen.easypqp.rt-cal=noiRT
speclibgen.easypqp.select-file.text=
speclibgen.run-speclibgen=false
speclibgen.use-easypqp=false
speclibgen.use-spectrast=true
tmtintegrator.add_Ref=1
tmtintegrator.allow_overlabel=true
tmtintegrator.allow_unlabeled=false
tmtintegrator.best_psm=true
tmtintegrator.channel_num=16
tmtintegrator.dont-run-fq-lq=false
tmtintegrator.freequant=--ptw 0.4 --tol 10 --isolated
tmtintegrator.groupby=0
tmtintegrator.labelquant=--tol 20
tmtintegrator.quant_level=2
tmtintegrator.max_pep_prob_thres=0.9
tmtintegrator.min_ntt=0
tmtintegrator.aggregation_method=0
tmtintegrator.min_pep_prob=0.9
tmtintegrator.min_percent=0.05
tmtintegrator.min_purity=0.5
tmtintegrator.min_site_prob=-1
tmtintegrator.mod_tag=none
tmtintegrator.ms1_int=true
tmtintegrator.outlier_removal=true
tmtintegrator.print_RefInt=false
tmtintegrator.prot_exclude=none
tmtintegrator.prot_norm=1
tmtintegrator.psm_norm=false
tmtintegrator.ref_tag=Bridge
tmtintegrator.run-tmtintegrator=true
tmtintegrator.top3_pep=true
tmtintegrator.unique_gene=0
tmtintegrator.unique_pep=false
workflow.description=<p style\="margin-top\: 0"> Basic TMT 16-plex workflow, with quantification and identification from MS2. Met oxidation, protein N-term Acetyl, n-term TMT are specified as variable modifications. TMT-Integrator with virtual reference approach, median-centering normalization, data summarization at the gene level. If a reference/bridge sample is available, specify the corresponding channel/sample name tag in the annotation file(s) and in TMT-Integrator tab. </p>
workflow.input.data-type.im-ms=false
workflow.input.data-type.regular-ms=true
workflow.process-exps-separately=false
workflow.saved-with-ver=14.0-rc2
