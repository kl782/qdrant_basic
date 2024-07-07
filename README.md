## Basic Local Search using Qdrant

If you've got local files you want to search through more intelligently, Qdrant can help you out. This bit of code (in its current form) supports docx. and .pdf files.

# Part 1: Set up
1) Create a folder in Documents, titled "qdrant". (Alternatively, edit the file path in the code before running it).
2) Drag and drop all the .docx and .pdf documents you want to search over into this folder. (If these live in other folders, either pull them out, or add '/[folder_name]' to the file path in the code)

# Part 2: Installations
1) Download Ollama here: https://ollama.com/download
2) Open Terminal
3) Copy and paste this in: `pip3 install -U sentence-transformers qdrant-client pymupdf python-docx tf-keras ollama`

# Part 3: You're ready!!
1) Download the qdrant_basic.py file.
2) What folder is this .py file in now? If it's in Downloads (the default), type into Terminal: `cd Downloads`. If it landed anywhere else, drag it into Downloads first.
3) Type this into the Terminal: `python3 qdrant_basic.py`

You'll see some loading bars for the embedding of all the documents you put in; then, you'll be prompted with: "What are you looking for? "
Type it in, and voila! You should see the file name and page reference for your search.

# Part 4: Customizations
1) If you want to see more results pulled up, look for the part of the code that says: #EDIT THE NUMBER BELOW TO INCREASE THE NUMBER OF SEARCH RESULTS
   **Change limit=1 to limit=n** (n being whatever number you want)
