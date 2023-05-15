//var modal = document.getElementById("myModal");

var btn = document.getElementById("modal_with_data");
var save_btn = document.getElementById("modal_data_send");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];


// Отправка данных по нажатию на кнопку модульного окна
save_btn.addEventListener("click",function(e){
    document.getElementById("delete_igirgi_data").disabled = false;
    console.log('Отправка файлов заблокирована');
    var data = document.getElementById("modal_data").value;
    var file = document.getElementById("igirgi_file");
    file.value='';
    file.setAttribute('disabled','disabled');
//    console.log("Data" + data);
//    var params = new FormData();
//    params.set('data', data);
//    fetch(document.URL+'data_input/', {
//        method: 'POST',
//        body: params})
    })


