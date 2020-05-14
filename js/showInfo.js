function showInfo() {
   var x = document.getElementById("kontakt");
   var y = document.getElementById("logo");
   if (x.style.display === "block") {
     x.style.display = "none";
	 y.style.width="80px";
	 y.style.height="40px";

   } else {
     x.style.display = "block";
	 y.style.width="160px";
	 y.style.height="80px";
   }
   }
