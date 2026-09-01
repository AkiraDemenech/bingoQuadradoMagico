latex:
	for t in $$(ls *.tex); \
	do \
		echo $$t; \
		pdflatex -interaction=nonstopmode $$t; \
	done

tex:	latex

clear:	clean
	for t in $$(ls *.tex); \
	do \
		n="$$(basename $$t)"; \
		b="$${n%.*}.pdf"; \
		echo $$b; \
		rm -f $$b; \
	done

clean:
	realpath ./ *.tex
	for e in $$(cat .gitignore); \
	do \
		echo "$$e"; \
		ls $$e; \
		rm -f $$e; \
	done
	
zip:	
	echo $$(ls *.tex).zip 
	zip -r $$(ls *.tex).zip ./
