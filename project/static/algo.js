//Local namespace object
var dataBank = {};

var getData = function(){

    $.ajax({
	url: "/pullData";
	type: "POST";
	data: undefined;
	success: function(d){
	    dataBank.cardData = JSON.parse(d);
	}
    });
    
}

getData();

var updateSet = function(){
    
    //var i = document.getElementById("curCardData").value;//something
    var i = getFirstCardData();

    var input = {"curCardData": i};

    $.ajax({
	url: "/liveUpdate";
	type: "POST";
	data: input;
	success: function(d){
	    d = JSON.parse(d);
	    console.log("Things were recieved: " + d["data"]);
	}
    });

}

document.getElementById("next").addEventListener("click", updateSet);//next card

var getFirstCardData = function(){
    
    var allData = dataBank.cardData;
    return allData[0];

}

//load by next up
var algoPush = function(response){//0-5 
    
    var removed = dataBank.cardData.splice(0,1);
    //temp: add to back;
    dataBank.cardData.push(removed);

    var newEF = getNewEF(removed[-1], response);
    if (response >= 3)
	removed[-1] = newEF; //update EF;
    else
	var pushAmt = algo(response);
    //put in a size check (if > array length)
//  dataBank.cardData.splice(pushAmt, 0, removed);
    
}

var algo = function(response){//0-5
    if (response < 3) return;
    else{
	var 
    }
    
    
}

var getNewEF = function(EF, response){//0-5
    newEF = EF - 0.8 + .28*response-0.02*response*response;
    if (newEF < 1.3) return 1.3;
    else return newEF;
}

//activeCard
//card_dict is a global variable
//somewhere, assume default EF is 2.5
//todo: put a cutoff for the session (you're done)

//algo notes: if I"m understanding this correctly, at the start of a session, first push is 1, second is 6, and then it starts getting scaled... we'll store that locally...
