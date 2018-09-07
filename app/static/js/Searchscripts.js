


function CallIn(URL, Id) {
    $.ajax({
        url: URL,
        dataType: "html",
        async: true,
        success: function (data) {
            $(Id).hide().html(data).fadeIn({ duration: 1000 });            
        }
    })
};


function getWiki(species){
    var indst = species.indexOf('(') + 1
    var inden = species.indexOf(')')
    var fullsci = species.substring(indst,inden)

    var spin = fullsci.indexOf(' ')
    var genus = fullsci.substring(0,spin)
    var specd = fullsci.substring(spin+1)



    var wormsjson = 'http://marinespecies.org/rest/AphiaIDByName/'+genus+'%20'+specd
    
    $.getJSON(wormsjson,function(data){
        var wormsid = '<p>'+data+'</p>'
        var wormshtml = "<a id='wormsbutton' href='http://marinespecies.org/aphia.php?p=taxdetails&id="+data+"' target='_blank' class='btn btn-info'>\
        <span class='glyphicon glyphicon-globe'></span> Go</a>"

        $('#worms').html(wormsid);
        $('#wormsbut').html(wormshtml);

    });
    


    var URL = 'https://en.wikipedia.org/api/rest_v1/page/summary/'+genus+'_'+specd

    var wikilink = 'https://en.wikipedia.org/wiki/'+genus+'_'+specd
    var wikihtml = "<p><a href="+wikilink+" style='color:blue'>Click here for the full Wikipedia article</a></p>"

    $.getJSON(URL,function(data){
        var fullhtml = '<h2>From Wikipedia:</h2>'+data.extract_html
        $('#wiki').html(fullhtml)
        $('#wikilink').html(wikihtml)

    });




}

function getGBIF(species){
    var indst = species.indexOf('(') + 1
    var inden = species.indexOf(')')
    var fullsci = species.substring(indst,inden)

    var spin = fullsci.indexOf(' ')
    var genus = fullsci.substring(0,spin)
    var specd = fullsci.substring(spin+1)

    $('#idd').html('<p>test</p>');

    var gbifjson = 'http://api.gbif.org/v1/species?name='+genus+'%20'+specd;

    $.getJSON(gbifjson,function(data){
        var gbifkey = '<p>'+data.results[0].key+'</p>'
        var gbifhtml = "<a href='https://www.gbif.org/species/"+data.results[0].key+"' target='_blank' class='btn btn-info'><span class='glyphicon glyphicon-globe'></span> Go</a>";
        $('#gbif').html(gbifkey);
        $('#gbifbutton').html(gbifhtml);

    });


}




function catsearch(e,out) {    
    var ID = $(e).data('value');
    if (out == '#subcatstab') {
        $('#subgrpstab').hide();
        $('#specstab').hide();
    } else if (out == '#subgrpstab') {
        $('#specstab').hide();
    }
    CallIn(ID,out)
}




function cs() {
    var X = $('#Search option:selected').val()
    var URL = '/spec/?spec='.concat(X); 
    CallIn(URL,'#mainframe')
    
}


function ls() {
    var X = $('#LSearch option:selected').val()
    var URL = '/info/?spec='.concat(X); 
    
    var spec = $('#LSearch option:selected').text()
    
    CallIn(URL,'#infoframe')
    getWiki(spec)
    setTimeout(function(){ getGBIF(spec)
    }, 30);
    

}


