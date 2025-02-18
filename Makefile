.PHONY: prepare-env

prepare-env:
	@echo "Creating directories and setting permissions..."
	@mkdir -p core
	@mkdir -p core-logs
	@mkdir -p core-data
	@chmod -R 777 core
	@chmod -R 777 core-logs
	@chmod -R 777 core-data
	@echo "Environment prepared successfully"

