var color_set_div = document.getElementById('colors_set');
var color_sliders_div = document.getElementById('color_sliders');
var speed_sliders_div = document.getElementById('rainbow_slider');

const modes_objects_list = [
    color_set_div,
    color_sliders_div,
    speed_sliders_div
]

$(document).ready(function() {
    $("#set").prop("set", true).trigger("click");

    show_current_mode(modes_objects_list, 0);

    $(function() {
        $("#slider_r").slider({
            slide: function(event, ui) {
                $("#display_r").html(ui.value);
                $("#slider_r.ui-slider").css("background", `rgb(${ui.value}, 0, 0)`);
                change_color_square();
            },
            min: 0,
            max: 255
        });
    });
    $(function() {
        $("#slider_g").slider({
            slide: function(event, ui) {
                $("#display_g").html(ui.value);
                $("#slider_g.ui-slider").css("background", `rgb(0, ${ui.value}, 0)`);
                change_color_square();
            },
            min: 0,
            max: 255
        });
    });
    $(function() {
        $("#slider_b").slider({
            slide: function(event, ui) {
                $("#display_b").html(ui.value);
                $("#slider_b.ui-slider").css("background", `rgb(0, 0, ${ui.value})`);
                change_color_square();
            },
            min: 0,
            max: 255
        });
    });
    $(function() {
        $("#slider_speed").slider({
            slide: function(event, ui) {
                $("#display_speed").html(ui.value/1000);
            },
            min: 0,
            max: 100
        });
    });
})

function change_color_square() {
    var color_square = document.getElementById('color_square');

    var c_r = document.getElementById('display_r').innerHTML;
    var c_g = document.getElementById('display_g').innerHTML;
    var c_b = document.getElementById('display_b').innerHTML;

    color_square.style.background = `rgb(${c_r}, ${c_g}, ${c_b})`;
}

function loadDoc() {
    var req = new XMLHttpRequest();

    var all_set_colors = document.getElementsByName('color');

    var got_color = null;

	for(i = 0; i < all_set_colors.length; i++) {
		if(all_set_colors[i].checked) {
    	    curr_id = all_set_colors[i].id;
            got_color = $(`#${curr_id}~span`).css('background-color');
        }
	}

    var ele = document.getElementsByName('modes');
	var current_mode = "1";
              
	for(i = 0; i < ele.length; i++) {
		if(ele[i].checked) {
    	    current_mode = ele[i].value;
        }
	}

    var c_r = 0;
    var c_g = 0;
    var c_b = 0;

    console.log(got_color);

    if (current_mode == 1) {
        c_r = getRGB(got_color).red;
        c_g = getRGB(got_color).green;
        c_b = getRGB(got_color).blue;
    }
    if (current_mode == 2) {
        c_r = document.getElementById('display_r').innerHTML;
        c_g = document.getElementById('display_g').innerHTML;
        c_b = document.getElementById('display_b').innerHTML;
    }
    
    var rainbow_speed = document.getElementById('display_speed').innerHTML;
    console.log(rainbow_speed);

    req.open('POST', '/', true);
    req.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    req.send(
        "color_r=" + c_r + "&" +
        "color_g=" + c_g + "&" +
        "color_b=" + c_b + "&" +
        "modes=" + current_mode + "&" +
        "rainbow_speed=" + rainbow_speed
    );
}

function modeChanged() {
    show_current_mode(modes_objects_list, 1);

    var ele = document.getElementsByName('modes');
	var current_mode = "1";
              
	for(i = 0; i < ele.length; i++) {
		if(ele[i].checked) {
    	    current_mode = ele[i].value;
            if (current_mode == 1) {
                show_current_mode(modes_objects_list, 0);
            }
            else if (current_mode == 2) {
                show_current_mode(modes_objects_list, 1);
            }
            else if (current_mode == 3) {
                show_current_mode(modes_objects_list, 2);
            }
        }
	}
}

function show_current_mode(modes_objects_list, mode) {
    console.log("SHOW");
    modes_objects_list.forEach(element => {
        element.style.display = 'none';
    });
    modes_objects_list[mode].style.display = 'block';
}

function getRGB(str){
    var match = str.match(/rgba?\((\d{1,3}), ?(\d{1,3}), ?(\d{1,3})\)?(?:, ?(\d(?:\.\d?))\))?/);
    return match ? {
        red: match[1],
        green: match[2],
        blue: match[3]
    } : {};
}

