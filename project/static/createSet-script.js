$(document).ready(function() {
    var cardCount = 1;
    $("#createSetForm").submit(function(e) {
        e.preventDefault();
	
        setData = {};
        //setData["setName"] = $("#setName").value;
		setData["setName"] = document.getElementById("setName").value;
        cardList = [];
        for (i = 1; i < cardCount + 1; i++) {
            entry = {};
			entry["frontText"] = document.getElementById("cardFront" + i).value;
			entry["backText"] = document.getElementById("cardBack" + i).value;
            //entry["frontText"] = $("#cardFront" + i).value;
            //entry["backText"] = $("#cardBack" + i).value;
            entry["imageName"] = "";
            entry["audioName"] = "";
            cardList.push(entry);
        }
        setData["cardList"] = cardList;
        $.ajax({
            type: "POST",
            url: "/createSet/",
            data: setData,
            success: function(d) {
                if (d != "False") { /*assuming that its a set id*/
                    window.location = "/viewSet/" + d;
                } else {
                    window.location = "/";
                }
            }
        });
    });
    $("#addButton").click(function(e) {
        newCard = document.createElement("div");
        cardCount += 1;
        newCard.innerHTML = `
          <div class="row">
              <div class="col-md-5 cardFrontCol">
                  <textarea id="cardFront` + cardCount + `" class="cardSide" name="cardFront` + cardCount + `" rows="2" maxlength="200" required></textarea>
              </div>
              <div class="col-md-5 cardBackCol">
                  <textarea id="cardBack` + cardCount + `" class="cardSide" name="cardBack` + cardCount + `" rows="2" maxlength="200" required></textarea>
              </div>
              <div class="col-md-2 cardButtons">
                  <div class="btn-group" role="group">
                      <button type="button" class="btn btn-defaul"><i class="glyphicon glyphicon-picture"></i></button>
                      <button type="button" class="btn btn-default"><i class="glyphicon glyphicon-music"></i></button>
                  </div>
              </div>
          </div>
        `
        document.getElementById("cardList").appendChild(newCard);
    });
});
