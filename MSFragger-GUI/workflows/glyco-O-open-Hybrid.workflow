# Workflow: glyco-O-open-Hybrid

crystalc.correct_isotope_error=false
crystalc.isotope_number=3
crystalc.max-charge=6
crystalc.precursor_isolation_window=0.7
crystalc.precursor_mass=20
crystalc.run-crystalc=true
database.decoy-tag=rev_
freequant.mz-tol=10
freequant.rt-tol=0.4
freequant.run-freequant=true
ionquant.imtol=0.05
ionquant.ionfdr=0.01
ionquant.label=
ionquant.mbr=0
ionquant.mbrimtol=0.05
ionquant.mbrmincorr=0
ionquant.mbrrttol=1
ionquant.mbrtoprun=3
ionquant.minfreq=0.5
ionquant.minions=1
ionquant.minisotopes=1
ionquant.writeindex=0
ionquant.mztol=10
ionquant.normalization=1
ionquant.peptidefdr=1
ionquant.proteinfdr=1
ionquant.requantify=1
ionquant.rttol=0.4
ionquant.run-ionquant=false
ionquant.tp=3
msfragger.Y_type_masses=0 203.07937 406.15874 568.21156 730.26438 892.3172 349.137279
msfragger.add_topN_complementary=0
msfragger.allow_multiple_variable_mods_on_residue=false
msfragger.allowed_missed_cleavage=1
msfragger.calibrate_mass=2
msfragger.clip_nTerm_M=true
msfragger.deisotope=1
msfragger.delta_mass_exclude_ranges=(-1.5,3.5)
msfragger.deltamass_allowed_residues=all
msfragger.diagnostic_fragments=204.086646 186.076086 168.065526 366.139466 144.0656 138.055 512.197375 292.1026925 274.0921325 657.2349 243.026426 405.079246 485.045576 308.09761
msfragger.diagnostic_intensity_filter=0.1
msfragger.digest_max_length=50
msfragger.digest_min_length=7
msfragger.fragment_ion_series=b,y,c,z,Y
msfragger.fragment_mass_tolerance=20
msfragger.fragment_mass_units=1
msfragger.intensity_transform=0
msfragger.ion_series_definitions=
msfragger.isotope_error=0
msfragger.labile_search_mode=labile
msfragger.localize_delta_mass=true
msfragger.mass_diff_to_variable_mod=0
msfragger.mass_offsets=0
msfragger.max_fragment_charge=2
msfragger.max_variable_mods_combinations=5000
msfragger.max_variable_mods_per_peptide=3
msfragger.min_fragments_modelling=2
msfragger.min_matched_fragments=4
msfragger.minimum_peaks=15
msfragger.minimum_ratio=0.00
msfragger.misc.fragger.clear-mz-hi=0
msfragger.misc.fragger.clear-mz-lo=0
msfragger.misc.fragger.digest-mass-hi=5000
msfragger.misc.fragger.digest-mass-lo=400
msfragger.misc.fragger.enzyme-dropdown=trypsin
msfragger.misc.fragger.precursor-charge-hi=4
msfragger.misc.fragger.precursor-charge-lo=1
msfragger.misc.fragger.remove-precursor-range-hi=3.5
msfragger.misc.fragger.remove-precursor-range-lo=-1.5
msfragger.misc.slice-db=1
msfragger.num_enzyme_termini=2
msfragger.output_format=pepXML
msfragger.output_max_expect=50
msfragger.output_report_topN=1
msfragger.override_charge=false
msfragger.precursor_mass_lower=-200
msfragger.precursor_mass_mode=corrected
msfragger.precursor_mass_units=0
msfragger.precursor_mass_upper=4000
msfragger.precursor_true_tolerance=20
msfragger.precursor_true_units=1
msfragger.remove_precursor_peak=2
msfragger.report_alternative_proteins=false
msfragger.run-msfragger=true
msfragger.search_enzyme_butnotafter=P
msfragger.search_enzyme_cutafter=KR
msfragger.search_enzyme_name=Trypsin
msfragger.table.fix-mods=0.00000,C-Term Peptide,true,-1; 0.00000,N-Term Peptide,true,-1; 0.00000,C-Term Protein,true,-1; 0.00000,N-Term Protein,true,-1; 0.00000,G (glycine),true,-1; 0.00000,A (alanine),true,-1; 0.00000,S (serine),true,-1; 0.00000,P (proline),true,-1; 0.00000,V (valine),true,-1; 0.00000,T (threonine),true,-1; 57.02146,C (cysteine),true,-1; 0.00000,L (leucine),true,-1; 0.00000,I (isoleucine),true,-1; 0.00000,N (asparagine),true,-1; 0.00000,D (aspartic acid),true,-1; 0.00000,Q (glutamine),true,-1; 0.00000,K (lysine),true,-1; 0.00000,E (glutamic acid),true,-1; 0.00000,M (methionine),true,-1; 0.00000,H (histidine),true,-1; 0.00000,F (phenylalanine),true,-1; 0.00000,R (arginine),true,-1; 0.00000,Y (tyrosine),true,-1; 0.00000,W (tryptophan),true,-1; 0.00000,B ,true,-1; 0.00000,J,true,-1; 0.00000,O,true,-1; 0.00000,U,true,-1; 0.00000,X,true,-1; 0.00000,Z,true,-1
msfragger.table.var-mods=15.99490,M,true,3; 42.01060,[^,true,1; 79.96633,STY,false,3; -17.02650,nQnC,false,1; -18.01060,nE,false,1; 0.00000,site_06,false,3; 0.00000,site_07,false,3
msfragger.track_zero_topN=0
msfragger.use_topN_peaks=300
msfragger.write_calibrated_mgf=false
msfragger.zero_bin_accept_expect=0.00
msfragger.zero_bin_mult_expect=1.00
peptide-prophet.cmd-opts=--nonparam --expectscore --decoyprobs --masswidth 4000.0 --clevel -2
peptide-prophet.combine-pepxml=true
peptide-prophet.run-peptide-prophet=true
phi-report.dont-use-prot-proph-file=false
phi-report.filter=--sequential --razor --prot 0.01 --mapmods
phi-report.pep-level-summary=false
phi-report.print-decoys=false
phi-report.run-report=true
phi-report.write-mzid=false
protein-prophet.cmd-opts=--maxppmdiff 2000000
protein-prophet.run-protein-prophet=true
ptmshepherd.annotation_tol=0.01
ptmshepherd.histo_smoothbins=2
ptmshepherd.localization_background=4
ptmshepherd.output_extended=false
ptmshepherd.peakpicking_mass_units=0
ptmshepherd.peakpicking_promRatio=0.3
ptmshepherd.peakpicking_width=0.002
ptmshepherd.precursor_mass_units=0
ptmshepherd.precursor_tol=0.01
ptmshepherd.run-shepherd=true
ptmshepherd.varmod_masses=Failed_Carbamidomethylation\:-57.021464
quantitation.run-label-free-quant=false
speclibgen.easypqp.extras.rt_lowess_fraction=0.05
speclibgen.easypqp.rt-cal=noiRT
speclibgen.easypqp.select-file.text=
speclibgen.run-speclibgen=false
speclibgen.use-easypqp=false
speclibgen.use-spectrast=true
tmtintegrator.add_Ref=-1
tmtintegrator.allow_overlabel=true
tmtintegrator.allow_unlabeled=true
tmtintegrator.best_psm=true
tmtintegrator.channel_num=6
tmtintegrator.dont-run-fq-lq=false
tmtintegrator.freequant=--ptw 0.4 --tol 10 --isolated
tmtintegrator.groupby=0
tmtintegrator.labelquant=--tol 20 --level 2
tmtintegrator.max_pep_prob_thres=0
tmtintegrator.min_ntt=0
tmtintegrator.min_pep_prob=0.9
tmtintegrator.min_percent=0.05
tmtintegrator.min_purity=0.5
tmtintegrator.min_site_prob=-1
tmtintegrator.mod_tag=none
tmtintegrator.ms1_int=true
tmtintegrator.outlier_removal=true
tmtintegrator.print_RefInt=false
tmtintegrator.prot_exclude=none
tmtintegrator.prot_norm=0
tmtintegrator.psm_norm=false
tmtintegrator.ref_tag=Bridge
tmtintegrator.run-tmtintegrator=false
tmtintegrator.top3_pep=true
tmtintegrator.unique_gene=0
tmtintegrator.unique_pep=false
workflow.description=<p style\="margin-top\: 0"> For hybrid activation open search of O-glycopeptides </p>
workflow.input.data-type.im-ms=false
workflow.input.data-type.regular-ms=true
workflow.process-exps-separately=false
workflow.saved-with-ver=13.0-RC8
