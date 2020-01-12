'''
.py file used as a psuedo database in the main program 

NOTE: flavors are strings to make str concats easier
'''

#Dr. S flavors
dr_s_flavors = {
	'Habanero Wonder Tonic' : '55',
	'Sweet Jalepeno Grassfire' : '83',
	'Tropical Citrus Surprise' : '54',
	'Sweet and Spicy Ginger Thai' : '76',
	'Peach Habanero' : '05',
	'Lightning Hot Buffalo' : '19'
}

#Mr. Q flavors
mr_q_flavors = {
	'Four Hoursemen Honey BBQ' : '77',
	'Black Mountain Meat Sauce' : '29',
	'Carolina Hog Sweat' : '62',
	'Memphis Fry Sauce' : '75'
}

#Bottle type ids
bottle_ids = {
	'5oz woozy' : '18',
	'8oz woozy' : '72',
	'12oz round' : '41'
}

#Batch parent ids
parent_ids = {
	'dr_s' : '5',
	'mr_q' : '7'
}

parent_flavors = {
	'dr_s' : dr_s_flavors,
	'mr_q' : mr_q_flavors
}

#Cook location id (add more if cooking in another location)
cook_location = {
	'BATC' : '1'
}