


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