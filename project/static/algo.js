//Local namespace object
var dataBank = {};

var isReady = function(card){
    
    cardYr = card[cardYr];
    cardMn = card[cardMn];
    cardDt = card[cardDt];
    
    if (cardYr < getFullYear()) return true;
    else if (cardYr == getFullYear()){
	if (cardMn < getMonth()) return true;
	else if (cardMn == getMonth())
	    if (cardDt <= getDate()) return true;
    }
    return false;

} 

//NOT FINISHED
var initializeSet = function(setID){
    //organize by date
    //on load, store by date. randomize within
    $.ajax({
	url: "/pullData/" + toString(setID);
	type: "POST";
	data: undefined;
	success: function(d){
	    dataBank[active] = JSON.parse(d);
	}
    });

    dataBank[inactive] = [];
    
    for (var i = 0; i < dataBank[active].length; i++){
	var card = dataBank[active][i];
	if (!isReady(card)){
	    dataBank[inactive].push(card);
	}
    }

    if (dataBank[active].length == 0) return false; 
    //do the randomize thing here
    //randomize order 
}


initializeSet();

var updateSet = function(response){
    
    algoPush(response);

    sendToServer();
    
    return getFirstCardData;
    
}

var sendToServer = function(){
    
    var toServer = dataBank[active].concat(dataBank[inactive]);

    $.ajax({
	url: "/liveUpdate";
	type: "POST";
	data: toServer;
	success: function(d){
	    d = JSON.parse(d);
	    console.log("Things were recieved: " + d["data"]);
	}
    });

}

document.getElementById("next").addEventListener("click", updateSet);//next card

var getFirstCardData = function(){
    
    var allData = dataBank[active];
    if (allData.length == 0) return false;
    else return allData[0];

}

//in case they dumb
var quidditched(){

    for (card in dataBank[active]){
	var days = card[interval]; // Days you want to add
	var date = new Date();
	var last = new Date(date.getTime() + (days * 24 * 60 * 60 * 1000));
	card[cardDt] = last.getDate();
	card[cardMn] = last.getMonth();
	card[cardYr] = last.getFullYear();
	dataBank[inactive].push(card);
    }
    sendToServer();
    
}

//DATABANK [<CARD>, <CARD>, <CARD>]
//<CARD>'s are dictionaries
//<CARD> keys are [data, interCt, interval, cardYr, cardMn, cardDt, cardEF]
//data is a list [<piece>, <piece>...]
//cardYr, cardMn, cardDt are scheduled dates
var algoPush = function(response){//the last card was just finished (and it's at the front of the deck), requesting new one... 
    
    //update last card. return new card and verify.
    var removed = dataBank[active].shift();
    var interCt = removed[interCt];
    var interval = removed[interval];
    var cardEF = removed[EF];
    
    if (response < 3){
	interCt = 1;
	interval = 1;
    }
    else {
	if (interCt == 1){
	    interval = 1; 
	}
	else {
	    interval = 6;
	}
	else {
	    interval = Math.ceil(interval * cardEF);
	}
	interCt++;
	cardEF = getNewEF(cardEF, response);
	
    }

    
    if (response < 4){
	dataBank[active].push(removed);
    }
    
    else{
	
	if (interCt == 1){
	    cardDt = getDate();
	    cardMn = getMonth();
	    cardYr = getFullYear();
	}
	    
	var days = interval; // Days you want to add
	var date = new Date();
	var last = new Date(date.getTime() + (days * 24 * 60 * 60 * 1000));
	removed[cardDt] = last.getDate();
	removed[cardMn] =last.getMonth();
	removed[cardYr] =last.getFullYear();
	dataBank[inactive].push(removed);//get interval
	
    }
    
    //next card
    if (dataBank[active].length == 0){
	return false;
    }
    else {
	return rd = dataBank[active][0];
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
