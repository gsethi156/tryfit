$("header").append("<div class='glitch-window'></div>");
//fill div with clone of real header
$("h1.glitched")
	.clone()
	.appendTo(".glitch-window");
