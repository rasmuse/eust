try:
    import pandasdmx
except ImportError as e:
    message = (
        'The package pandasdmx is needed for this operation. '
        'pip install eust[metadata] or pip install pandasdmx.'
        )
    raise ImportError(message) from e

def download_datastructure(table_name, outfile):
    service = 'ESTAT'
    name = f'DSD_{table_name}'
    r = pandasdmx.Request(service)
    r.datastructure(name).write_source(outfile)

def read_labels(structure_path):
    req = pandasdmx.Request()
    structure = req.get(
        fromfile=structure_path,
        writer='pandasdmx.writer.structure2pd'
        )
    codelist = structure.write()['codelist']

    result = {}

    dims = codelist[codelist['dim_or_attr']=='D'].groupby(level=0)
    for dim, dim_metadata in dims:
        key = f'dimension/{dim}'
        labels = dim_metadata.loc[dim]['name']
        labels.index.name = 'code'
        result[key] = labels

    attrs = codelist[codelist['dim_or_attr']=='A'].groupby(level=0)
    for attr, attr_metadata in attrs:
        key = f'attr/{attr}'
        labels = attr_metadata.loc[attr]['name']
        labels.index.name = 'code'
        result[key] = labels

    return result
