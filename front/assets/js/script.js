Highcharts.chart('container', {

  title: {
    text: 'Nombre total de transactions par année de 2008 a 2020'
  },



  yAxis: {
    title: {
      text: 'Nombre de transactions'
    }
  },

  xAxis: {
    accessibility: {
      rangeDescription: 'Range: 2008 to 2020'
    }
  },

  legend: {
    layout: 'vertical',
    align: 'right',
    verticalAlign: 'middle'
  },

  plotOptions: {
    series: {
      label: {
        connectorAllowed: false
      },
      pointStart: 2008
    }
  },

  series: [{
    name: 'Nombre de<br>transactions',
    data: [44692, 39394, 42019, 44734, 43710, 38774, 36249, 34348, 34693, 31983, 31355, 30326, 16629]
  }
        ],

  responsive: {
    rules: [{
      condition: {
        maxWidth: 500
      },
      chartOptions: {
        legend: {
          layout: 'horizontal',
          align: 'center',
          verticalAlign: 'bottom'
        }
      }
    }]
  }

});















///////////// Highchat 2 celui pour la somme total des transactions par années //////////////////////////////





Highcharts.chart('container2', {

  title: {
    text: "Montant total des transactions en milliards d'euros par année de 2008 a 2020"
  },



  yAxis: {
    title: {
      text: 'Euros en milliards'
    }
  },

  xAxis: {
    accessibility: {
      rangeDescription: 'Range: 2008 to 2020'
    }
  },

  legend: {
    layout: 'vertical',
    align: 'right',
    verticalAlign: 'middle'
  },

  plotOptions: {
    series: {
      label: {
        connectorAllowed: false
      },
      pointStart: 2008
    }
  },

  series: [{
    name: 'Montant des<br>transactions',
    data: [9.832, 9.696, 12.932, 11.246, 18.337, 11.533, 7.475, 12.695, 10.919, 10.008, 11.631, 7.561, 5.134]
  }
        ],

  responsive: {
    rules: [{
      condition: {
        maxWidth: 500
      },
      chartOptions: {
        legend: {
          layout: 'horizontal',
          align: 'center',
          verticalAlign: 'bottom'
        }
      }
    }]
  }

});