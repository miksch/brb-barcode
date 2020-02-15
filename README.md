# brb-barcode

Interactive Jupyter Notebook for custom barcode creation and logging. Made 
specifically for [Bear River Bottling LLC](https://www.bearriverbottling.com/). 

#### Library Requirements
Installation using Anaconda (Python 3.7 or 3.8) is recommended.
- python-barcode
- pandas 
- numpy
- panel
- param
- pillow
- sqlite3

#### Usage
1. Open create_barcode.ipynb as a Jupyter Notebook.
2. Run the first two cells to create the interactive Panel instance.
3. Change dropdown menus to match what the sauce case(s) contain, and then enter the estimated
amount of cases you have. The "Batch ID" automatically increments based on the previous batch,
but it can also be changed manually.
4. Check to make sure the information is correct by looking at the displayed values on the right
of the Panel instance, then click "Save CIN Batch" to write the CINs to create barcode labels and
update both the database and .csv CIN record. Single barcode labels are stored in the
"label singles" folder, with each folder corresponding to the batch number.
5. The values should update on the right (including the batch number), and another batch can 
be created.
6. If a clean CIN database is needed, make sure your previous data ("data/cin_record.csv" and
"data/cin_record.csv") is backed up in another directory. Then delete the "cin_record.db" file, 
copy the "cin_record_clean.db" into the same directory, rename it as "cin_record.db", then 
restart and run "create_barcode.ipynb" again to load the new database.

#### Updating Database
All ID numbers used in creating the CINs are stored in the database "data/cin_record.db", along
with the CIN record. If more flavors, sizes, cook locations, etc. need to be added, use a 
database browsing software (e.g. https://sqlitebrowser.org/) to edit the various ID and string
representations. 

#### To-Do
- Add pictures to "Usage" section
- Add environment.yml file
- Add label sheets to output
- Write tests