# MSDN Migration Tools

A collection of Python methods to migrate App Service MSDN blog content to GitHub Pages.

Applies the following fixes:
- Prepend the YYYY-MM-DD to file names
- Edit the file paths for all images and JS
- Remove CSS, as Jekyll applies its own
- Remove the \<h1> title tag, as Jekyll adds that for us

## Usage

You must activate the virtual environment and import the dependencies in `requirements.txt`.

Powershell:
```
cd blog-migration-scripts
.\venv\Scripts\activate
pip3 install -r requirements.txt
```

Finally, run the main command to edit the MSDN HTML files:

```
python main.py <input dir> <output dir>
```

Where `input dir` is the directory with the MSDN blogs and `output dir` is where you would like the edited files to be saved. This tool does **not** edit the files in the input directory.