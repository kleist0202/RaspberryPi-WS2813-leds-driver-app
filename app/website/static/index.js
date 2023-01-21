var color_set_div = document.getElementById('colors_set');
var color_sliders_div = document.getElementById('color-options');
var speed_sliders_div = document.getElementById('rainbow-options');
var speed_walker_div = document.getElementById('walker-options');
var snake_speed_div = document.getElementById('snake-options');

const modes_objects_dict = {
    1: color_set_div,
    2: color_sliders_div,
    3: speed_sliders_div,
    5: speed_walker_div,
    8: snake_speed_div,
}

$(document).ready(function() {
    var parentDOM = document.querySelector('#brightness-slider');
    var input_bright = parentDOM.querySelector('input[type=range]');

    input_bright.addEventListener("input", function() {
        change_color_square();
        let bright = parentDOM.querySelector('#display_brightness').innerHTML;
        input_bright.style.background = `rgb(${bright}, ${bright}, ${bright})`;
    });

    var parentDOMR = document.querySelector('#slider-r');
    var input_r = parentDOMR.querySelector('input[type=range]');

    input_r.addEventListener("input", function() {
        change_color_square();
        let r_value = parentDOMR.querySelector('#display_r').innerHTML;
        input_r.style.background = `rgb(${r_value}, 0, 0)`;
    });

    var parentDOMG = document.querySelector('#slider-g');
    var input_g = parentDOMG.querySelector('input[type=range]');

    input_g.addEventListener("input", function() {
        change_color_square();
        let g_value = parentDOMG.querySelector('#display_g').innerHTML;
        input_g.style.background = `rgb(0, ${g_value}, 0)`;
    });

    var parentDOMB = document.querySelector('#slider-b');
    var input_b = parentDOMB.querySelector('input[type=range]');

    input_b.addEventListener("input", function() {
        change_color_square();
        let b_value = parentDOMB.querySelector('#display_b').innerHTML;
        input_b.style.background = `rgb(0, 0, ${b_value})`;
    });

    let ele = document.getElementsByName('modes');
    ele[0].checked = true;

    let all_set_colors = document.getElementsByName('color');
    all_set_colors[0].checked = true;

    modeChanged();
              
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

    if (current_mode == 1) {
        var brightness = parseFloat(document.getElementById('display_brightness').innerHTML) / 100;
        c_r = parseInt(getRGB(got_color).red * brightness);
        c_g = parseInt(getRGB(got_color).green * brightness);
        c_b = parseInt(getRGB(got_color).blue * brightness);
    }
    if (current_mode == 2) {
        c_r = document.getElementById('display_r').innerHTML;
        c_g = document.getElementById('display_g').innerHTML;
        c_b = document.getElementById('display_b').innerHTML;
    }

    var snake_configs = document.getElementsByName('snake-config');
    var current_snake_config = "1";

	for(i = 0; i < snake_configs.length; i++) {
		if(snake_configs[i].checked) {
    	    current_snake_config = snake_configs[i].value;
        }
	}
    
    var rainbow_speed = document.getElementById('display_rainbow_speed').innerHTML;
    var walker_speed = document.getElementById('display_walker_speed').innerHTML;
    var snake_speed = document.getElementById('display_snake_speed').innerHTML;

    req.open('POST', '/', true);
    req.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    req.send(
        "color_r=" + c_r + "&" +
        "color_g=" + c_g + "&" +
        "color_b=" + c_b + "&" +
        "modes=" + current_mode + "&" +
        "rainbow_speed=" + rainbow_speed + "&" +
        "walker_speed=" + walker_speed + "&" +
        "snake_speed=" + snake_speed + "&" +
        "current_snake_config=" + current_snake_config
    );
}

function updateDoc() {
    var req = new XMLHttpRequest();

    var snake_configs = document.getElementsByName('snake-config');
    var current_snake_config = "1";

	for(i = 0; i < snake_configs.length; i++) {
		if(snake_configs[i].checked) {
    	    current_snake_config = snake_configs[i].value;
        }
	}

    var updated_snake_speed = document.getElementById('display_snake_speed').innerHTML;

    req.open('POST', '/', true);
    req.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    req.send(
        "updated_snake_speed=" + updated_snake_speed + "&" +
        "updated_snake_config=" + current_snake_config
    );
}

function turnLeftReq() {
    console.log("galoo");
    var req = new XMLHttpRequest();

    req.open('POST', '/', true);
    req.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    req.send(
        "turn_req=" + "1"
    );
}

function turnRightReq() {
    var req = new XMLHttpRequest();

    req.open('POST', '/', true);
    req.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    req.send(
        "turn_req=" + "2"
    );
}

function modeChanged() {
    show_current_mode(1);

    var mode_title = document.getElementById('mode-title');
    var ele = document.getElementsByName('modes');
	var current_mode = "1";
    var current_label = null;
              
	for(i = 0; i < ele.length; i++) {
		if(ele[i].checked) {
    	    current_mode = ele[i].value;
            show_current_mode(current_mode);
            current_label = ele[i];
        }
	}
    mode_title.innerHTML = current_label.labels[0].textContent;
}

function show_current_mode(mode) {
    console.log("SHOW");
    //modes_objects_list.forEach(element => {
    //    element.style.display = 'none';
    //});
    //if (mode >= modes_objects_list.length)
    //    return;
    //modes_objects_list[mode].style.display = 'flex';

    Object.keys(modes_objects_dict).forEach(key => {
        modes_objects_dict[key].style.display = 'none';
    });
    if (!(mode in modes_objects_dict))
        return
    modes_objects_dict[mode].style.display = 'block';
}

function getRGB(str){
    if (str == null)
        return {red: 0, green: 0, blue: 0};
    var match = str.match(/rgba?\((\d{1,3}), ?(\d{1,3}), ?(\d{1,3})\)?(?:, ?(\d(?:\.\d?))\))?/);
    return match ? {
        red: match[1],
        green: match[2],
        blue: match[3]
    } : {red: 0, green: 0, blue: 0};
}
