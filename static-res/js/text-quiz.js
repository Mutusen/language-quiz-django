score = 0;
questions = 0;
choices = 0;
difficult = 0;

function check_answer() {
    if ($(this).attr('data-answer') == $('#text-sample').attr('lang')) {
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
    $('button.answer[data-answer=' + $('#text-sample').attr('lang') + ']').addClass('btn-success');
    $('#source a').show();
    $('#source span').hide();
    $('button.answer').prop('disabled', true);
    $('#your-answer').text($(this).text());
    $('#after-answer').show();
};

function next_button() {
    $.ajax({
        url: $(this).attr('data-url'),
        data: {
            number: $('#current-question').text(),
            score: score,
            questions: questions,
            choices: choices,
            difficult: difficult,
            past_texts: $('#past-texts').val(),
            correct: $('#correct-answer').is(':visible')
        },
        method: "POST",
        dataType: "html",
        success: function(data) {
            $('#text-quiz').html(data);
            setup();
        }
    });
};

function setup() {
    $('#text-quiz .d-none').hide().removeClass('d-none');
    $('button.answer').click(check_answer);
    $('#next').click(next_button);
}

$('#start').click(function(){
    questions = $('#questions').val();
    choices = $('#choices').val();
    difficult = $('#difficult').is(':checked') ? 1 : 0;
    $.ajax({
        url: $(this).attr('data-url'),
        data: {
            number: 0,
            score: 0,
            questions: questions,
            choices: choices,
            difficult: difficult,
            past_texts: "",
        },
        method: "POST",
        dataType: "html",
        success: function(data) {
            $('#text-quiz').html(data);
            setup();
        }
    });
});