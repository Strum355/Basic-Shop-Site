#!/usr/local/bin/python3

from os import environ
from http.cookies import SimpleCookie     
from welcome import welcome
from loginText import returnText
import pymysql as db

cookie       = SimpleCookie()
cookieHeader = environ.get('HTTP_COOKIE')
returnText = returnText()
welcomeText = returnText[1]
buttonText  = returnText[0]

print('Content-Type: text/html')
print()
print(""" 
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8" />
        <title>Caps by Alexx | Home</title>
        <link rel="stylesheet" href="styles.css" />
        <script src='slideshow.js'></script> 
        <link rel="icon" href="images/favicon.ico" type="image/x-icon">        
    </head>  
    <body>
        <header>
            <a href=''><img src='images/noshlogo.png' /></a>
            <form action='showroom.py' method='get'>
                <input type='text' placeholder='Search' name='search'>
                <input type='submit' value='Search'>
            </form>            
            <nav>
                <ul>
                    %s
                    <li><a href=''>Home</a></li>
                    <li><a href='showroom.py'>Showroom</a></li>
                    <li><a href='about.py'>About Us</a></li>
                    <li><a href='login.py'>%s</a></li>
                    <li><a href='cart.py'><img src='images/cart.png'/></a></li>
                </ul>
            </nav>
        </header>
        <main>
            <section id='top'>
               <h1>Keycaps by Alex</h1>
               <p>pretty rad if you ask me</p>

            </section>

            <section id='show' class='index'>
                <article>
                    <ul id='slideshow'>
                        <li><img src='images/image1.jpg'/></li>
                        <li><img src='images/image2.jpg'/></li>
                        <li><img src='images/image3.jpg'/></li>                  
                    </ul>
                    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla scelerisque sagittis libero, in rutrum massa dignissim ut. Vestibulum mollis purus quis ipsum finibus dignissim. Sed suscipit vitae elit tincidunt tempus. Nulla facilisi. Morbi vitae porta felis. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Pellentesque mattis ante felis, et commodo est lacinia vitae.
                    </p><p>
Phasellus eu risus volutpat, ultrices erat ut, finibus enim. Etiam porta arcu ex, ut egestas massa iaculis in. Morbi aliquet feugiat felis, at iaculis sapien faucibus ut. Praesent tincidunt ac justo vitae hendrerit. Sed finibus ultricies nibh, nec facilisis felis vulputate eu. Praesent id risus elit. Morbi sollicitudin tortor ac mauris tempus venenatis. Aliquam suscipit vulputate nulla sollicitudin tristique. Morbi vel rutrum ante. Phasellus porta, augue nec consectetur finibus, mauris orci ultrices purus, in accumsan eros augue id lectus. Ut sed orci sagittis, tristique lorem a, convallis nisi. Curabitur eget iaculis diam. Nunc velit mi, porta eu libero ac, vulputate pretium nulla.
</p><p>
Nullam consectetur ultricies viverra. Sed accumsan nunc dolor, eu malesuada quam imperdiet id. Maecenas convallis nisi ut mattis rutrum. Praesent ut odio lacinia, vestibulum enim sed, elementum purus. Ut vulputate sem ut tempor semper. Nunc eleifend mauris sit amet fringilla maximus. Curabitur blandit feugiat ante, ut convallis orci consequat eu. Quisque eget dictum massa, id faucibus diam. Pellentesque quis dictum elit. Aliquam condimentum, elit ut viverra fringilla, nunc ante dictum ante, nec ornare augue risus quis lectus. Mauris eu mauris vel dui ultrices pellentesque nec sit amet ligula. Integer quis turpis sit amet sem cursus mattis.
</p><p>
Donec quis velit lacus. Duis ut lectus vel dui luctus pellentesque eget sit amet justo. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Vestibulum consequat libero metus, sit amet sodales lorem malesuada ut. Etiam non ornare elit, sit amet dapibus dolor. Nam accumsan felis ac massa pharetra ullamcorper. Sed sapien dui, imperdiet nec lacus vel, blandit sodales quam.
</p><p>
Fusce auctor posuere tortor, id dignissim dolor venenatis a. Sed dictum quam mi, varius elementum erat imperdiet quis. Cras tempor quis lectus quis porta. Proin a lorem eu ligula luctus tempor. Maecenas blandit dui porta erat consectetur venenatis. Vivamus fringilla consectetur justo. Pellentesque sit amet luctus ipsum, id malesuada justo. Fusce at arcu nisi. Praesent rutrum risus a lorem rhoncus, at fringilla est rutrum.</p>
                </article>
            </section>
  
        </main>
        <footer>
			<small>&copy; Noah Santschi-Cooney. Powered by a crippling addiction to code.</small>        
		</footer>
    </body>  
</html>
""" % (welcomeText, buttonText))
