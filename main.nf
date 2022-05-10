#! /usr/bin/env nextflow

println "\nThis pipeline creates blast-database and BLAST your query against to it. After that alignment and clustering will be performed."

nextflow.enable.dsl = 1

def helpMessage(){
	log.info """
		Usage:
        	To running this pipeline:
        	
        	nextflow run main.nf --createdb (createdb is optional)

       		Optional arguments
       		--createdb                     You can specify proteome fasta file (.fasta format) to make blast database
        	--help                         Help documentation.

        	Other arguments were described in the file called "nextflow.config."
		"""
}


// Display help documentation

if (params.help) {
	helpMessage()
	exit 0
}

//setting Channels

Channel
	.fromPath(params.query)
	.splitFasta(by:params.chunkSize, file:true)
	.set{queryFile_ch}


//WORK-1 (Creating BLAST Database)

if (params.createdb) {
	createdbfile_ch=Channel
		.fromPath(params.createdb)
		.map{file -> tuple(file.simpleName, file.parent, file)}

	process MakeBlastDB {
                input:
		set val(db_name),path(dbpath),file(FILE) from createdbfile_ch
		output:
		val db_name into db_name_ch
		path dbpath into dbpath_ch
		
		script:
                """
                makeblastdb -in ${params.createdb} -parse_seqids -dbtype 'prot' -out $dbpath/$db_name
                """
        }       
} else {

Channel
	.fromPath(params.dbpath)
	.set{dbpath_ch}

Channel
	.from(params.db_name)
	.set{db_name_ch}
}


//WORK-2 (Running BLAST)

process PerformBlast {
	container="ncbi/blast"
	publishDir "${params.outdir}/blastout"

	input:
	path queryFile from queryFile_ch	
	path dbpath from dbpath_ch.val
	val db_name from db_name_ch.val

	output:
	path(params.blastoutput) into blast_output_ch

	script:
	"""
	$params.app -num_threads $params.threads -query $queryFile -db $dbpath/$db_name -max_target_seqs $params.options -outfmt $params.outfmt -out $params.blastoutput
	"""
}

blast_output_ch
	.collectFile(name: 'blast_output_all.txt', storeDir: params.outdir)
	.set{pre_align_ch}


//WORK-3 (Getting FASTA Sequences of BLAST Outputs)

project_dir = projectDir

process GettingFasta {
	publishDir "${params.outdir}/1_PRE-ALIGNMENT"

	input:	
	path file from pre_align_ch
	output:
	path (params.outdbname) into pre_align_out_ch

	"""
	python $project_dir/scripts/gettingFasta.py --input "${file}" --database $params.db
	"""  
}


//WORK-4 (Global Alignment with Clustal Omega)

process GlobalAlignment {
	publishDir "${params.outdir}/2_GLOBAL-ALIGNMENT"

	input:	
	path x from pre_align_out_ch
	output:
	path (params.matrix) into alignment_out_ch

	script:
	"""
	$project_dir/scripts/./clustalo -i ${x} --distmat-out=${params.matrix} --guidetree-out=dnd_file -o $params.outFilename --outfmt=clustal -v --full
	"""
}


//WORK-5 (Getting Similarity Score Matrix from Alignment)

process SimilarityScoring {
	publishDir "${params.outdir}/3_SIMILARITY-SCORE-MATRIX"

	input:	
	file y from alignment_out_ch
	output:
	path (params.table) into similarityScore_ch

	"""
	python $project_dir/scripts/pretable.py --input "${params.matrix}"
	"""
}

process ScoreMatrix {
	publishDir "${params.outdir}/4-MATRIX"

	input:	
	file z from similarityScore_ch
	output:
	path (params.finaltable) into ScoreMatrix_ch

	"""
	python $project_dir/scripts/table.py --input "${z}"
	"""
}

process ClusterMapping {
	publishDir "${params.outdir}/5-CLUSTERMAP"

	input:	
	file t from ScoreMatrix_ch
	output:
	path (params.map) into clustermap_ch

	"""
	python $project_dir/scripts/clustermapper.py --input "${t}"
	"""
}