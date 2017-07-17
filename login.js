(function (){

    document.addEventListener('DOMContentLoaded', init, false);

    var pass, pass1;
    
    function init(){
        pass     = document.querySelector('#pass');
        pass1    = document.querySelector('#pass1');

        pass.addEventListener('change', validate, false);
        pass1.addEventListener('change', validate, false);
    }

    function validate(){
        console.log('yes');
        if(pass.value != pass1.value){
            console.log('no');
            pass1.setCustomValidity("Passwords don't match");
        }else{
            pass1.setCustomValidity('');
        }
    }

}());