function updateText(newCount) {
    $('.count-clap').text(newCount)
}
$('.clap-btn').click(function(e) {
    e.preventDefault()
    var this_ = $(this)
    var clapUrl = this_.attr('data-href')
    var previous_count = parseInt(this_.attr('data-claps')) | 0
    var previous_count = parseInt($('.count-clap').text());
    // var previous_count = parseInt(this_.attr('data-claps')) | 0
    // console.log("previous_count " + previous_count)
    $.ajax({
        url: clapUrl,
        method: 'GET',
        data: {},
        success: function(data) {
            console.log(data)
            var claps;
            if (data.liked) {
                claps = previous_count > 0 ? previous_count - 1 : 0
                console.log("data.liked claps=" + claps)
                updateText(claps)
                this_.html('<img class="ml-1" src="{% static 'blog/img/clapping.svg' %}" width="25" height="25">')
            } else {
                claps = previous_count + 1
                console.log("data.unliked claps=" + claps)
                updateText(claps)
                this_.html('<img class="ml-1" src="{% static 'blog/img/clapping_filled.svg' %}" width="25" height="25">')
            }
        },
        error: function(error) {
            console.log(error)
            console.log('error')
        }
    })
})
