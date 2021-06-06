var subtasks = {};
var subtask_lis = document.getElementsByClassName('subtask-item');
var item_lis = document.getElementsByClassName('item-item');
for (var i = 0; i < subtask_lis.length; ++i){
    var items = {};
    for (var j = 0; j < item_lis.length; ++j){
        if (item_lis[j].parentNode.parentNode == subtask_lis[i]){
            items[item_lis[j].id] = document.getElementById('btn-check-'+item_lis[j].id.split('_')[1]).checked;
        }
    }
    subtasks[subtask_lis[i].id] = items;
}

function subtask_done(subtask_id){
    var subtask = subtasks[subtask_id];
    var res = true;
    for (var key in subtask){
        if (!subtask[key]){
            res = false;
            break;
        }
    }
    return res;
}

function subtask_progress(subtask_id){
    var subtask = subtasks[subtask_id];
    var res = false;
    for (var key in subtask){
        if (subtask[key]){
            res = true;
            break;
        }
    }
    return res;
}

function toggle_item(button_id){
    console.log(button_id);
    var subtask_id = document.getElementById(button_id).parentNode.parentNode.id;
    
    var item_id = button_id;
    subtasks[subtask_id][item_id] = !subtasks[subtask_id][item_id];

    var checkbox = document.getElementById('btn-check-'+item_id.split('_')[1]);
    
    var is_item_done = subtasks[subtask_id][item_id];
    var is_subtask_done = subtask_done(subtask_id);
    var is_subtask_progress = subtask_progress(subtask_id);
    var item_li = document.getElementById(item_id);
    var subtask_li = item_li.parentNode.parentNode;
    var item_classes = item_li.classList;
    item_classes.remove('item-item-done');
    if (is_item_done){
        item_classes.add('item-item-done');
    }
    var subtask_classes = subtask_li.classList;
    subtask_classes.remove('subtask-item-done', 'subtask-item-progress');
    if (is_subtask_done){
        subtask_classes.add('subtask-item-done');
    }
    else if (is_subtask_progress){
        subtask_classes.add('subtask-item-progress');
    }
    checkbox.checked = is_item_done;

    fetch('/toggle-item', {
        method: 'POST',
        body: JSON.stringify({itemId: item_id.split('_')[1]})
    });
}