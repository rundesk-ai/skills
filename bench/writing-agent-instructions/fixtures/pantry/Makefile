.PHONY: run test check fmt release

run:
	python3 -m pantry

test:
	python3 -m unittest discover -s tests -t .

# The gate: formats the code, then runs the tests.
check:
	python3 tools/fmt.py --write pantry tests
	python3 -m unittest discover -s tests -t .

fmt:
	python3 tools/fmt.py --write pantry tests

release:
	python3 tools/bump.py
	git commit -am "Release $$(cat VERSION)"
	git tag "v$$(cat VERSION)"
