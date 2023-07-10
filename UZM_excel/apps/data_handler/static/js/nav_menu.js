
window.addEventListener('load', () => {
    let path = window.location.search.toString()  // что было выбрано
    if (path != ''){
    console.log('Выбрано', path)
    sessionStorage.setItem("url_status", path); // сохраняем выбранный элемент
    } else {
    let status = sessionStorage.getItem("url_status");

    if (status != null) { // востанавливаем выбранный элемент
        if  (window.location.href.toString().includes('/data_handler/trajectories') || window.location.href.toString().includes('/data_handler/parametrs')){
        window.location = window.location.href + status; }
    }

    }
});

