(function() {

    var radios = [];

    document.addEventListener('DOMContentLoaded', init, false);

    function init(){
        insert = document.querySelector('#show');
        radios = document.getElementsByName('sort');
        for(i = 0; i < radios.length; i++){
            radios[i].addEventListener('change', sendRequest, false);
        }
    }

    function sendRequest(event){
        var id = event.target.id;
        var url = window.location.search;
        url = url.replace("?", '');
        if(url != ''){
            url = '&'+url;
        }
        request = new XMLHttpRequest();
        request.addEventListener('readystatechange', getResponse, false);
        request.open('GET', 'sortShowroom.py?sortBy=' +id+url, true);
        request.send(null);
    }

        function getResponse() {
        if(request.readyState === 4){
            if(request.status === 200){
               insert.innerHTML = request.responseText;     
            }
        }
    }
}());