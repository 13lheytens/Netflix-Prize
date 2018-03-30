FILES :=                              \
    Netflix.html                      \
    Netflix.py                        \
    RunNetflix.in                     \
    RunNetflix.out                    \
    RunNetflix.py                     \
    TestNetflix.out                   \
    TestNetflix.py

COVERAGE := coverage-3.5
PYLINT   := pylint

.pylintrc:
	$(PYLINT) --disable=bad-whitespace,missing-docstring,pointless-string-statement,too-many-public-methods,global-statement  --reports=n --generate-rcfile > $@

Netflix.html: Netflix.py
	pydoc3 -w Netflix

RunNetflix.tmp: .pylintrc RunNetflix.in RunNetflix.out RunNetflix.py
	-$(PYLINT) Netflix.py
	-$(PYLINT) RunNetflix.py
	./RunNetflix.py < RunNetflix.in > RunNetflix.tmp
	python3 -m cProfile RunNetflix.py < RunNetflix.in > RunNetflix.tmp

RunProbe: .pylintrc RunNetflix.py
	-$(PYLINT) Netflix.py
	-$(PYLINT) RunNetflix.py
	python3 RunNetflix.py < probe.txt > probe.out

TestNetflix.out: .pylintrc TestNetflix.py
	-$(PYLINT) Netflix.py
	-$(PYLINT) TestNetflix.py
	$(COVERAGE) run    --branch TestNetflix.py >  TestNetflix.out 2>&1
	$(COVERAGE) report --omit=/lusr/lib/python3.5/site-packages/numpy/ -m                      >> TestNetflix.out
	cat TestNetflix.out

check:
	@not_found=0;                                 \
    for i in $(FILES);                            \
    do                                            \
        if [ -e $$i ];                            \
        then                                      \
            echo "$$i found";                     \
        else                                      \
            echo "$$i NOT FOUND";                 \
            not_found=`expr "$$not_found" + "1"`; \
        fi                                        \
    done;                                         \
    if [ $$not_found -ne 0 ];                     \
    then                                          \
        echo "$$not_found failures";              \
        exit 1;                                   \
    fi;                                           \
    echo "success";

clean:
	rm -f  .coverage
	rm -f  .pylintrc
	rm -f  *.pyc
	rm -f  Netflix.html
	rm -f  RunNetflix.tmp
	rm -f  TestNetflix.out
	rm -f  probe.out
	rm -rf __pycache__

config:
	git config -l

format:
	autopep8 -i Netflix.py
	autopep8 -i RunNetflix.py
	autopep8 -i TestNetflix.py

status:
	make clean
	@echo
	git branch
	git remote -v
	git status

test: Netflix.html RunNetflix.tmp TestNetflix.out check
