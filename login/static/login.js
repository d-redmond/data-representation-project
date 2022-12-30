$(function() {
    if (localStorage.chkbx && localStorage.chkbx != '') {
        $('#username').val(localStorage.usrname);
        $('#password').val(localStorage.pass);
    } else {
        $('#username').val('');
        $('#password').val('');
    };
});

