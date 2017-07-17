(function() {
    
    var username, checkSpan, request;

    document.addEventListener('DOMContentLoaded', init, false);

    function init(){
        username  = document.querySelector('#regName');
        checkSpan = document.querySelector('#check');

        username.addEventListener('keypress', setLink, false);
        checkSpan.addEventListener('click', sendRequest, false);
    }

    function setLink(){
        checkSpan.innerHTML = '<a href="#">Check name is available</a>';
    }

    function sendRequest(){
        request = new XMLHttpRequest();
        request.addEventListener('readystatechange', getResponse, false);
        request.open('GET', 'nameCheck.py?username=' + username.value, true);
        request.send(null);
    }
    
    function getResponse(){
        if(request.readyState === 4){
            if(request.status === 200){
                if(request.responseText.trim() === 'free') {
                    checkSpan.innerHTML = 'Name available';
                }else if(request.responseText.trim() === 'taken') {
                    checkSpan.innerHTML = 'Name not available';
                }
            }
        }
    }
})();