import pandas as pd
import barcode
from barcode.writer import ImageWriter
import datetime as dt
import numpy as np
import panel as pn
import param
#import matplotlib.pyplot as plt
from PIL import Image, ImageFont, ImageDraw
import math
import sqlite3

#pn.extension()

class Bottle_UI(param.Parameterized):
    '''
    Param class for setting up the interactive panel to create CINs
    '''
    
    #Read in relational db
    conn = sqlite3.connect('data/cin_record.db')
    
    df_query = "SELECT * FROM cin_record"
    bottle_df = pd.read_sql(df_query, con=conn, index_col='record')
    new_bottle_df = bottle_df.drop(bottle_df.index)
    
    def unpack_sql_query(sql_list):
        
        return [i[0] for i in sql_list]
    

    #Batch Parents
    parent_list = unpack_sql_query(conn.execute('SELECT batch_parent_str FROM batch_parent').fetchall())
    batch_parent = param.ObjectSelector(parent_list[0], parent_list,
                                       doc='Batch Parent')
    
    #Flavors
    flavor_dict={}
    for p in parent_list:
        flavor_dict[p] = unpack_sql_query(conn.execute("SELECT flavor_str FROM flavors "
                                                       "WHERE batch_parent_id = "
                                                       "(SELECT batch_parent_id FROM batch_parent "
                                                       "WHERE batch_parent_str=?)", 
                                                       (p,)))
    flavor_list = flavor_dict[parent_list[0]]
    flavor = param.ObjectSelector(flavor_list[0], flavor_list,
                                  doc='Flavors')
    
    #Bottle sizes
    size_list = unpack_sql_query(conn.execute('SELECT bottle_size_str FROM bottle_size'))
    bottle_size = param.ObjectSelector(size_list[0], size_list,
                                      doc='Bottle Size')
    
    #Location
    location_list = unpack_sql_query(conn.execute('SELECT location_str FROM cook_location'))
    location = param.ObjectSelector(location_list[0], location_list,
                                   doc='Cook Location')
    
    #Batch ID and estimated number of cases
    batch_id = param.Integer(int(bottle_df['batch_id'].values[-1])+1,
                             doc='Batch ID')
    num_cases = param.Integer(5,
                              doc='Number of Cases')
        
    @param.depends('batch_parent', watch=True)
    def _update_flavors(self):
        def unpack_sql_query(sql_list):
        
            return [i[0] for i in sql_list]
    
        flavor_list = unpack_sql_query(self.conn.execute("SELECT flavor_str FROM flavors "
                                                       "WHERE batch_parent_id = "
                                                       "(SELECT batch_parent_id FROM batch_parent "
                                                       "WHERE batch_parent_str=?)", 
                                                       (self.batch_parent,)))
        self.param['flavor'].objects = flavor_list
        self.flavor = flavor_list[0]
    
    save_cin = param.Action(lambda self: self.create_barcode_sheets(),
                           label = 'Save CIN Batch')
    
    def create_barcode_sheets(self):
        '''
        Create PDF of printable barcodes based on a list of cin_nums
        
        '''   
        
        # Set up barcode class
        bar_class = barcode.get_barcode_class('code128')
        bar_writer = barcode.writer.ImageWriter()
            
        # Set up each sheet of barcodes
        num_codes = len(self.new_bottle_df.index)
        #num_sheets = math.ceil(num_codes / self.codes_per_sheet)
        
        # Loop through each code and create a barcode
        for i, record in enumerate(self.new_bottle_df.index):
            
            cin_str = self.new_bottle_df['cin_str'][record]
            test_barcode = bar_class(cin_str, writer = bar_writer)
            test_barcode.save(f"label_singles/{cin_str}", options={'write_text':True})
        
        # Write out new values to database and create new set of values
        self.new_bottle_df.to_sql('cin_record', self.conn, if_exists='append', index='record')
        self.new_bottle_df = self.bottle_df.drop(self.bottle_df.index)
        
        # Re-read record list with new values, then write out to .csv file
        self.bottle_df = pd.read_sql(self.df_query, con=self.conn, index_col='record')
        self.bottle_df.to_csv('data/cin_record.csv')
        
        # Increment batch_id
        self.batch_id = int(self.bottle_df['batch_id'].values[-1])+1
        
        return
    
    @param.depends('batch_parent', 'num_cases', 'flavor', 'bottle_size', 'batch_id', watch=True)
    def view(self):
        
        # Read in data and increment record number
        new_bottle_df = self.bottle_df.drop(self.bottle_df.index)
        new_rn = self.bottle_df.index.values[-1] + 1
        new_index = pd.Index(np.arange(new_rn, new_rn+self.num_cases))
        timestamp = dt.datetime.now()
        
        def unpack_sql_query(sql_list):
        
            return [i[0] for i in sql_list]
    
        # Get ID numbers for each selection
        bp_query = "SELECT batch_parent_id FROM batch_parent WHERE batch_parent_str=?"
        bp = unpack_sql_query(self.conn.execute(bp_query, (self.batch_parent,)))[0]
        
        fl_query = "SELECT flavor_id FROM flavors WHERE flavor_str=?"
        fl = unpack_sql_query(self.conn.execute(fl_query, (self.flavor,)))[0]
        
        bs_query = "SELECT bottle_size_id FROM bottle_size WHERE bottle_size_str=?"
        bs = unpack_sql_query(self.conn.execute(bs_query, (self.bottle_size,)))[0]
        
        loc_query = "SELECT location_id FROM cook_location WHERE location_str=?"
        loc = unpack_sql_query(self.conn.execute(loc_query, (self.location,)))[0]
        
        bi = f'{self.batch_id:04}'
        ci = np.array([f'{int(i):03}' for i in np.arange(int(self.num_cases))]) 

        # Create CIN list
        self.cin_str = [f'{bp}{int(fl):02}-{int(bs):02}-{loc}{bi}{j}' for j in ci]
        self.cin_int = [int(cs.replace('-','')) for cs in self.cin_str]
        
        # Write out new dataframe
        new_bottle_df = new_bottle_df.reindex(new_index)
        new_bottle_df['cin_int'] = np.array(self.cin_int)
        new_bottle_df['cin_str'] = np.array(self.cin_str)
        new_bottle_df['timestamp'] = pd.to_datetime(timestamp)
        new_bottle_df['location_id'] = int(loc)
        new_bottle_df['flavor_id'] = int(fl) 
        new_bottle_df['bottle_size_id'] = int(bs)
        new_bottle_df['batch_parent_id'] = int(bp)
        new_bottle_df['batch_id'] = int(self.batch_id) 
        new_bottle_df['case_id'] = np.array([i for i in np.arange(int(self.num_cases))])
        
        self.new_bottle_df = new_bottle_df
        
        df = pn.widgets.DataFrame(self.new_bottle_df, name='df')
        
        return pn.Row(self.param,df)