from IPython.display import display,Javascript
import numpy as np

def control(app,stores=None,viewClass=None, controllers=None, config=None):
  if viewClass is None:
    capitalizedApp = app.capitalize()
    viewClass = '{}.view.{}Panel'.format(app,capitalizedApp)
    controllers = "controllers: '{}PanelController',".format(capitalizedApp)

  code = '''var out = Jupyter.notebook.get_selected_cell().output_area.element[0];
    Ext.application({{
      name: '{}',
      paths: {{
        'jupyter' : '/files/extjs/jupyter',
        'Ext' : '/files/extjs/Ext',
        '{}' : '/files/extjs/{}'
      }},
      {}
      {}
      launch: function () {{
        Ext.create('{}',{{
          width: '100%',
          height: 500,
          {}
          renderTo: out
        }});
      }}
    }});'''.format(app,app,app
                   ,'stores:'+ stores + ',' if stores is not None else ''
                   ,controllers if controllers is not None else ''
                   , viewClass
                   , str(config).strip('{}') + ',' if config is not None else '')
  return Javascript(code
    # ,lib=['https://cdnjs.cloudflare.com/ajax/libs/extjs/6.2.0/ext-all-debug.js'
    #       ,'https://cdnjs.cloudflare.com/ajax/libs/extjs/6.2.0/packages/charts/classic/charts-debug.js']
    ,css=[
      'https://cdnjs.cloudflare.com/ajax/libs/extjs/6.2.0/packages/charts/classic/crisp/resources/charts-all-debug.css',
      'https://cdnjs.cloudflare.com/ajax/libs/extjs/6.2.0/classic/theme-crisp/resources/theme-crisp-all_1.css',
      'https://cdnjs.cloudflare.com/ajax/libs/extjs/6.2.0/classic/theme-crisp/resources/theme-crisp-all_2.css'
    ])

def to_message(df):
  def type(dtype):
    return 'number' if dtype == 'float64' else 'date' if issubclass(dtype.type, np.datetime64) else 'string'

  def field(name):
    return {'name': name, 'type': type(df.dtypes[name])}

  def column(name,dtype,header=None):
    retVal = {'dataIndex': name, 'header': name if header is None else header, 'flex': 1}
    if dtype == 'float64':
      retVal.update({
        'xtype' : 'numbercolumn',
        'format': '0,000.00',
        'align':'right'
      })
    return retVal

  metaData = {
    'colModel': [column('id',df.index.dtype,df.index.name)] + [column(c,df.dtypes[c]) for c in df.columns]
  }
  if not 'Capital' in df.columns:
    metaData['fields'] = [field(c) for c in df.columns] + [{'name': 'id', 'type': type(df.index.dtype)}]

  return {
    'rows': df.to_csv(index_label='id'),
    'metaData': metaData
  }