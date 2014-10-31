$.getJSON('http://api.giphy.com/v1/gifs/search?q=doge&limit=20&rating=pg&api_key=dc6zaTOxFJmzC',
function(data) {
  var randMeme = Math.floor((Math.random() * 20) + 1);
  console.log(data.data[randMeme]);
  var chosenMeme = data.data[randMeme].images.original.url;
  document.getElementById("test").style.backgroundImage="url('"+chosenMeme+"')";
});
if (document.getElementById("submit"))
	document.getElementById("submit").disabled = true;

function validateLongURL(){
   var lurl = document.getElementById('longURL');
   document.getElementById('shortURL').value = "";
   if(isUrl(lurl.value)){
      document.getElementById("submit").disabled = false;
      lurl.style.backgroundColor = "#B1FFB1"
      genShort();
   }else{
      document.getElementById("submit").disabled = true;
      lurl.placeholder = "Please input a valid URL";
      lurl.value = "";
      lurl.style.backgroundColor = "#FFB6B3";
   }

};

function validateShortURL(){
   var surl = document.getElementById('shortURL');
   if(isSUrl(surl.value)){
      document.getElementById("submit").disabled = false;
      surl.style.backgroundColor = "#B1FFB1"
   }else{
      document.getElementById("submit").disabled = true;
      surl.placeholder = "Only letters are allowed in a short URL, no numbers";
      surl.value = "";
      surl.style.backgroundColor = "#FFB6B3";
   }

};

function genShort() {
   var surl = document.getElementById('shortURL');
   var tt = new Date().getTime();
   var digits = [];
   var letters = [];
   var remainder = 0;
   var ascii_code = 0;

   while(tt > 0){
      remainder = ~~(tt % 52);
      if(remainder > 0){
         digits[digits.length] = remainder;
      }
      tt = tt / 52;
   }

   digits = shuffle(digits);

   for(var x=0; x<digits.length; x++){
      ascii_code = 0;
      if(digits[x] > 26){
         ascii_code = 65 + (digits[x] - 26);
      }else{
         ascii_code = 97 + digits[x];
      }
      letters[letters.length] = String.fromCharCode(ascii_code);
   }
   surl.value = letters.join("");
};

function isSUrl(s) {
   // var regexp = /^(?!\.\*[0-9 ])[a-zA-Z]+/;
   var regexp = /^[a-zA-Z]+$/;
   console.log(regexp.test(s));
   return regexp.test(s);
};

function isUrl(s) {
   var regexp = /((ftp|http|https):\/\/)?(\w+:{0,1}\w*@)?(\S+)\.(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/
   return regexp.test(s);
};


function shuffle(o){
    for(var j, x, i = o.length; i; j = Math.floor(Math.random() * i), x = o[--i], o[i] = o[j], o[j] = x);
    return o;
};