#!/usr/bin/env python
# coding: utf-8

# # Amazon Prime Coverage zone in Canada
# 
# 1. Pulling out the most recent Canada Shape file (.shp) from gov website
# 2. Extract valid zip codes form the shapefile 
# 3. Check all the zip codes into the Amazon Prime website to find out eligible zip codes for Amazon Prime delivery
# 4. Map the eligible zip codes with folium package  

# In[ ]:


import numpy as np
import pandas as pd
#import seaborn as sns
import json
import time as time

import shapefile
from json import dumps

import folium


# ## import shapefile and extract zipcodes

# In[2]:


import geopandas as gpd
import matplotlib.pyplot as mplt


# In[3]:


canada_shp = gpd.read_file('C:/Users/omid/Desktop/Amazon Project/ShapeFile/lfsa000b16a_e.shp')


# In[16]:


df_zipcodes_census = pd.read_excel('ZipCode Canada Amazon Coverage.xlsx')


# In[17]:


df_zipcodes_census.tail()


# In[48]:





# In[47]:


canada_shp.tail()


# In[18]:


canada_shp_coverage = pd.merge(canada_shp, df_zipcodes_census[['Covereage','Zip Code short']], left_on = 'CFSAUID', right_on = 'Zip Code short', how = 'left') 


# In[20]:


canada_shp_coverage.tail()


# In[21]:


df_zipcodes_pop = pd.read_excel('CA_pop.xlsx')


# In[22]:


df_zipcodes_pop.head()


# In[24]:


df_zipcodes_pop[df_zipcodes_pop.loc[:,'Geographic code'] != df_zipcodes_pop.loc[:,'Geographic name']]


# In[26]:


canada_shp_coverage_pop = pd.merge(canada_shp_coverage, df_zipcodes_pop[['Geographic code','Province or territory','Population, 2016']], left_on = 'CFSAUID', right_on = 'Geographic code', how = 'left') 


# In[34]:


canada_shp_coverage_pop.dtypes


# In[33]:


canada_shp_coverage_pop = canada_shp_coverage_pop.set_geometry('geometry')


# In[35]:


canada_shp_coverage_pop.to_file('canada_shp_coverage_pop.shp')


# In[9]:


canada_shp.crs


# In[6]:


canada_shp = canada_shp.to_crs({'init' :'epsg:4326'})


# In[8]:


canada_shp = canada_shp.set_geometry('geometry')


# In[11]:


canada_shp.plot(
mplt.gcf().set_size_inches( 10, 10)


# In[36]:


canada_shp.to_file('canada.shp')


# In[38]:


# read the shapefile
reader = shapefile.Reader ("canada_shp_coverage_pop.shp", encoding='latin-1')

## Convert shapefile to json
fields = reader.fields[1:]
field_names = [field[0] for field in fields]
buffer = []
for sr in reader.shapeRecords():
    atr = dict(zip(field_names, sr.record))
    geom = sr.shape.__geo_interface__
    buffer.append(dict(type="Feature",     geometry=geom, properties=atr)) 

# write the GeoJSON file
geojson = open("canada_shp_coverage_pop.json", "w")
geojson.write(dumps({"type": "FeatureCollection", "features": buffer}, indent=2) + "\n")
geojson.close()


# In[41]:


## Load GEOJSON
with open ('canada_shp_coverage_pop.json', 'r') as jsonFile:
    data = json.load(jsonFile)
tmp = data


# In[47]:


## Extracting All the Canada ZipCodes

## Load GEOJSON
with open ('Canada_zipcodes.json', 'r') as jsonFile:
    data = json.load(jsonFile)
tmp = data

zipcodes_census = []
for i in range(len(tmp['features'])):
    zipcodes_census.append(tmp['features'][i]['properties']['CFSAUID'])    


# In[ ]:





# In[64]:


## Creatubg 6 digit ZipCodes for Amazon

zipcodes_census_6digit = []
for i in range(len(zipcodes_census)):
    zipcodes_census_6digit.append(zipcodes_census[i]+' 1G7')


# In[ ]:





# In[66]:


df_zipcodes_census = pd.DataFrame({'ZipCode':zipcodes_census_6digit})


# In[ ]:





# ### Now put data

# In[156]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")

browser = webdriver.Chrome(executable_path = r'C:/Users/omid/Desktop/Amazon Project/chromedriver_win32/chromedriver.exe',
                           options = chrome_options)


# In[148]:





# In[157]:


df_zipcodes_census['No Covereage'] = 0
df_zipcodes_census['Covereage'] = 0


# In[158]:


browser.get('https://www.amazon.ca/b?ie=UTF8&node=9863204011')

## Find the location of the search bar
searchbar = browser.find_element_by_id('free_same_day_zip_checker_input')


# In[159]:


for i in range (0, df_zipcodes_census.shape[0]):
    if i % 50 == 0:
        print(i , 'zip code completed and' , df_zipcodes_census.shape[0]-i,' zip code remains.')
    if i % 100 == 0:
        df_zipcodes_census.to_excel('C:/Users/omid/Desktop/Amazon Project/ZipCode Canada Amazon Coverage.xlsx',sheet_name = 'sheet1',index = False)
        #writer = pd.ExcelWriter('output.xlsx')
    ## Search for ZipCode
    searchbar.send_keys(df_zipcodes_census.loc[i,'ZipCode'])

    ## Enter the zipcode and begin the search
    searchbar.send_keys(Keys.ENTER)

    time.sleep(0.9)

    ## Capturing the result
    result = browser.find_element_by_id('free_same_day_zip_checker_message_2')

    if result.text.find('Prime Free Same-Day or Free One-Day Delivery is available for residential addresses in') != -1:
        df_zipcodes_census.loc[i, 'Covereage'] = 1
    elif result.text.find('is not within the Prime Free Same-Day or Free One-Day Delivery areas.') != -1:
        df_zipcodes_census.loc[i, 'No Covereage'] = 1  
    
    ## Find the location of the search bar and Clear text from text area 
    browser.find_element_by_id('free_same_day_zip_checker_input').clear()


# In[ ]:





# ### Map the result

# In[128]:


df_zipcodes_census['Zip Code short'] = zipcodes_census


# In[129]:


df_zipcodes_census.head()


# In[ ]:





# ### Finding Lat and Lng for ZipCodes

# In[3]:


df_zipcodes_census = pd.read_excel('ZipCode Canada Amazon Coverage.xlsx')


# In[4]:


df_zipcodes_census.head()


# In[30]:


df_zipcodes_lat_lng = pd.read_excel('ca_postal_codes2.xlsx')


# In[31]:


df_zipcodes_lat_lng = df_zipcodes_lat_lng.loc[:,['Postal Code','Province','Latitude','Longitude']]


# In[32]:


df_zipcodes_lat_lng.head()


# In[33]:


df_zipcodes_total = pd.merge(df_zipcodes_census, df_zipcodes_lat_lng, left_on = 'Zip Code short', right_on = 'Postal Code', how = 'inner')


# In[34]:


df_zipcodes_total.tail()


# In[41]:


df_zipcodes_total.to_excel('C:/Users/omid/Desktop/Amazon Project/Amazon Colab.xlsx',sheet_name = 'sheet1',index = False)


# In[35]:


df_zipcodes_total.dtypes


# In[40]:


set(df_zipcodes_total.loc[:,'Covereage'].tolist())


# In[ ]:


folium.


# ### Mapping the coordinates

# In[42]:


m = folium.Map(location = [43.653963, -79.387207], zoom_start = 4)

for i in range(df_zipcodes_total.shape[0]):
    if df_zipcodes_total.loc[i,'Covereage'] == 1:
        folium.Circle([df_zipcodes_total.loc[i,'Latitude'],df_zipcodes_total.loc[i,'Longitude']], color = 'Red', radius = 100,
                      fill = True, popup = df_zipcodes_total.loc[i,'Postal Code']+', '+df_zipcodes_total.loc[i,'Province']).add_to(m)

display(m)


# ### Extracting Ontario

# In[43]:


df_zipcodes_census_map=pd.DataFrame(columns = df_zipcodes_census.columns)
for i in range(df_zipcodes_census.shape[0]):
    if df_zipcodes_census.loc[i,'Zip Code short'][0] in ['K','L','M','N']:
        df_zipcodes_census_map = df_zipcodes_census_map.append(df_zipcodes_census.loc[i,:],ignore_index = True, sort = False)


# In[44]:


df_zipcodes_census_map.tail()


# In[ ]:


geozips = []
for i in range(len(tmp['features'])):
    if tmp['features'][i]['properties']['CFSAUID'] in df_zipcodes_census_map['Zip Code short'].tolist():
        geozips.append(tmp['features'][i])


# In[ ]:





# In[49]:


df_zipcodes_census_map.loc[:,'Covereage'] = df_zipcodes_census_map.loc[:,'Covereage'].astype(float)


# In[ ]:





# In[ ]:





# In[46]:


df_zipcodes_census.dtypes


# In[43]:


tmp['features'][0]


# In[45]:


la_geo = r'canada_shp_coverage_pop.json'

m = folium.Map(location = [43.653963, -79.387207], zoom_start = 4, tiles = 'OpenStreetMap')

m.choropleth(
    geo_data = la_geo,
    fill_opacity = 0.4,
    line_opacity = 0.1,
    data = df_zipcodes_census,
    key_on = 'feature.properties.CFSAUID',
    columns = ['Zip Code short','Covereage'],
    fill_color = 'YlOrRd')
folium.LayerControl().add_to(m)

m.save(outfile = 'Amazon_covereage.html')


# ## Creating Map for each province

# In[ ]:





# In[ ]:





# In[95]:


canada_shp_coverage_pop_bc = canada_shp_coverage_pop[canada_shp_coverage_pop['PRNAME'] == 'British Columbia / Colombie-Britannique']


# In[96]:


canada_shp_coverage_pop_bc.head(2)


# In[97]:


canada_shp_coverage_pop_bc.loc[:,'Population, 2016'].sum()


# In[98]:


canada_shp_coverage_pop_bc[canada_shp_coverage_pop_bc['Covereage']==1].loc[:,'Population, 2016'].sum()


# In[ ]:





# In[ ]:





# In[80]:


print(canada_shp_coverage_pop_QC.shape)

print(set(canada_shp_coverage_pop_QC['Province or territory'].tolist()))

canada_shp_coverage_pop_QC = canada_shp_coverage_pop_QC.to_crs({'init' :'epsg:4326'})

canada_shp_coverage_pop_QC = canada_shp_coverage_pop_QC.set_geometry('geometry')

#canada_shp_coverage_pop_ON.plot()
#mplt.gcf().set_size_inches( 10, 10)

canada_shp_coverage_pop_QC.to_file('canada_QC.shp')

# read the shapefile
reader = shapefile.Reader ("canada_QC.shp", encoding='latin-1')

## Convert shapefile to json
fields = reader.fields[1:]
field_names = [field[0] for field in fields]
buffer = []
for sr in reader.shapeRecords():
    atr = dict(zip(field_names, sr.record))
    geom = sr.shape.__geo_interface__
    buffer.append(dict(type="Feature",     geometry=geom, properties=atr)) 

# write the GeoJSON file
geojson = open("canada_QC.json", "w")
geojson.write(dumps({"type": "FeatureCollection", "features": buffer}, indent=2) + "\n")
geojson.close()

la_geo = r'canada_QC.json'

m = folium.Map(location = [45.516136, -73.656830], zoom_start = 5, tiles = 'OpenStreetMap')

m.choropleth(
    geo_data = la_geo,
    fill_opacity = 0.4,
    line_opacity = 0.15,
    data = df_zipcodes_census,
    key_on = 'feature.properties.CFSAUID',
    columns = ['Zip Code short','Covereage'],
    fill_color = 'YlOrRd')
folium.LayerControl().add_to(m)

m.save(outfile = 'Amazon_covereage_QC.html')


# In[ ]:





# In[64]:


set(canada_shp['PRNAME'].tolist())


# In[ ]:


canada_shp_coverage_pop_bc= canada_shp_coverage_pop[canada_shp_coverage_pop['PRNAME'] == 'British Columbia / Colombie-Britannique']


# In[69]:


canada_shp_coverage_pop_bc.shape


# In[70]:


set(canada_shp_coverage_pop_bc['Province or territory'].tolist())


# In[53]:


canada_shp_coverage_pop_alberta = canada_shp_coverage_pop_alberta.to_crs({'init' :'epsg:4326'})


# In[54]:


canada_shp_coverage_pop_alberta = canada_shp_coverage_pop_alberta.set_geometry('geometry')


# In[56]:


canada_shp_coverage_pop_alberta.plot()
mplt.gcf().set_size_inches( 10, 10)


# In[57]:


canada_shp_coverage_pop_alberta.to_file('canada_Alberta.shp')


# In[58]:


# read the shapefile
reader = shapefile.Reader ("canada_Alberta.shp", encoding='latin-1')

## Convert shapefile to json
fields = reader.fields[1:]
field_names = [field[0] for field in fields]
buffer = []
for sr in reader.shapeRecords():
    atr = dict(zip(field_names, sr.record))
    geom = sr.shape.__geo_interface__
    buffer.append(dict(type="Feature",     geometry=geom, properties=atr)) 

# write the GeoJSON file
geojson = open("canada_Alberta.json", "w")
geojson.write(dumps({"type": "FeatureCollection", "features": buffer}, indent=2) + "\n")
geojson.close()


# In[63]:


la_geo = r'canada_Alberta.json'

m = folium.Map(location = [56.90, -115.00], zoom_start = 5, tiles = 'OpenStreetMap')

m.choropleth(
    geo_data = la_geo,
    fill_opacity = 0.4,
    line_opacity = 0.15,
    data = df_zipcodes_census,
    key_on = 'feature.properties.CFSAUID',
    columns = ['Zip Code short','Covereage'],
    fill_color = 'YlOrRd')
folium.LayerControl().add_to(m)

m.save(outfile = 'Amazon_covereage_Alberta.html')


# In[49]:


canada_shp_coverage_pop.head()


# In[ ]:




