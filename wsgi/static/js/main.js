$('#porform-btnadd').on('click', function () {
   alert('Got into the add button')
    $('#portfolio_id').val('');
    $('#title').val('');
    $('#description').val('');
    $('#tags').tagsinput('removeAll');
    $('#porto_form').modal('show');
    return false;
});

function editPortfolioForm(id) {
    $('#portofolio_id').val();
    $.getJSON('/get_portoflio/' + id, {})
        .then(function (data) {
            $('#portofolio_id').val(data.id);
            $('#title').val(data.title);
            $('#description').val(data.description);
            $('#tags').tagsinput('removeAll');
            $('#tags').tagsinput('add', data.tags);
            $('#porto_form').modal('show');
        }).error(function (data, textstatus, xhr) {
        alert(data, textstatus, xhr)
    })
}


$('#portform_btnsave').on('click', function () {
    alert("This is the amazing side of it all");
    $.post("{{ url_for('/portfolio_add_update')}}", $('#portform').serialize(), function (data, textStatus) {
        debugger;
        var errors = $.parseJSON(data);
        $('#description_errors').text('');
        $('#title_errors').text('');
        $('#tags_errors').text('');
        if(errors.iserror){
            if(errors.title != undefined){$('#title_errors').text(errors.title[0])}
            if(errors.description != undefined){$('#description_errors').text(errors.description[0])}
            if(errors.tags != undefined){$('#tags_errors').text(errors.tags[0])}
        }else if(errors.savedsuccess){
            $('#porto_form').modal('hide');
            location.reload();
        }
    })
});
