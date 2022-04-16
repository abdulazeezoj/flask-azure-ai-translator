$(document).ready(function () {
    let key_timer = 0;  // keypress timer

    $("#src-text").keypress(function (e) {
        // clear timer if available
        if (key_timer) {
            clearTimeout(key_timer);
        }

        // set timer to wait for user to stop typing
        key_timer = setTimeout(translate, 500);
    });

    $("#trans-lang").change(translate);


    function translate() {
        let src_text = $("#src-text").val();
        let src_lang = $("#src-lang").val();
        let trans_lang = $("#trans-lang").val();

        var server_data = {
            'src-text': src_text,
            'src-lang': src_lang,
            'trans-lang': trans_lang
        };

        $.ajax({
            url: "/translate",
            type: "POST",
            data: JSON.stringify(server_data),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function render(result) {
                $("#trans-text").val(result['trans_text']);
                $("#src-lang option").each(function () {
                    if ($(this).val() == result['src_lang']) {
                        $(this).attr("selected", "selected");
                    }
                });

                // for debug
                // console.log(result)
            }
        });
    }
});