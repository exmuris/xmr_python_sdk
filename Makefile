
.PHONY: test
test:
	coverage run -m unittest discover -v tests && \
	coverage report -m

.PHONY: build
build:
	rm -rf dist
	poetry build
