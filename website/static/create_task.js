$(window).on('beforeunload', function() {
    return "";
});
$('form').submit(function () {
    console.log("hahahahhahaha");
    $(window).unbind('beforeunload');
});

function create_task_delete_item(item_id){
    var li = document.getElementById("item_" + item_id).parentNode.parentNode;
    var sec_id = Number(item_id.split('_')[1]);
    var fir_id = item_id.split('_')[0];
    var ul = li.parentNode;
    ul.removeChild(li);
    for (var i = sec_id; i <= ul.children.length; ++i){
        //input id
        document.getElementById("item_" + fir_id + "_" + (i+1)).id = "item_" + fir_id + "_" + i;
        //button id
        document.getElementById(fir_id + "_" + (i + 1)).id = fir_id + "_" + i;
    }
    if (ul.children.length == 0){
        create_task_delete_subtask(Number(fir_id));
    }
}

function create_task_delete_subtask(subtask_id){
    var li = document.getElementById("subtask_"+subtask_id).parentNode;
    var ul = li.parentNode;
    var lis = ul.children;
    ul.removeChild(li);
    for (var i = subtask_id; i < lis.length; ++i){
        var subtask_li = document.getElementById("subtask_"+(i+1)).parentNode;
        //input id
        document.getElementById("subtask_"+(i+1)).id = "subtask_"+i;
        //button id
        document.getElementById((i+1)).id = i;

        var items_ul = subtask_li.children[1];
        var count_items = items_ul.children.length;
        for (var j = 1; j <= count_items; ++j){
            document.getElementById("item_"+(i+1)+"_"+j).id = "item_"+i+"_"+j;
            document.getElementById((i+1)+"_"+j).id = i+"_"+j;
        }
    }
}

function create_task_new_item(subtask_id){
    var ul = document.getElementById("item_" + subtask_id + "_" + "1").parentNode.parentNode.parentNode;
    console.log(ul);
    var items_count = ul.children.length;
    var item_id = subtask_id + "_" + (items_count+1);

    var item_li = document.createElement("li");
    item_li.setAttribute("class", "create-task-item");
    var item_div = document.createElement("div");
    item_div.setAttribute("class", "create-task-item-text");
    var item_input = document.createElement("input");
    item_input.type = "text";
    item_input.id = "item_" + item_id;
    item_input.name = item_input.id;
    item_input.value = "Item";
    var item_button = document.createElement("button");
    item_button.type = "button";
    item_button.id = item_id;
    item_button.setAttribute("class", "create-task-item-delete");
    item_button.setAttribute("onclick", "create_task_delete_item(this.id)");
    var item_button_span = document.createElement("span");
    item_button_span.setAttribute("aria-hidden", "true")
    item_button_span.innerHTML = "&times;";

    item_button.appendChild(item_button_span);
    item_div.appendChild(item_input);
    item_div.appendChild(item_button);
    item_li.appendChild(item_div);
    ul.appendChild(item_li);
}


function create_task_new_subtask(){
    var ul = document.getElementById("subtasks_list");
    var subtask_id = ul.children.length;
    var item_id = subtask_id + "_1";
    console.log(subtask_id);
    var subtask_li = document.createElement("li");
    subtask_li.setAttribute("class", "create-task-subtask");
    var subtask_input = document.createElement("input");
    subtask_input.type = "text";
    subtask_input.name = "subtask_" + subtask_id;
    subtask_input.id = subtask_input.name;
    subtask_input.placeholder = "Subtask";
    var subtask_ul = document.createElement("ul");
    subtask_ul.setAttribute("class", "list list-group-flush");
    var item_li = document.createElement("li");
    item_li.setAttribute("class", "create-task-item");
    var item_div = document.createElement("div");
    item_div.setAttribute("class", "create-task-item-text");
    var item_input = document.createElement("input");
    item_input.type = "text";
    item_input.id = "item_" + item_id;
    item_input.name = item_input.id;
    item_input.value = "Item";
    var item_button = document.createElement("button");
    item_button.type = "button";
    item_button.id = item_id;
    item_button.setAttribute("class", "create-task-item-delete");
    item_button.setAttribute("onclick", "create_task_delete_item(this.id)");
    var item_button_span = document.createElement("span");
    item_button_span.setAttribute("aria-hidden", "true")
    item_button_span.innerHTML = "&times;";
    var subtask_button_div = document.createElement("div");
    subtask_button_div.align = "center";
    var subtask_button = document.createElement("button");
    subtask_button.type = "button";
    subtask_button.id = subtask_id + "";
    subtask_button.setAttribute("class", "btn btn-primary new-item-btn");
    subtask_button.setAttribute("onclick", "create_task_new_item(this.id)");
    subtask_button.innerHTML = "New Item";

    item_button.appendChild(item_button_span);
    item_div.appendChild(item_input);
    item_div.appendChild(item_button);
    item_li.appendChild(item_div);
    subtask_ul.appendChild(item_li);
    subtask_button_div.appendChild(subtask_button);
    subtask_li.appendChild(subtask_input);
    subtask_li.appendChild(subtask_ul);
    subtask_li.appendChild(subtask_button_div);
    ul.insertBefore(subtask_li, ul.children[subtask_id - 1])
}