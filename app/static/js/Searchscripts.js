$(document).ready(function () {
    $('a').on("click", function (e) {
        var cl = $(this).attr('class');
        if (cl == 'catas') {
            e.preventDefault();
            $("#subcatstab").load($(this).attr('href'), function () { }).hide().fadeIn(1000);
            $('#subgrpstab').hide();
            $('#specstab').hide();
        } else if (cl == 'subcatas') {
            e.preventDefault();
            $("#subgrpstab").load($(this).attr('href'), function () { }).hide().fadeIn(1000);
            $('#specstab').hide();
        } else if (cl == 'subgrps') {
            e.preventDefault();
            $("#specstab").load($(this).attr('href'), function () { }).hide().fadeIn(1000);
        } else {            
        };

        
        
    });
});
