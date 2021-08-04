# PDF merger tool

## Usage

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
.\YYYY-MM-DD project_name prefix (HHMM).pdf | 2021-08-04 project_name prefix(1601).pdf
```

## Install

1. Install Python 3.7.4 or later.
2. Run `pip install -r requirements.txt` if you just installed Python
3. Just run `PDF_merge.py`
4. You should type 'slug' for your folder, so you'll get `PDF_slug.py` script file
5. Run `PDF_slug.py`. First time you should give `project_name`
6. You can type comments for `changelog.txt`
7. You can add `prefix`. Just start your comment with `!` symbol
8. Hit `enter`
9. Delete `PDF_merge.py` if you don't need it any more.

The files in `MyDir` folder should start with numbers.
