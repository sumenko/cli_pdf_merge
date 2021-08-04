# PDF merger tool

Sometimes you have folder with many .PDF files

```
.\
MyDir\
	1 - file.pdf
	2 - file.pdf
	... file.pdf
	project.txt
	changelog.txt
```

You run `PDF_MyDir.py` tool and get single file

```
.\YYYY-MM-DD project_name prefix (HHMM).pdf
```

# Install

Just run PDF_merge.py
1. You should type 'slug' for your folder, so you'll get `PDF_slug.py` script file
2. Run `PDF_slug.py`. First time you should give `project_name`
3. You can type comments for `changelog.txt`
4. You can add `prefix`. Just start your comment with `!` symbol
5. Hit `enter`

The files in `MyDir` folder should start with numbers.
