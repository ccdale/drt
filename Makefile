vfn=drt/__init__.py
dev:
	buildn=$$(sed -n 's/buildv = \([0-9]\+\)/\1/p' $(vfn) );\
		   buildn=$$(( buildn + 1 ));\
		   sed -i "/buildv =/s/[0-9]\+/$$buildn/" $(vfn)
	git add $(vfn)
	git commit -m "bumping build version"
	pip install -e .

sdist:
	python setup.py sdist

bdist:
	python setup.py bdist_wheel
