$(document).ready(function () {

    RefreshQuote($('#getNewQuote'));
    $('#getNewQuote').click(function () {
        RefreshQuote(this);
    });
    function getNewBackgroundColor() {
        const color = '#' + Math.random().toString(16).substr(-6);
        return color;
    }

    function RefreshQuote(that) {
        var btn = $(that);
        btn.find('.text').text('Get New quote');
        btn.prop('disabled', true);
        btn.find('.text').addClass('d-none');
        btn.find('.spinner-border').removeClass('d-none');
        var gradient = JSON.parse(localStorage.getItem("gradient"));
        const source = '/Home/GetQuote?isGrayscale=' + gradient;
        $.getJSON(source)
            .done(function (newQuote) {
                if (!newQuote || newQuote.error) {
                    error(btn);
                } else {
                    $('#quoteText').html(newQuote.quoteText);
                    $('#quoteAuthor').html(newQuote.quoteAuthor);
                    $('html').css('--main-bg-color', getNewBackgroundColor());
                    //$('#quoteBox').css('background-image', `url(${newQuote.imageLink})`);
                    setBackground(newQuote.imageBase64String);
                }
            })
            .fail(function (jqXHR, textStatus, errorThrown) {
                console.error(`AJAX request failed: ${textStatus}, ${errorThrown}`);
                error(btn);
            })
            .always(function () {
                btn.prop('disabled', false);
                btn.find('.text').removeClass('d-none');
                btn.find('.spinner-border').addClass('d-none');
            });

    }

    function setBackground(base64String) {
        
        var dataUrl = "data:image/jpeg;base64," + base64String;
        $("#quoteBox").css("background-image", "url('" + dataUrl + "')");
    }
    function error(btn) {
        btn.find('.text').text('Refresh');
    }
    $("#settingsModel").on('show.bs.modal', function () {
        $("#gradient").prop('checked', JSON.parse(localStorage.getItem("gradient")));
    });

    $("#btnSave").on("click", function () {
        localStorage.setItem("gradient", $('#gradient').is(':checked'));
        $('#settingsModel').modal('hide');
        RefreshQuote($('#getNewQuote'));
    });



});