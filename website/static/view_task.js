async function toggle_item(button_id){
    var item_id = button_id.split('_')[1];
    var checkbox = document.getElementById('btn-check-'+item_id);
    var res = await fetch('/toggle-item', {
        method: 'POST',
        body: JSON.stringify({itemId: item_id})
    });
    res = await res.json();
    var item_done = res.item_done;
    var subtask_done = res.subtask_done;
    var subtask_progress = res.subtask_progress;
    var item_li = document.getElementById('item_'+item_id);
    var subtask_li = item_li.parentNode.parentNode;
    var item_classes = item_li.classList;
    item_classes.remove('item-item-done');
    if (item_done){
        item_classes.add('item-item-done');
    }
    var subtask_classes = subtask_li.classList;
    subtask_classes.remove('subtask-item-done', 'subtask-item-progress');
    if (subtask_done){
        subtask_classes.add('subtask-item-done');
    }
    else if (subtask_progress){
        subtask_classes.add('subtask-item-progress');
    }
    checkbox.checked = item_done;
}

async function update_colors(item_id, change){
    var item_res = await fetch('/get-item-done/'+item_id);
    var subtask_res = await fetch('/get-subtask-done/'+item_id);
    item_res = await item_res.json()
    
    subtask_res = await subtask_res.json();
    
    
}