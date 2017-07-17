(function(){

    document.addEventListener('DOMContentLoaded', init, false);
    var index = 0;
    var numImages, numDots;
    var images = [];
    var dots = [];
    function  init(){
        images = document.querySelectorAll('#slideshow img');
       // dots   = document.querySelectorAll('.dot');

        numImages = images.length;
       // numDots   = dots.length;

        display();
        window.setInterval(display, 5000);
    }

    function display(){
        index = index % numImages;
        for(i = 0; i < numImages; i++){
            images[i].style.display = 'none';
            //dots[i].className = dots[i].className.replace(' active', '');
        }  

        //dots[index].className += ' active';
        images[index].style.display = 'inline';
        index++;
    }
}());