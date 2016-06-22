$('#porform-btnadd').on('click', function () {
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
            $('#portofolio_id').val();
            $('#title').val(data.title);
            $('#description').val(data.description);
            $('#tags').tagsinput('removeAll');
            $('#tags').tagsinput('add', data.tags);
            $('#porto_form').modal('show');
        }).error(function (data, textstatus, xhr) {
        alert(data, textstatus, xhr)
    })
}

$('#portform_btnsave').click(function () {
    console.log('This is the portform button');
    console.log($('#portform').serialize());
    $.post("/portfolio_add_update", $('#portform').serialize(), function (data, textStatus) {
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
