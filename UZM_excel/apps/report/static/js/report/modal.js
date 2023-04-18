// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("modal_with_data");

var save_btn = document.getElementById("modal_data_send");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal
btn.onclick = function() {
  modal.style.display = "block";
}

save_btn.onclick = function() {
    modal.style.display = "none";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

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


