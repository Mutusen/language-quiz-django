score = 0;
questions = 0;
choices = 0;
hide = 0;
difficult = 0;

function check_answer() {
    if ($(this).attr('data-answer') == $('#song-language').val()) {
        $('#correct-answer').show();
        $('#wrong-answer').hide();
        $('#after-answer-alert').addClass('alert-success');
        score++;
    }
    else {
        $(this).addClass('btn-danger');
        $('#correct-answer').hide();
        $('#wrong-answer').show();
        $('#after-answer-alert').addClass('alert-danger');
    }
    $('#hide-video').remove();
    $('button.answer[data-answer=' + $('#song-language').val() + ']').addClass('btn-success');
    $('button.answer').prop('disabled', true);
    $('#your-answer').text($(this).text());
    $('#after-answer').show();
    $([document.documentElement, document.body]).animate({
        scrollTop: $("#after-answer").offset().top
    }, 200);
};

function next_button() {
    $.ajax({
        url: $(this).attr('data-url'),
        data: {
            number: $('#current-question').text(),
            score: score,
            questions: questions,
            choices: choices,
            hide: hide,
            difficult: difficult,
            past_songs: $('#past-songs').val(),
            correct: $('#correct-answer').is(':visible')
        },
        method: "POST",
        dataType: "html",
        success: function(data) {
            $('#song-quiz').html(data);
            setup();
        }
    });
};

function setup() {
    $('#song-quiz .d-none').hide().removeClass('d-none');
    $('button.answer').click(check_answer);
    $('#next').click(next_button);
    $('#hide-video button').click(function(){
        $('#hide-video').remove();
    });
}

$('#start').click(function(){
    questions = $('#questions').val();
    choices = $('#choices').val();
    hide = $('#hide').is(':checked') ? 1 : 0;
    difficult = $('#difficult').is(':checked') ? 1 : 0;
    $.ajax({
        url: $(this).attr('data-url'),
        data: {
            number: 0,
            score: 0,
            questions: questions,
            choices: choices,
            hide: hide,
            difficult: difficult,
            past_songs: "",
        },
        method: "POST",
        dataType: "html",
        success: function(data) {
            $('#song-quiz').html(data);
            setup();
        }
    });
});