

window.addEventListener('load', () => {
    let path = window.location.search.toString()  // что было выбрано
    if (path != ''){
    console.log('Выбрано', path)
    localStorage.setItem("url_status", path); // сохраняем выбранный элемент
    } else {
    let status = localStorage.getItem("url_status");
    if (status != null && window.location.href.toString().includes('/data_handler/trajectories')) { // востанавливаем выбранный элемент
        window.location = window.location.href + status
    } else {
        console.log('hi', window.location.href)
    }

    }
});

