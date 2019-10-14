
var url_year_oa = "https://data.enseignementsup-recherche.gouv.fr/api/records/1.0/search/?dataset=open-access-monitor-france&rows=0&facet=oa_host_type_year&apikey=8b8d1b13d9551d9d68ea99f20682806c31b2adce9a10795ca73e6980"
var url_year_oa_field = "https://data.enseignementsup-recherche.gouv.fr/api/records/1.0/search/?dataset=open-access-monitor-france&facet=oa_host_type_year_scientific_field&apikey=8b8d1b13d9551d9d68ea99f20682806c31b2adce9a10795ca73e6980&refine.scientific_field="
var url_oa_genre = "https://data.enseignementsup-recherche.gouv.fr/api/records/1.0/search/?dataset=open-access-monitor-france&facet=oa_host_type_genre&apikey=8b8d1b13d9551d9d68ea99f20682806c31b2adce9a10795ca73e6980&refine.year=2017"
var url_oa_publisher = "https://data.enseignementsup-recherche.gouv.fr/api/records/1.0/search/?dataset=open-access-monitor-france&facet=oa_host_type_publisher&apikey=8b8d1b13d9551d9d68ea99f20682806c31b2adce9a10795ca73e6980&refine.publisher=Elsevier BV&refine.publisher=Springer Nature&refine.publisher=Wiley-Blackwell&refine.publisher=OpenEdition&refine.publisher=Springer International Publishing&refine.publisher=Informa UK Limited&refine.publisher=CAIRN&refine.publisher=EDP Sciences&refine.publisher=American Chemical Society (ACS)&refine.publisher=IOP Publishing&refine.publisher=IEEE&disjunctive.publisher=true&refine.year=2017"
var url_oa_field = "https://data.enseignementsup-recherche.gouv.fr/api/records/1.0/search/?dataset=open-access-monitor-france&facet=oa_host_type_scientific_field&apikey=8b8d1b13d9551d9d68ea99f20682806c31b2adce9a10795ca73e6980&refine.year=2017"

var color_repository = '#61cdbb';
var color_publisher = '#f1e15b';
var color_unknown = '#205A7D';
var color_closed = 'grey';
var color_oa = '#3288BD';

var graph_year = null;
var graph_genre = null;
var graph_publisher = null;
var graph_field = null;
var graph_sunburst = null;

var graph_height_1 = '500 px';
var graph_height_2 = '670 px';


/*
$('#scientific_field_selection').change(function() {
	refresh_data_year()
});
$('#year_selection_genre').change(function() {
	refresh_data_genre()
});
$('#year_selection_field').change(function() {
	refresh_data_field()
});
$('#year_selection_publisher').change(function() {
	refresh_data_publisher()
});
*/

function export_file(chart_name, filetype){
	if (filetype === 'csv') {
		chart_name.downloadCSV();
	}
	else if (filetype === 'xls') {
		chart_name.downloadXLS();
	}
	else {
		chart_name.exportChart({
		type: filetype,
    		});
	}
}

function refresh_data_year(lang) {
        url_to_use = url_year_oa
	/*
	if ($('#scientific_field_selection').val() === 'all') {
                url_to_use = url_year_oa
        }
        else {
                url_to_use = url_year_oa_field+$('#scientific_field_selection').val()
        }*/
  $.ajax({ url: url_to_use,
        success: function(data){
		draw_graph_year(data, lang)
	}
  });
}

function refresh_data_sunburst(lang) {
        url_to_use = url_year_oa
  $.ajax({ url: url_to_use,
        success: function(data){
		draw_sunburst_year(data, lang)
	}
  });
}

function refresh_data_genre(lang) {
  url_to_use = url_oa_genre // + $('#year_selection_genre').val()
  $.ajax({ url: url_to_use,
        success: function(data){
		draw_graph_genre(data, lang)
	}
  });
}
function refresh_data_publisher(lang) {
//  url_to_use = url_oa_publisher + $('#year_selection_publisher').val()
  url_to_use = url_oa_publisher
  $.ajax({ url: url_to_use,
        success: function(data){
		draw_graph_publisher(data, lang)
	}
  });
}
function refresh_data_field(lang) {
//  url_to_use = url_oa_field + $('#year_selection_field').val()
  url_to_use = url_oa_field
  $.ajax({ url: url_to_use,
        success: function(data){
		draw_graph_field(data, lang)
	}
  });
}


function format_data(data, facet_name, add_count = true){
  var k = 0;
  for (i = 0; i < data['facet_groups'].length; i++) { 
       if (data['facet_groups'][i]['name'] === facet_name) {k = i}
  }

  var response = data['facet_groups'][k]['facets']
  var count_oa_label_host = {}
  var labels = []
  var labels_with_count = []
  var oa_repository = []
  var oa_publisher = []
  var oa_unknown = []
  var closed = []
  var oa_all = []
  for (i = 0; i < response.length; i++) {
    label_split = response[i]["name"].split("|")
    oa_type = label_split[0]
    label = label_split[1]
    if (label === "unknown") {
	    continue
    }
    oa_type_count = response[i]["count"]
    if (!(label in count_oa_label_host)) {
      labels.push(label)
      count_oa_label_host[label] = {}
    }
    count_oa_label_host[label][oa_type] = oa_type_count
  }
  labels = labels.sort()
  nb_total_label = {}
  
  for (i in labels){
    label = labels[i]
    nb_repository = count_oa_label_host[label]['repository']
    nb_publisher = count_oa_label_host[label]['publisher']
    nb_unknown = count_oa_label_host[label]['unknown']
    nb_closed = count_oa_label_host[label]['closed access']
    nb_oa = nb_repository + nb_publisher + nb_unknown
    nb_total = nb_repository + nb_publisher + nb_unknown + nb_closed
    count_oa_label_host[label]['total'] = nb_total
    nb_total_label[label] = nb_total
    if (add_count) {
	    labels_with_count.push(label + "<br/>(" + nb_total +" publications)")
    } else {
	    labels_with_count.push(label)
    }
    oa_repository.push({'y': nb_repository/nb_total * 100, 'y_abs':nb_repository, 'y_tot':nb_total})
    oa_publisher.push({'y': nb_publisher/nb_total * 100, 'y_abs':nb_publisher, 'y_tot':nb_total})
    oa_unknown.push({'y': nb_unknown/nb_total * 100, 'y_abs':nb_unknown, 'y_tot':nb_total})
    closed.push({'y': nb_closed/nb_total * 100, 'y_abs':nb_closed, 'y_tot':nb_total})
    oa_all.push({'y': nb_oa/nb_total * 100, 'y_abs':nb_oa, 'y_tot':nb_total})
  }
  return {'labels': labels_with_count, 'oa_repository':oa_repository, 'oa_publisher':oa_publisher, 'oa_unknown': oa_unknown, 'oa': oa_all, 'closed': closed}
  }

function draw_graph_genre(data, lang) {
    data_formatted = format_data(data, "oa_host_type_genre", add_count = false)
    console.log(data_formatted)
    labels = data_formatted['labels']
    oa_repository = data_formatted['oa_repository']
    oa_publisher = data_formatted['oa_publisher']
    oa_unknown = data_formatted['oa_unknown']
    closed_access = data_formatted['closed']
   graph_genre = hc_treemap('container_genre', labels, oa_repository, oa_publisher, oa_unknown, closed_access, translation['title_graph_genre'][lang], lang, graph_height_1)
}
function draw_graph_field(data, lang) {
    data_formatted = format_data(data, "oa_host_type_year_scientific_field")
    labels = data_formatted['labels']
    oa_repository = data_formatted['oa_repository']
    oa_publisher = data_formatted['oa_publisher']
    oa_unknown = data_formatted['oa_unknown']
   graph_field = hc('container_field', labels, oa_unknown, oa_publisher, oa_repository, translation['title_graph_field'][lang], "bar", lang, graph_height_2)
}
function draw_graph_publisher(data, lang) {
    data_formatted = format_data(data, "oa_host_type_publisher")
    labels = data_formatted['labels']
    oa_repository = data_formatted['oa_repository']
    oa_publisher = data_formatted['oa_publisher']
    oa_unknown = data_formatted['oa_unknown']
   graph_publisher = hc('container_publisher', labels, oa_unknown, oa_publisher, oa_repository,  translation['title_graph_publisher'][lang], "bar", lang, graph_height_2, annotations=[], caption = translation['publisher-caption'][lang], margin_bottom = 120)
}

function draw_graph_year(data, lang) {

 // var scientific_field_title = "(" + $('#scientific_field_selection :selected').text() + ")"
 // var scientific_field_title = ""
 // if ($('#scientific_field_selection').val() === 'all') {scientific_field_title = '(toutes disciplines)'}
    data_formatted = format_data(data, "oa_host_type_year")
    labels = data_formatted['labels']
    oa_repository = data_formatted['oa_repository']
    oa_publisher = data_formatted['oa_publisher']
    oa_unknown = data_formatted['oa_unknown']

 annotations = [
	 {
        labels: [{
            point: {
                xAxis: 0,
                yAxis: 0,
                x: 4,
                y: 45
            },
            text: translation['last_year_oa'][lang]
        }]
    }, {
        labelOptions: {
            shape: 'connector',
            align: 'right',
            justify: false,
            crop: true,
            style: {
                fontSize: '0.8em',
                textOutline: '1px white'
            }
        },
    }]


   graph_year = hc('container_year', labels, oa_unknown, oa_publisher, oa_repository, translation['title_graph_year'][lang], "column", lang, graph_height_1, annotations, caption="",margin_bottom = 150)
}


function draw_sunburst_year(data, lang){

    data_formatted = format_data(data)
    year_index = 4
    year = data_formatted['labels'][year_index]
    oa_repository = data_formatted['oa_repository'][year_index]
    oa_publisher = data_formatted['oa_publisher'][year_index]
    oa_unknown = data_formatted['oa_unknown'][year_index]
    closed_access = data_formatted['closed'][year_index]
    oa_all = data_formatted['oa'][year_index]
    graph_sunburst = hc_sunburst('container_sunburst', year, oa_repository, oa_publisher, oa_unknown, oa_all, closed_access, translation['title_graph_sunburst'][lang], lang)
}


function hc_treemap(container_name, labels, oa_repository, oa_publisher, oa_unknown, closed_access, current_title, lang, graph_height){
var data = [
{
    id: 'closed',
    name: translation['closed-access'][lang],
    color: color_closed
//}, {
//    id: 'oa',
//    name: translation['open-access'][lang],
//    color: color_oa
}, {
    id: 'publisher',
    name: translation['host-publisher'][lang],
    color: color_publisher,
//    parent: 'oa'
}, {
    id: 'repository',
    name: translation['host-archive'][lang],
    color: color_repository,
//    parent: 'oa'
}, {
    id: 'unknown',
    name: translation['host-unknown'][lang],
    color: color_unknown,
//    parent: 'oa'
}
];

  for (i = 0; i < labels.length; i++) { 
	  data.push({
		  name: translation[labels[i]][lang],
		  access_type: translation['closed-access'][lang],
		  parent: 'closed',
		  value: closed_access[i]['y_abs']});
	  data.push({
		  name: translation[labels[i]][lang],
		  parent: 'repository',
		  access_type: translation['open-access'][lang] + ' ( ' + translation['host-archive'][lang] + ' )',
		  value: oa_repository[i]['y_abs']});
	  data.push({
		  name: translation[labels[i]][lang],
		  parent: 'publisher',
		  access_type: translation['open-access'][lang] + ' ( ' + translation['host-publisher'][lang] + ' )',
		  value: oa_publisher[i]['y_abs']});
	  data.push({
		  name: translation[labels[i]][lang],
		  parent: 'unknown',
		  access_type: translation['open-access'][lang] + ' ( ' + translation['host-unknown'][lang] + ' )',
		  value: oa_unknown[i]['y_abs']});
}

current_chart = Highcharts.chart(container_name, {

    chart: {
        height: graph_height
    },

    title: {
        text: current_title
    },
    subtitle: {
            text: translation['subtitle_graph'][lang]
    },
    credits: {
            enabled: false
    },
    series: [{
        type: "treemap",
	    layoutAlgorithm: 'stripes',
        alternateStartingDirection: true,
        levels: [{
            level: 1,
            layoutAlgorithm: 'sliceAndDice',
            dataLabels: {
                enabled: true,
                align: 'left',
                verticalAlign: 'top',
                style: {
                    fontSize: '15px',
                    fontWeight: 'bold'
                }
            }
        }],
        data: data,
        cursor: 'pointer'
    }],
    tooltip: {
        headerFormat: '',
        pointFormat: "<b> {point.value}</b> {point.name} <br/> {point.access_type} ",
	    formatter: function (tooltip) {
            if (this.point.noTooltip) {
                return false;
            }
            // If not null, use the default formatter
            return tooltip.defaultFormatter.call(this, tooltip);
        }
    }
    });
return current_chart;
}


function hc_sunburst(container_name, year, oa_repository, oa_publisher, oa_unknown, oa_all, closed_access, current_title, lang){
var data = [
{
    id: '0.0',
    parent: '',
    noTooltip: true,
    borderColor: 'white', 
    name: year,
    value: 100,
    total: closed_access['y_tot'],
    abs_value: closed_access['y_tot']
}, {
    id: '1.1',
    parent: '0.0',
    name: translation['host-publisher'][lang],
    color: color_publisher,
    value: oa_publisher['y'],
    abs_value: oa_publisher['y_abs'],
    total: oa_publisher['y_tot']
}, {
    id: '1.2',
    parent: '0.0',
    name: translation['host-archive'][lang],
    color: color_repository,
    value: oa_repository['y'],
    abs_value: oa_repository['y_abs'],
    total: oa_repository['y_tot']
}, {
    id: '1.3',
    parent: '0.0',
    name: translation['host-unknown'][lang],
    color: color_unknown,
    value: oa_unknown['y'],
    abs_value: oa_unknown['y_abs'],
    total: oa_unknown['y_tot']
}, {
    id: '2.1',
    parent: '1.1',
    color: color_oa,
    borderColor: color_oa,
    dataLabels: {align: 'left'},
    name: translation['open-access'][lang],
    value: oa_all['y'],
    abs_value: oa_all['y_abs'],
    total: oa_all['y_tot']
}, {
    id: '2.2',
    parent: '1.2',
    color: color_oa,
    borderColor: color_oa,
    dataLabels: {enabled: false},
    name: translation['open-access'][lang],
    value: oa_all['y'],
    abs_value: oa_all['y_abs'],
    total: oa_all['y_tot']
}, {
    id: '2.3',
    parent: '1.3',
    color: color_oa,
    borderColor: color_oa,
    dataLabels: {enabled: false},
    name: translation['open-access'][lang],
    value: oa_all['y'],
    abs_value: oa_all['y_abs'],
    total: oa_all['y_tot']
}, {
    id: '1.0',
    parent: '0.0',
    name: '0-Accès fermé',
    noTooltip: true,
    borderColor: 'white',
    value: closed_access['y'],
    abs_value: closed_access['y_abs'],
    total: closed_access['y_tot']
}, {
    id: '2.0',
    parent: '1.0',
    name: 'Accès fermé',
    name: translation['closed-access'][lang],
    value: closed_access['y'],
    abs_value: closed_access['y_abs'],
    total: closed_access['y_tot'],
    color:color_closed
}];

Highcharts.getOptions().colors.splice(0, 0, '#f8f9fa');

current_chart = Highcharts.chart(container_name, {

    chart: {
        height: graph_height_1
    },

    title: {
        text: current_title
    },
    subtitle: {
	    text: translation['subtitle_graph'][lang]
    },
    credits: {
	    enabled: false
    },
    series: [{
        type: "sunburst",
        data: data,
        allowDrillToNode: false,
        cursor: 'pointer',
	levels:[{
            level:3,
            levelSize: {
                unit: 'weight',
                value: 1.3
            }
	}],
        dataLabels: {
	    format: '{point.name}<br>{point.value:.0f} %',
            rotationMode: 'auto',
	    filter: {
                property: 'name',
                operator: '>',
                value: '3'
            }
        }
    }],
    tooltip: {
        headerFormat: '',
        pointFormat: "<b>{point.name}</b><br/><b>{point.value:.2f} %</b> " + translation['des-publications'][lang]+" ({point.abs_value:.0f} / {point.total:.0f}  ) ",
	    formatter: function (tooltip) {
            if (this.point.noTooltip) {
                return false;
            }
            // If not null, use the default formatter
            return tooltip.defaultFormatter.call(this, tooltip);
        }
    }
});
return current_chart;
}

function hc(container_name, years, oa_unknown, oa_publisher, oa_repository, current_title, graph_type, lang, graph_height, annotations = [], caption="", margin_bottom = 120) {
	var current_chart = Highcharts.chart(container_name, {
    chart: {
        type: graph_type,
        height: graph_height,
	marginBottom: margin_bottom
    },
    title: {
        text: current_title
    },
    subtitle: {
	    text: translation['subtitle_graph'][lang]
    },
    caption: {
	    text: caption,
	    useHTML: true
    },
    annotations: annotations,
    credits: {
	    enabled: false,
	    text: "Accès à la méthodologie",
	    style: {
		    color: "#33333"
            },
	    href: "https://dataesr.github.io/publications/MonitoringOpenAccessatnationallevelFrenchcase",
	    position: {
               align: 'right',
               verticalAlign: 'bottom',
               x: 0,
               y: 0
        }
    },
    xAxis: {
        categories: years
    },
    yAxis: {
        min: 0,
	max: 100,
	title:'',
        stackLabels: {
            enabled: true,
            formatter: function () {
		    return this.total.toFixed(1) + " %";
            },
            style: {
                fontWeight: 'bold',
                color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'
            }
        },
	labels: {
            formatter: function () {
                var label = this.axis.defaultLabelFormatter.call(this);
                return label+' %';
            }
        }
    },
    legend: {
	    title: {
		    text: translation['hosting'][lang]
	    },
        align: 'left',
	y: 10,
        verticalAlign: 'bottom',
	layout: 'horizontal',
        backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || 'white',
        borderColor: '#CCC',
        borderWidth: 0,
        shadow: false
    },
    tooltip: {
        headerFormat: '<b>{point.x}</b><br/>',
	    pointFormat: "• "+translation['open-access-rate'][lang] +"<br>" +translation['with-host'][lang] + " {series.name}:<br> {point.y:.2f} % ({point.y_abs} / {point.y_tot}) <br/> • " + translation['open-access-rate'][lang]+" :<br> {point.stackTotal:.2f} %"
    },
    plotOptions: {
        column: {
            stacking: 'normal',
            dataLabels: {
                enabled: false,
                formatter: function () {
		    return this.y.toFixed(1) + " %";
                },
                color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white'
            }
        },
        series: {
            stacking: 'normal',
            dataLabels: {
                enabled: false,
                formatter: function () {
		    return this.y.toFixed(1) + " %";
                },
                color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white'
            }
        }
    },
    series: [{
        name: translation['host-unknown'][lang],
        data: oa_unknown,
	color: color_unknown,
	legendIndex: 2
    }, {
        name: translation['host-publisher'][lang],
        data: oa_publisher,
	color: color_publisher,
	legendIndex: 1
    }, {
        name: translation['host-archive'][lang],
        data: oa_repository,
	color: color_repository,
	legendIndex: 0
    }]
});
return current_chart;
}


// Read a page's GET URL variables and return them as an associative array.
function getUrlVars()
{
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for(var i = 0; i < hashes.length; i++)
    {
        hash = hashes[i].split('=');
        vars.push(hash[0]);
        vars[hash[0]] = hash[1];
    }
    return vars;
}
