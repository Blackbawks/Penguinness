

function addrow(ee) {
    var idval = $(ee).attr('id');
    var numval = parseInt(idval.substring(6,7), 10) + 1;
    var newval = '#Search'+numval+'row';
    $(newval).show()
}

function removerow(ee) {
    var idval = $(ee).attr('id');
    var newval = '#Search'+idval.substring(6,7)+'row';
    var selectid = '#Search'+idval.substring(6,7);
    $(selectid).val('default').selectpicker("refresh");
    $(newval).hide();
    
}

function viewdata() {

    $('#diveintro').hide();
    $('#myChart').show();

    var listItems = ['#Search1','#Search2','#Search3','#Search4','#Search5'];
    
    var arrayLength = listItems.length;
    var arr = [];
    for (var i = 0; i < arrayLength; i++) {
        if($(listItems[i]).val() != 'Select by common or latin name'){
            arr.push($(listItems[i]).val());
        }
        
    };
    var joined = arr.join('&specid=');
    var URL = '/DiveData/?specid='+joined;
    


    for(var i = 0; i < 7; i++){
        removeData(chart,landmark=true);
    }

         
    var colors = ['#6699CC','#FFF275','#FF8C42','#FF3C38','#A23E48']
    $.getJSON(URL,function(data){

        var arrlen = Object.keys(data.keys).length

    
        chart.data.datasets[0].backgroundColor = [];  

        for(var i = 0; i < arrlen; i++){
                      
            addData(chart,data.keys[i],data.data[i],data.max[i],colors[i],i)

        }


    });
    
};



function addData(Chart, label, data, point, colour,i) {
    Chart.data.labels.push(label);
    Chart.data.datasets[0].backgroundColor[i] = colour;

    Chart.data.datasets[0].data.push(data);
    
    if(point != 0){
        Chart.data.datasets[1].data.push(point);
    };

    Chart.update();
}

function addLData(Chart, label, data, colour,i) {
    Chart.data.labels.push(label);
    Chart.data.datasets[0].backgroundColor[i] = colour;

    Chart.data.datasets[0].data.push(data);

    Chart.update();
}


function removeData(chart,landmark) {
    chart.data.labels.pop();
    chart.data.datasets[0].data.pop();
    if(landmark==true){
        chart.data.datasets[1].data.pop();
    }
    chart.update();
}

function addLandmark(){

    var height = parseInt($('#Landmark').val(),10);
    var lname = $('#Landmark option:selected').text();


    var listItems = ['#Search1','#Search2','#Search3','#Search4','#Search5'];
    
    var arrayLength = listItems.length;
    var arr = [];
    for (var i = 0; i < arrayLength; i++) {
        if($(listItems[i]).val() != 'Select by common or latin name'){
            arr.push($(listItems[i]).val());
        }
        
    };

    alen = arr.length

    if(alen < chart.data.datasets[0].data.length){
        removeData(chart,landmark=false)
    };

    if(height > 0){
        var spot = chart.data.datasets[0].data.length
        addLData(chart,lname,height,'#0F0102',spot)
        chart.data.datasets[0].labels[spot] = 'Height'
    };


}