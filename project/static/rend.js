var card2 = document.getElementById("mod2");
var body = document.getElementById("cc1");
var body2 = document.getElementById("cc2");
var save = document.getElementById("save");
var edit = document.getElementById("edit");
var img = document.getElementById("img");
var place = document.getElementById("picture");
var spin = 0;
var back = document.getElementById("front");
var next = document.getElementById("next");

var cards;

var brow = document.getElementsByClassName('btn-secondary');

for(var i = 0; i< brow.length; i++){
	brow[i].onclick = pls;
}

//permanent nodes
var front = document.createElement('p');
//var backs = document.createElement('p');
var f = document.createTextNode("");
//var b = document.createTextNode("");
front.appendChild(f);
//global variable counter for current set
var count = 0;

//creation of test variables
var mama = document.createElement('p');
var pool = document.createTextNode("I AM AN APPLE");
mama.appendChild(pool);
var dada = document.createElement('p');
var poole = document.createTextNode("I AM AN ORANGE");
dada.appendChild(poole);
var son = document.createElement('p');
var pole = document.createTextNode("I AM A DOG");
son.appendChild(pole);
var dau = document.createElement('p');
var poles = document.createTextNode("I AM AN USERID");
dau.appendChild(poles);

function pls(){
	count += 1;
	if (count >= Object.keys(cards['cards']).length) count = 0;
	console.log(count);
	setTimeout(function(){body2.style.boxShadow = "2px 2px 2px black";}, 2000);
	if(spin % 360 != 0 && spin != 0) body2.style.transform = "rotateY(180deg)";
    body2.style.left = "50%";
	body2.style.top = "35%";
	body2.style.height = "40%";
	body2.style.width = "40%";
	body2.style.marginLeft = "-20%";
	body2.removeAttribute("right");
	body2.style.zIndex = 3;
	body2.style.display = "flex";
	body2.style.backgroundColor = "#76A2C1";
	body2.style.transition = "1s";
	body2.appendChild(front);
	f.nodeValue = cards['cards'][count.toString()]["front"][0];
	body2.style.display = "flex";
	setTimeout(function(){
	body.innerHTML = "";
	body.style.backgroundColor = "#345CA8";
	body.style.right = "0";
	body.style.left= "40%";
	body.style.top = "30%";
	body.style.height = "30%";
	body.style.width = "20%";
	body.style.transition = "1s";
	body.style.zIndex = 2;
	body.innerHTML = "";
	},1000);
	setTimeout(function(){body = [body2, body2 = body][0]}, 2000);
	
}

/*img.onclick = function (){
	var i = document.getElementById("mage").value;
	$.ajax({
		url: '/data',
		type: 'GET',
		data: "moo",
		success: function(d){
			var pos = document.createElement('img');
			pos.style.maxWidth = "100%";
			pos.style.maxHeight = "100%";
			pos.className = "card-img-top";
			pos.src = i;
			place.appendChild(pos);
		}
	});
}*/

back.onclick = function(){
	spin += 180;
	body.style.transform = "rotateY(" + spin + "deg)";
	body.style.transition = "1s";
	setTimeout(function(){if(spin % 360 != 0){
		    $.ajax({
			   url: '/data',
			   type: 'GET',
			   data: "no data",
			   success: function(d){
					//d = JSON.parse(d);
					/*mama.id = "yes";
					mama.onclick = function(){
					var edi = document.createElement('input');
				    edi.defaultValue = d['string'] ;
					edi.style.transform = "rotateY(180deg)";
					body.removeChild(document.getElementById("yes"));
					body.insertBefore(edi, body.childNodes[0]);
					card2 = edi;
					}
					front.style.transform = "rotateY(180deg)";
				    body.appendChild(mama);*/
			}});
			f.nodeValue = cards['cards'][count.toString()]["back"][0];
			front.style.transform = "rotateY(180deg)";
	}
	else{
		f.nodeValue = cards['cards'][count.toString()]["front"][0];
		front.style.transform = "rotateY(0deg)";
	}}, 300);
}

window.onload = function(){
	$.ajax({
		url: '/pullSet1/1/',
		type: 'GET',
		success: function(d){
            console.log(d);
			d = JSON.parse(d);
			cards = d;
			body.appendChild(front);
			front.style.fontSize = "30px";
			f.nodeValue = cards['cards'][count.toString()]["front"][0];
			console.log("this is the best");
			console.log(window.location.href.split("/"));
			/*for(i = 0; i < Object.keys(d['cards']).length; i++){
				console.log(d['cards'][i.toString()]["front"][0]);
				console.log(d['cards'][i.toString()]["back"][0]);
			}
			console.log(window.location.href.split("/"))
			console.log(d['cards'][0]["front"][0]);
			console.log(d);*/
		}
	});
	var notify = document.createElement("div");
	var saved = document.createTextNode("Your card has been saved in the set");
	notify.appendChild(saved);
	notify.id = "notify";
	document.body.appendChild(notify);
}

save.onclick = function(){
	var d = document.getElementById("description");
	var t = document.getElementById("title");
	var moe = document.getElementById("notify");
	moe.style.opacity = 1;
	setTimeout(function(){moe.style.opacity = 0;},3000);
	var info = {}
	info['desc'] = d.value;
	info['title'] = t.value;
	d.value = '';
	t.value =  '';
	/*var length = i.length;
	var height = 1;
	while(length - 24 > 0){
		height++;
		length -= 24;
	}*/
	$.ajax({
		url: '/pushData/1/',
		type: 'GET',
		data: info,
		success: function(d){
			/*body.removeChild(card2);
			var pos = document.createElement('p');
			var te = document.createTextNode(i);
			if(spin % 360 != 0) pos.style.transform = "rotateY(180deg)";
			pos.appendChild(te);
			pos.className = "card-title";
			pos.style.fontSize = 30 - height + "px";
			pos.style.fontFamily = "sans-serif";
			pos.style.textAlign = "center";
			pos.style.margin = 0;
			pos.id = "yes";
			pos.onclick = function(){
				var edi = document.createElement('input');
				if(spin % 360 != 0) edi.style.transform = "rotateY(180deg)";
				edi.defaultValue = i;
			        body.removeChild(document.getElementById("yes"));
				body.insertBefore(edi, body.childNodes[0]);
				card2 = edi;
			}
			body.insertBefore(pos, body.childNodes[0]);*/
		}
	});
}
