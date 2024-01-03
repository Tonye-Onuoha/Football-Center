window.onload = function(){
	let statsTableHeight = $("#statsTable").height()
	$("#chatApp").css("height",statsTableHeight)
	
	
	let thumbs = document.querySelectorAll("i.thumb")
	for (i = 0; i < thumbs.length; i++) {
		thumbs[i].addEventListener("click",function() {
			if ($(this).css("color") != "rgb(255, 191, 0)") {
				$(this).css("color","rgb(255, 191, 0)")
			}
			else {
				$(this).css("color","rgb(0, 0, 0)")
			}
		})
	}
}




function opentab(evt, box) {
	let content = document.getElementsByClassName("usertabcontent")
	for (let i = 0; i < content.length; i++) {
		content[i].style.display = "none";
	}
	let links = document.getElementsByClassName("tablinks")
	for (let i = 0; i < links.length; i++) {
		links[i].className = links[i].className.replace(" activetab", "");
	}
	document.getElementById(box).style.display = "block";
	evt.currentTarget.className += " activetab";
}

