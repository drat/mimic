function refreshIframe() {
    var ifr = document.getElementsByName('Right')[0];
    ifr.src = ifr.src;
}

function myHandler(e) {
    $("#myVideo").fadeOut(1000);
    $("#loginForm").fadeIn(3000);
}

setTimeout(function (){
    myHandler("")
 }, 3000)