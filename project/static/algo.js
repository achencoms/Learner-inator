//Local namespace object
var dataBank = {};

dataBank.allCards = document.getElementById("set");
//set should be loaded on page, in javascript dictionary

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
    
    var i = document.getElementById("cardData").value;//something
    var input = {"cardData": i};

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
var algoPush = function(){ 
    //temp: add to back;
    removed = dataBank.cardData.splice(0,1);
    dataBank.push(removed);

}

var updatePriorities = function(response){
    //get currently active card
    //use a getByID with constraint if that's a thing...
    //just loop for now
    for (int i = 0; i < card_dict.length(); i++){
	if (allCards.childNodes[i].current = true){
	    allCards.childNodes[i].priority += response;
	    return;
	}
    }
    
}

//activeCard
//card_dict is a global variable
