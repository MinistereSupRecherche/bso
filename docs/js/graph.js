function include_graph(container_name, graph_name, collapse_name, page_name, text_share, lang) {

var url_to_embed = "https://ministeresuprecherche.github.io/bso/" + page_name
var twitter_share = "https://twitter.com/intent/tweet?text=" + text_share 
twitter_share += "&url=" + url_to_embed
twitter_share += "&related=sup_recherche&hashtags=OpenAccess,ScienceOuverte,dataESR"

var facebook_share = "http://www.facebook.com/sharer.php?u=" + url_to_embed
facebook_share += "&t=" + text_share

url_for_linkedin = "https://ministeresuprecherche.github.io/bso/logo_fr.png"
var linkedin_share = "http://www.linkedin.com/shareArticle?mini=true&url=" + url_for_linkedin
linkedin_share += "&title=" + text_share

var html ="<div id='" + container_name + "' class='graph_card'></div>"
html += "<div class='collapse' id='" + collapse_name +"'>"
html += "<div class='' style='background-color:white;padding:10px;'>"
html += translation['desc_embed'][lang]

html += "<textarea readonly class='form-control' rows='3'> <iframe src='" + url_to_embed +"' width='500px' height='700px' frameborder='0' scrolling='auto'></iframe> </textarea>"
html += "</div> </div>"

html+="<div class='card-footer text-muted'><ul class='card-ul'>"

html+="<li class='card-li'>"
html+= translation['download'][lang]
html+="</li>"

html+="<li class='card-li'>"
html+="<a style='color:white' href='#!' onclick=\"export_file(" + graph_name +", 'xls')\" data-toggle=\"tooltip\" data-placement='top' title='"
html += translation['tooltip_xls'][lang]
html += "'>"
html+="<i class='fas fa-lg fa-file-excel' aria-hidden='true'></i></a></li>"

html+="<li class='card-li'>"
html+="<a style='color:white' href='#!' onclick=\"export_file(" + graph_name +", 'csv')\" data-toggle=\"tooltip\" data-placement='top' title='"
html += translation['tooltip_csv'][lang]
html += "'>"
html+="<i class='fas fa-lg fa-file-csv' aria-hidden='true'></i></a></li>"

html+="<li class='card-li'>"
html+="<a style='color:white' href='#!' onclick=\"export_file(" + graph_name + ", 'image/png')\" data-toggle=\"tooltip\" data-placement='top' title=\""
html += translation['tooltip_png'][lang]
html += "\">"
html+="<i class='fas fa-lg fa-file-image' aria-hidden='true'></i></a></li>"

html+="<li class='card-li'>"
html+= translation['integrate'][lang]
html+="</li>"

html+="<li class='card-li' style='cursor:pointer;' data-toggle='collapse' href='#" + collapse_name +"' aria-expanded='false' aria-controls='" + collapse_name + "'>"
html+="<a style='color:white' data-toggle=\"tooltip\" data-placement='top' title=\""
html+= translation['tooltip_embed'][lang]
html += "\">"
html+="<i class='fas fa-lg fa-code' aria-hidden='true'></i></a></li>"

html+="<li class='card-li'>"
html+= translation['share'][lang]
html+="</li>"

html+="<li class='card-li'>"
html+="<a style='color:white' href='" + twitter_share + "' data-toggle=\"tooltip\" data-placement='top' title=\""
html+= translation['share_twitter'][lang]
html+="\" >"
html+="<i class='fab fa-lg fa-twitter' aria-hidden='true'></i></a></li>"

html+="<li class='card-li'>"
html+="<a style='color:white' href='" + facebook_share + "' data-toggle=\"tooltip\" data-placement='top' title=\""
html+= translation['share_facebook'][lang]
html+="\" >"
html+="<i class='fab fa-lg fa-facebook-f' aria-hidden='true'></i></a></li>"

html+="<li class='card-li'>"
html+="<a style='color:white' href='" + linkedin_share + "' data-toggle=\"tooltip\" data-placement='top' title=\""
html+= translation['share_linkedin'][lang]
html+="\" >"
html+="<i class='fab fa-lg fa-linkedin' aria-hidden='true'></i></a></li>"

$('#'+graph_name).html(html); 

}
