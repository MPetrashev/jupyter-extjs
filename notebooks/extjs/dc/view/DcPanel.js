Ext.define('dc.view.DcPanel',{
  extend: 'Ext.panel.Panel',
  alias: 'widget.dcpanel',
  requires: ['jupyter.chart.TSChart'],
  items:[{
    xtype: 'tsChart',
    itemId: 'chart',
    command: 'global_spikes',
    height: 450,
    region: 'center'
  }]
});