$('select.drop-select').each(function () {
    new Select({
        el: this,
        selectLikeAlignment: $(this).attr('data-select-like-alignement') || 'auto',
        className: 'select-theme-dark'
    });
});
