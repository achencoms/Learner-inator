//Local namespace object
var dataBank = {};

var getData = function(){
    //on load, store by date. randomize within
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

//interYr:
//load by next up
//DATABANK [<CARD>, <CARD>, <CARD>]
//<CARD>'s are dictionaries
//<CARD> keys are [data, interCt, interval, cardYr, cardMn, cardDt, cardEF]
//data is a list [<piece>, <piece>...]
//cardYr, cardMn, cardDt are scheduled dates
var algoPush = function(response){//the last card was just finished (and it's at the front of the deck), requesting new one... 
    
    //update last card. return new card and verify.
    var removed = dataBank.cardData[0];
    var nxtCard = dataBank.cardData[1];

    //temp: add to back;
    //dataBank.cardData.push(removed);
    
    var interCt = removed[1];
    var interval = removed[2];
    if (response < 3){
	interCt = 1;
    }
    if (response < 4){
	dataBank.cardData.push(removed);
    }
    if (interCt == 1){
	removed[cardYr] = 
    } 
    //assuming we're supposed to do it on the given day
    //next card
    var cardYr = nxtCard[3];
    var cardMn = nxtCard[4];
    var cardDt = nxtCard[5];
    var cardEF = nxtCard[6];
    if (cardYr <= getFullYear() && cardMn <= getMonth() && cardDt <= getDate()){
	return nxtCard[0]; //data
    }
    else {
	return false; //we're done. go home
    }
    var newEF = getNewEF(cardEF, response);
    if (response >= 3)
	removed[-1] = newEF; //update EF;
    else
	var pushAmt = algo(response);
    //put in a size check (if > array length)
//  dataBank.cardData.splice(pushAmt, 0, removed);
    //add interval when pushed into backend.
    
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
