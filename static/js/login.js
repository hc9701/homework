function setContentHeight() {
    var web_subnav = document.getElementById("login_bj");
    web_subnav.style.height = document.documentElement.clientHeight + 'px';
}

window.onload = setContentHeight;
window.onresize = setContentHeight;

$('select.drop-select').each(function () {
    new Select({
        el: this,
        selectLikeAlignment: $(this).attr('data-select-like-alignement') || 'auto',
        className: 'select-theme-dark'
    });
});