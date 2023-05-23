.PHONY: all clean cleanall

all: ../report/documento.pdf

documento.pdf: ../report/documento.tex bibliografia.bib
	pdflatex documento.tex
	biber documento
	pdflatex documento.tex
	pdflatex documento.tex

clean:
	rm -f *.aux *.blg *.bbl *.toc *.log *.lof *.lot *.log.xml *.bcf *.out *.run.xml

cleanall: clean
	rm -f documento.pdf

