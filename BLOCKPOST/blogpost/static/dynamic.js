/*
    functions for all pages file
*/
function isHidden(el) {
    var style = window.getComputedStyle(el);
    return (style.display === 'none')
} 

function hide_func(){
    var page_name = retrieve_filename();
    id = "middle";
    if(page_name === "About"){
        id="middleabout";
    }
    else if(page_name === "register"){
        id="middleregister";
    }
    if(page_name === "home"){
      //  document.getElementById(id).style.border="solid #f0f0f0 5px";
    }
    
    var sty = isHidden(document.getElementById("left"));
    if(sty){
        document.getElementById("right").style.display = "none";
        document.getElementById(id).style.width ="100vw";
        document.getElementById(id).style.marginLeft="calc(-45vw + 48%)";
        document.getElementById(id).style.marginTop="30%";
    }else{
        document.getElementById("right").style.display = "inline";
        document.getElementById(id).style.width = "50%";
        document.getElementById(id).style.marginLeft = "25%";
        document.getElementById(id).style.marginTop = "10%";
    }
    liked("liked")
}

function retrieve_filename(){
    var path = window.location.pathname;
    var page = path.split("/").pop()
    if(page){
        return page;
    }
    else{
        return "home";
    }
}
/*
    functions for home.html(Home Page) file
*/

function border_func(home_p){
    if(home_p==='home'){
        document.getElementById()
    }
}

/*
    functions for about.html file(About Page) file
*/

var x = 0;
function background_(){
    el_ = document.getElementById("middleabout");
    var backgrounds = new Array(
        "url(static/app_pics/x1.jpeg)",
        "url(static/app_pics/x2.jpeg)",
        "url(static/app_pics/x3.jpeg)",
        "url(static/app_pics/x4.jpeg)"
    );
    el_.style.backgroundImage = backgrounds[x];
    x++;
    if(x >= backgrounds.length){
        x = 0;
    } 
}

function getStyle(el, prop) {
    return (typeof getComputedStyle !== 'undefined' ?
        getComputedStyle(el, null) :
        el.currentStyle
    )[prop];
}

function liked(name){
    var elems = document.getElementsByName(name);
    for(var i=0;i<elems.length;i++){
        elems[i].style.color = "rgb(0,0,250)";
    }
}

function toggle_u_d(x) {
   var color = getStyle(x,"color");
   var vals = color.substring(color.indexOf('(') +1, color.length -1).split(', ');
   if(vals[2] === "11"){
       x.style.color = "rgb(0,0,250)";
       var id = "l"+x.id;
       inc_likes(id,"inc");
   }
   else if(vals[2] === "250"){
       x.style.color = "rgb(11,11,11)";
       var id = "l"+x.id;
       inc_likes(id,"dec");
   }
} 

function inc_likes(id,inc){
    var elem = document.getElementById(id);
    var text = elem.textContent;
    var vals = text.substring(text.indexOf('|') +1, text.length -1).split(' ');
    var num = parseInt(vals[0])
    if(inc === "inc"){
        num=num+1;
        elem.textContent = num.toString()+" Likes";
    }
    else if(inc === "dec"){
        num=num-1;
        elem.textContent = num.toString()+" Likes";
    }
}

function closeForm(){
    document.getElementById("myForm").style.display = "none";
}

function openForm(){
    document.getElementById("myForm").style.display = "block";
}