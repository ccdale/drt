vfn=drt/__init__.py
dev:
	buildn=$$(sed -n 's/buildv = \([0-9]\+\)/\1/p' $(vfn) );\
		   buildn=$$(( buildn + 1 ));\
		   sed -i "/buildv =/s/[0-9]\+/$$buildn/" $(vfn)
	pandoc --from=markdown --to=rst --output=README.rst README.md
	git add $(vfn)
	git add README.rst
	git commit -m "bumping build version"
	pip install -e .

sdist:
	rm -rf dist/
	rm -rf build/
	python setup.py sdist

bdist: sdist
	python setup.py bdist_wheel

upload: bdist
	twine upload --repository testpypi dist/*
