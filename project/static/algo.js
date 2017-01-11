var allCards = document.getElementById("set");
//set should be loaded on page, in javascript dictionary
var cardList = [];

//load by lowest priority
var getNextCard = function(){//variable is a 
    var champ = 0;
    for (int i = 1; i < allCards.length(); i++){
	if (allCards.childNodes[i].priority < allCards.childNodes[champ].priority){
	    champ = i;
	}
    }
    return champ;
    //decrement everyone's priority??? time issue
}

var updatePriorities = function(response){
    //get currently active card
    //use a getByID with constraint if that's a thing...
    //just loop for now
    for (int i = 0; i < allCards.length(); i++){
	if (allCards.childNodes[i].current = true){
	    allCards.childNodes[i].priority += response;
	    return;
	}
    }
    
}
