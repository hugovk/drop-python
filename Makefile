help:
	@echo "make help     -- print this help"
	@echo "make generate -- regenerate the files"
	@echo "make update   -- upload the json and index.html to s3"

generate:
	python3 generate.py --version 2.6
	python3 generate.py --version 3.2
	python3 generate.py --version 3.3

update:
	/usr/local/bin/s3cmd put index.html s3://wheelpackages/index.html  --cf-invalidate \
	--add-header='Cache-Control: max-age=30' \
	--add-header='Date: `date -u +"%a, %d %b %Y %H:%M:%S GMT"`'
	/usr/local/bin/s3cmd put results.json s3://wheelpackages/results.json  --cf-invalidate \
	--add-header='Cache-Control: max-age=30' \
	--add-header='Date: `date -u +"%a, %d %b %Y %H:%M:%S GMT"`'
	/usr/local/bin/s3cmd put wheel.svg s3://wheelpackages/wheel.svg  --cf-invalidate \
	--add-header='Cache-Control: max-age=30' \
	--add-header='Date: `date -u +"%a, %d %b %Y %H:%M:%S GMT"`'
	/usr/local/bin/s3cmd put wheel.css s3://wheelpackages/wheel.css  --cf-invalidate \
	--add-header='Cache-Control: max-age=30' \
	--add-header='Date: `date -u +"%a, %d %b %Y %H:%M:%S GMT"`'
