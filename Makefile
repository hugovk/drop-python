help:
	@echo "make help     -- print this help"
	@echo "make generate -- regenerate the files"
	@echo "make deploy   -- deploy the json and index.html to GitHub Pages"

generate:
	rm -rf build
	mkdir build
	python generate.py --version 2.6
	python generate.py --version 3.2
	python generate.py --version 3.3
	cp -R 2.6 build/
	cp -R 3.2 build/
	cp -R 3.3 build/
	cp index.html build/
	cp wheel.css build/

deploy:
	# Adapted from https://zellwk.com/blog/deploy-static-site/

	# Stashes everything away in case you didn't commit them
	git stash save

	# The build script
	make generate

	# Gets commit hash as message
	REV=`git rev-parse HEAD`

	# Switch branches
	git checkout gh-pages

	# Copy build files to root
	cp -R build/ . && rm -rf build

	# Add newly-generated files
	git add .

	# Commit!
	git commit -m "Deploy $REV"

	# Push!
	git push origin gh-pages

	 # Switch back
	git checkout -

	# Applies previously saved stash so you can continue working on changes
	# Once applied, removes stash
	git stash pop
