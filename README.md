# Amazon_Prime_Coverage_Canada_2018

Amaozn Prime is a service provided by Amazon for same-day/one-day online shipping in Canada. This service costs around $100/year and Amazon provides special discount for students. Have you ever curious about how far Amazon Prime is extended in Canada?
In this project, I analyzed the Amazon Prime coverage zone in Canada with Python. 

The packages I used:

- Folium
- Geopandas
- Selenium

The flow-chart of the Amazon Prime Same-day/One-day coverage in Canada in 2018 project is the following:

1. Canada ShapeFile (.shp) consisting of Canada zip codes and corresponding geometery polygans/multi-polygans
2. Extracting canada zip codes from the shapefile
3. Check all the zip codes in Amazon Prime website to find eligible zip codes for free Amazon Prime coverage zone
4. Map the eligible zip codes in Python using folium package

Below is the Ontario and Quebuc coverage for free Amazon Prime Same-day/One-day.

![amz_on](https://user-images.githubusercontent.com/16935815/51081882-01720d00-16c9-11e9-9b5a-73f3d89635ad.jpg)

![amz_qc](https://user-images.githubusercontent.com/16935815/51081953-975a6780-16ca-11e9-9b1d-00d61707fe2f.jpg)
