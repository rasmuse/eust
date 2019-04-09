inp2 = $(word 2,$^)
inp3 = $(word 3,$^)

.SECONDARY: # to save intermediate results

data/download/tables/%/data.tsv:
	mkdir -p $(@D)
	curl -s "https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?sort=1&file=data%2F$*.tsv.gz" \
	| gunzip -c > $@

data/download/tables/%/sdmx-structure.xml:
	mkdir -p $(@D)
	eust table download_datastructure $* $@

data/download/nuts/ref-nuts-%.zip:
	mkdir -p $(@D)
	curl -s "https://ec.europa.eu/eurostat/cache/GISCO/distribution/v2/nuts/download/ref-nuts-$*.zip" > $@

data/download/nuts/NUTS_%.zip:
	mkdir -p $(@D)
	cd $(@D)
	curl -s "https://ec.europa.eu/eurostat/ramon/documents/nuts/NUTS_$*.zip" > $@

data/nuts/gis/%: data/download/nuts/ref-nuts-%.zip
	mkdir -p $(@D)
	unzip $< -d $@

data/nuts/codes/NUTS_2006.xls: data/download/nuts/NUTS_2006.zip
	mkdir -p $(@D)
	unzip $< -d $(@D)
	touch -c $@

data/nuts/codes/NUTS_2010.xls: data/download/nuts/NUTS_2010.zip
	mkdir -p $(@D)
	unzip $< -d $(@D)
	touch -c $@

data/nuts/codes/NUTS_2013.xls: data/download/nuts/NUTS_2013.zip
	mkdir -p $(@D)
	unzip $< -d $(@D)
	touch -c $@

data/nuts/codes/NUTS_2016.xlsx: data/download/nuts/NUTS_2016.zip
	mkdir -p $(@D)
	unzip $< -d $(@D)
	mv "data/nuts/codes/NUTS 2016.xlsx" $@
	touch -c $@

data/nuts/codes/NUTS_2006.csv: data/nuts/codes/NUTS_2006.xls
	eust nuts to_csv $< $@

data/nuts/codes/NUTS_2010.csv: data/nuts/codes/NUTS_2010.xls
	eust nuts to_csv $< $@

data/nuts/codes/NUTS_2013.csv: data/nuts/codes/NUTS_2013.xls
	eust nuts to_csv $< $@

data/nuts/codes/NUTS_2016.csv: data/nuts/codes/NUTS_2016.xlsx
	eust nuts to_csv $< $@

nuts: data/nuts/codes/NUTS_2016.csv data/nuts/gis/2016-03m.shp data/nuts/gis/2016-10m.shp \
	data/nuts/codes/NUTS_2013.csv data/nuts/gis/2013-03m.shp data/nuts/gis/2013-10m.shp \
	data/nuts/codes/NUTS_2010.csv data/nuts/gis/2010-03m.shp data/nuts/gis/2010-10m.shp \
	data/nuts/codes/NUTS_2006.csv data/nuts/gis/2006-03m.shp data/nuts/gis/2006-10m.shp


data/tables/%.h5: data/download/tables/%/sdmx-structure.xml data/download/tables/%/data.tsv
	mkdir -p $(@D)
	eust table create $^ $@
