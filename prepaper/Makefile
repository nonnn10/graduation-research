# Created by Daichi Toma on Nov 16, 2011

TARGET=finalpre

LATEX=uplatex
BIBTEX=pbibtex
DVIPDF=dvipdfmx -p a4
#You need setting "-l" option if You think You get a landscape PDF
#DVIPDF_OPT=-l

#Embed fonts
#DVIPDF_OPT=-f hiraginoEmbed.map

.SUFFIXES: .tex .dvi .pdf

.tex.dvi:
	$(LATEX) $<
	#$(BIBTEX) $(TARGET)
	$(LATEX) $<
	$(LATEX) $<

.dvi.pdf:
	$(DVIPDF) $(DVIPDF_OPT) $<


all: $(TARGET).pdf
	open $(TARGET).pdf

dvi: $(TARGET).dvi

pdf: $(TARGET).pdf


clean:
	rm -f *.dvi *.aux *.log  *.ps *.gz *.bbl *.blg *.toc *~ *.core *.fdb_latexmk  *.fls

