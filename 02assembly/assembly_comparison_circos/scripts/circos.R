require(circlize)

output = snakemake@output[[1]]
pdf(output, width = 8, height = 8)#, res = 300, units = 'in', type = 'cairo')

#rRNA. if this file is empty, don't plot highlight points.
highlight = tryCatch({
	read.table(snakemake@input[[3]])
	},
	error = function(cond) {},
	finally = {draw.highlights = FALSE}
)
#rRNA intensities. IF this file is empty, don't plot, just produce an empty matrix.
highlight.intensities = tryCatch({
	read.table(snakemake@input[[4]])
	},
	error = function(cond) {return(matrix(ncol=2, nrow = 0))}
)

#load contig alignments
contig.alignments = unlist(snakemake@input)[5:length(snakemake@input)]
print(contig.alignments)
timepoint = sapply(contig.alignments, function(x) strsplit(strsplit(basename(x), '\\.')[[1]][1], '_')[[1]][2])
condition = sapply(contig.alignments, function(x) strsplit(strsplit(basename(x), '\\.')[[1]][1], '_')[[1]][1])

contig.alignments = data.frame(contig.alignments, timepoint, condition)
print(contig.alignments)
#if some contigs should be plotted darker, load that file. if it's empty, return an empty matrix.
dark.contigs = tryCatch({
		read.table(snakemake@input[[2]])
	},
	error = function(cond){
		return(matrix(ncol=4, nrow = 0))
	}
)
colnames(dark.contigs) = c('assembly', 'condition', 'timepoint', 'contig')
if (nrow(dark.contigs)!=0){
	dark.contigs = merge(dark.contigs, contig.alignments)
}

#load the reference sequence used in the alignments.
genome = read.table(snakemake@input[[1]])

#aesthetic knobs
highlight_size = 1.2
tick.interval = 0.5e6
track.height = 0.5
contig.alpha = 0.3
highlight_offset = 1.2

#track colors. one of these is taken directly from the Snakemake config, but can be hard-coded.
color1 = "#241E1E"
color2 = snakemake@params[[1]] #"#557BB8"
color3 = "#5AC6E2"

#ready the colors for plotting by altering their transparency
bed1.color = adjustcolor(color1, alpha = contig.alpha)
bed2.color = adjustcolor(color2, alpha = contig.alpha)
bed3.color = adjustcolor(color3, alpha = contig.alpha)
bed.colors.faint = c(bed1.color, bed2.color, bed3.color)

bed1.color = adjustcolor(color1, alpha = 0.8)
bed2.color = adjustcolor(color2, alpha = 0.9)
bed3.color = adjustcolor(color3, alpha = 0.9)
bed.colors.bold = c(bed1.color, bed2.color, bed3.color)


#set highlight colors and transparencies. Not used if highlight files are empty.
locus.alpha = 1

color.highlight = rgb(0.8, 0.3, 0.1, alpha = locus.alpha)
color.highlight2 = rgb(0, 0.7, 0.5, alpha = locus.alpha)
highlight.colors = c(color.highlight, color.highlight2)

contig_height = 0.5
min.contig.size = 0
contig.shave.width = 1000

#initialize genome plot
genome = genome[genome[,2] > min.contig.size,] #filter small contigs from the assembly
par(mar =c(2, 2, 2, 2)) #set figure margins
circos.par("track.height" = track.height,canvas.xlim =c(-1, 1), canvas.ylim =c(-1, 1), "start.degree" = 90)  #set circos orientation and location
cytoband = data.frame(genome[,1], rep(0, nrow(genome)), genome[,2], genome[,1], rep('foo', nrow(genome))) #frankly, I don't remember
cytoband[,1] = as.character(cytoband[,1]) #shrug
circos.initializeWithIdeogram(cytoband=cytoband, plotType = NULL) #initialize the plot
genome.length = sum(cytoband[,3]) #get total length...
breaks = seq(0, genome.length, by = tick.interval) #...and divide in order to obtain tick intervals.

#CONTIGS
for (tp in unique(timepoint)){

	#group the contigs together in one list for plotting
	beds = contig.alignments$contig.alignments[contig.alignments$timepoint == tp]

	contig.list = lapply(beds, function(bed){
		contigs1 = read.table(as.character(bed), sep = "")
		contigs1 = contigs1[contigs1[,3] - contigs1[,2] > min.contig.size, ]
		contigs1[,2] = contigs1[,2] + contig.shave.width
		contigs1[,3] = contigs1[,3] - contig.shave.width
		contigs1
	})
	#plot the contigs
	circos.genomicTrackPlotRegion(contig.list, bg.border = NA, stack = TRUE, track.height = track.height, ylim = c(0,0.5), panel.fun =function(region, value, ...) {
		i = getI(...)
		col = bed.colors.faint[i]
		circos.genomicRect(region, value, col = col, border = "white", ytop = i + contig_height, ybottom = i - contig_height, ...)

		#endarken darker contigs
		if (nrow(dark.contigs) != 0){
			to_darken = which(as.character(value[,1]) %in% as.character(dark.contigs$contig[dark.contigs$timepoint == tp]))
		}
		else{
			to_darken= which(value[,1] %in% value[,1])
		}
		region.dark = region[to_darken,]
		value.dark = value[to_darken,]

		col = bed.colors.bold[i]
		if (length(value.dark) > 0){
			circos.genomicRect(region.dark, value.dark, col = col, border = "white", ytop = i + contig_height, ybottom = i - contig_height, ...)
		}

		#draw axis on the first track
		if (tp == unique(timepoint)[1]){
			circos.axis(h = "top", major.at = breaks, labels = c('', '', '1', '', '2', '', '3', '', '4', '', '5', '', '6'), minor.ticks = 0,
								major.tick.percentage = 0.2, labels.away.percentage = 0.05, labels.cex = 1.5)
		}
	})
}

#everything below this is for plotting callout points, e.g. indicating gene locations or some such. Generally not used.


#deduplicate highlight sequence beds
#highlight_interval = 30000
#breaks = seq(1, max(highlight[,2]), highlight_interval)
#highlight[,2] = breaks[cut(highlight[,2], breaks, labels = FALSE)+1]
#highlight[,3] = highlight[,2] + 1000
#highlight = unique(highlight)
if (draw.highlights){
	highlight = highlight[order(highlight[,2]),]
	highlight = cbind(highlight[,c(1,2)], highlight[,4])


	if (length(strsplit(as.character(highlight[1,3]), ';')[[1]]) > 1){
		#color the highlights by the first ';' delimited portion of their original sequence names.
		highlight$type = sapply(highlight[,3], function(x) strsplit(as.character(x), ';')[[1]][1])
	} else {
		#don't.
		highlight$type = rep('foo', nrow(highlight))
	}


	#print(head(highlight))
	#print(head(highlight.intensities))
	#print(timepoint)
	colnames(highlight) = c('Ref.contig', 'Coord', 'Highlight.seq', 'Group.member')

	if (nrow(highlight.intensities) > 0){
		colnames(highlight.intensities) = c('Highlight.seq', unique(sort(timepoint)))
		#intensities over 1 are reduced to 1
		#highlight.intensities[,-c(1)][highlight.intensities[,-c(1)]>1] = 1
		highlight.intensities[,-c(1)] = highlight.intensities[,-c(1)] / max(highlight.intensities[,-c(1)])
	}

	#HIGHLIGHTED SEQUENCES
	for (tp in sort(unique(timepoint))){
		if (nrow(highlight.intensities) > 0){
			highlight.merge = merge(highlight, highlight.intensities)
			highlight.merge = highlight.merge[,c(-1)]
			highlight.merge = highlight.merge[c(1,2,which(colnames(highlight.merge) == tp),3)]
		}
		else
			highlight.merge = highlight

		#print(head(highlight))
		highlight.merge$Group.member = factor(highlight.merge$Group.member)
		levels(highlight.merge$Group.member) = c(TRUE, FALSE)

		bedlist = list(
			highlight.merge[highlight.merge$Group.member == TRUE,],
			highlight.merge[highlight.merge$Group.member == FALSE,]
		)
	#print(bedlist)
}
	circos.genomicTrackPlotRegion(bedlist[[1]], stack = FALSE, bg.border = NA, track.height = track.height, ylim = c(0,1), panel.fun =function(region, value, ...) {
		i = getI(...)
		color = highlight.colors[i]

		data = region[region[,2] >= 0,]
		circos.points(data[,1], rep(length(unique(timepoint)) + highlight_offset , nrow(data)), pch = 1, col = color, cex = highlight_size)
		circos.points(data[,1], rep(length(unique(timepoint)) + highlight_offset , nrow(data)), pch = 16, col = color, cex = (data[,2]) * highlight_size)

		no_data = region[region[,2] < 0,]
		circos.points(no_data[,1], rep(length(unique(timepoint)) + highlight_offset , nrow(no_data)), pch = 4, col = color, cex = highlight_size)

		if (nrow(highlight.intensities) == 0){
			data = region
			circos.points(data[,1], rep(length(unique(timepoint)) + highlight_offset, nrow(data)), pch = 16, col = color, cex = highlight_size)
		}
	})
}

circos.clear()
dev.off()
