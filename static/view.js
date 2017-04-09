once = new Object()
function edit(id,value) {
    if ( typeof(once[id]) == "undefined") {
      document.getElementById(id).innerHTML='<td><input type="text" name=' + id + ' value=' + value + ' ></td>';
    }
    once[id] = id;
}
function text(id,value) {
    if ( typeof(once[id]) == "undefined") {
      document.getElementById(id).innerHTML='<td><textarea name=' + id + ' rows="3" cols="130">' + value + '</textarea></td>';
    }
    once[id] = id;
}

