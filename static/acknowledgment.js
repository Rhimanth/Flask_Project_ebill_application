function generateCoustmerId(){
    var randomNumber=Math.floor(Math.random()*90000)+10000;

    return randomNumber;
}

function displayCustomerInfo(){
    var coustmerId=generateCoustmerId();
    //document.getElementById("c_id").innerHTML=coustmerId;
}

window.onload=displayCustomerInfo;