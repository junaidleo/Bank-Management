function num_check(id){
    if(!isNaN(document.getElementById(id).value)){
        document.getElementById(id).style.color=rgb(83, 80, 80);
    }
    else{
        document.getElementById(id).style.color="red";
    }
}
function message(){
    document.getElementById('message').hidden=true;
}