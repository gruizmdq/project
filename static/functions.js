function readURL(input, id) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        console.log(input, id)
        
        reader.onload = function (e) {
            $(id).attr('src', e.target.result);
        }
        
        reader.readAsDataURL(input.files[0]);
    }
}


$("#description").keyup(function(){
    $('#description-helper').removeClass('text-red')
    len = $(this).val().length
    $('#description-helper').text(len + "/300");
    if (len == 300){
        $('#description-helper').addClass("text-red");
    }
})
$("#description-edit").keyup(function(){
    $('#description-helper-edit').removeClass('text-red')
    len = $(this).val().length
    $('#description-helper-edit').text(len + "/300");
    if (len == 300){
        $('#description-helper-edit').addClass("text-red");
    }
})
$(document).on('click', '.item-editar', function(){
    var tr = $(this).closest('tr')
    var id = tr.attr('data-id')
    var index = tr.children('.index').text()
    var description = tr.children('.description').text()

    $("#description-edit").val(description)
    $("#id-edit").val(id)
})


/********************
 *  DRAG AND DROP
 * 
 *******************/
var dragSrcEl = null;

function handleDragStart(e) {
    this.style.opacity = '0.4';  // this / e.target is the source node.

    dragSrcEl = this;

    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/html', this.innerHTML);
}
 

function handleDragOver(e) {
    if (e.preventDefault) {
      e.preventDefault(); // Necessary. Allows us to drop.
    }
  
    e.dataTransfer.dropEffect = 'move';  // See the section on the DataTransfer object.
  
    return false;
}

function handleDragEnter(e) {
    // this / e.target is the current hover target.
    this.classList.add('border-top');
}

function handleDragLeave(e) {
    this.classList.remove('border-top');  // this / e.target is previous target element.

}

function handleDrop(e) {
    // this/e.target is current target element.
  
    if (e.stopPropagation) {
      e.stopPropagation(); // Stops some browsers from redirecting.
    }
  
    // Don't do anything if dropping the same column we're dragging.
    if (dragSrcEl != this) {
        // Set the source column's HTML to the HTML of the columnwe dropped on.
        //dragSrcEl.innerHTML = this.innerHTML
        //this.innerHTML = e.dataTransfer.getData('text/html')
        var aux = $(dragSrcEl)

        $(dragSrcEl).remove()
        aux.insertBefore($(this))

        //change position text
        /*aux = $(dragSrcEl).children('th')[0].textContent
        $(dragSrcEl).children('th')[0].textContent = $(this).children('th')[0].textContent
        $(this).children('th')[0].textContent = aux

        aux = $(dragSrcEl).attr('data-id')
        $(dragSrcEl).attr('data-id',$(this).attr('data-id'))
        $(this).attr('data-id', aux)
*/

    }
  
    return false;
}
  
function handleDragEnd(e) {
    // this/e.target is the source node.
    this.style.opacity = '1';  

    [].forEach.call(rows, function (row) {
        row.classList.remove('border-top');
    });
    change_indexes()
}
var rows
function make_dragables(){
    rows = document.querySelectorAll('#table .table-row');
    [].forEach.call(rows, function(row) {
    row.addEventListener('dragstart', handleDragStart, false);
    row.addEventListener('dragend', handleDragEnd, false);
    row.addEventListener('dragenter', handleDragEnter, false);
    row.addEventListener('dragover', handleDragOver, false);
    row.addEventListener('dragleave', handleDragLeave, false);
    row.addEventListener('drop', handleDrop, false);
    row.addEventListener('dragend', handleDragEnd, false);
});
}

/******************************** */
/******** POST RESPONSE*********** */
/******************************** */
function edit_item_row(data){
    var tr = $("tbody").find("[data-id="+data['id']+"]")
    tr.children('.description').text(data['description'])
    //To do what happend whit image
}

function delete_item_row(data){
    var tr = $("tbody").find("[data-id="+data+"]")
    tr.fadeOut(1000, function() { 
        $(this).remove(); 
        $("#counter span").text($('#table tbody tr').length)
        $("#table tbody tr th").each(function(index) {
            $(this).text(index+1);
        })
    })
}


var id_alert = 0

function notification(html, id){
    $("#alert-div").append(html)                    
    setTimeout(function(){
        $("#"+id+".alert").first().fadeOut(1000, function() { $(this).remove(); });
    }, 2000);
}
function onPostSuccessDelete(){
    var id = id_alert++    

    var html = success_alert(id, ['¡Perfecto!', 'La imagen se borró con éxito.'])
    notification(html, id)
}

function onPostSuccessInsert(data){
    var id = id_alert++
    var html
    if (data === '3'){
        html = warning_alert(id, ['Hubo un error', 'La imagen que intenta subir ya existe.'])
    }
    else if (data === '2'){
        html = danger_alert(id, ['ERROR', 'Las dimensiones deben ser 320px x 320px'] )
    }
    else if (data === '1'){
        html = danger_alert(id, ['ERROR', 'La extensión del archivo no es soportada.'] )
    }
    else{
        html = success_alert(id, ['¡Perfecto!', 'La imagen se agregó al final de la tabla.'])        
    }

    notification(html, id)
}


function onPostSuccessEdit(data){
    var id = id_alert++
    var html
    
    $('#edit-modal').modal('hide')
    if (data === '3'){
        html = warning_alert(id, ['Hubo un error', 'La imagen que intenta subir ya existe.'])
    }
    else if (data === '2'){
        html = danger_alert(id, ['ERROR', 'Las dimensiones deben ser 320px x 320px'] )
    }
    else if (data === '1'){
        html = danger_alert(id, ['ERROR', 'La extensión del archivo no es soportada.'] )
    }
    else
        html = success_alert(id, ['¡Perfecto!', 'La imagen se editó con éxito.'])
    
    notification(html, id)

}

function warning_alert(id, arr){
    html = '<div id="'+id+'" class="alert alert-warning alert-dismissible fade show" role="alert">'
    html += '<strong>'+ arr[0]+'.</strong> '+ arr[1]+'.'
    html += '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>'
    return html
}

function danger_alert(id, arr){
    html = '<div id="'+id+'" class="alert alert-danger alert-dismissible fade show" role="alert">'
    html += '<strong>'+ arr[0]+'.</strong> '+ arr[1]+'.'
    html += '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>'
    return html
}

function success_alert(id, arr){
    html = '<div id="'+id+'" class="alert alert-success alert-dismissible fade show" role="alert">'
    html += '<strong>'+ arr[0]+'.</strong> '+ arr[1]+'.'
    html += '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>'
    return html
}


var id_image = 0
function add_item_row(data, load_image){
    html = '<tr data-id="'+ data.id+'" class="table-row" draggable=true>'
    html += '<th scope="row" class="index">'+(parseInt($('#table tbody tr').length)+1)+'</th>'
    html += '<td><img id="image-'+id_image+'" alt="" draggable="false"></td>'
    html += '<td class="description">'+ data.description+'</td>'
    html += '<td><ul class="item-ul"><li class="pr-1 item-editar"><i class="far fa-edit"></i></li><li><i class="far fa-trash-alt item-borrar"></i></li></ul></td> </tr>'

    $('#table tbody').append(html)
    var id = "#image-"+id_image

    if (load_image == true)
        readURL($("#image-upload")[0], id)
    else
        $(id).attr('src', data.file_path);
    id_image += 1

    make_dragables()
}
