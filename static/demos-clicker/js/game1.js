class Game1 {
    constructor(player) {
        this.player = player;
        this.clicks = 10;
        $("#timer").text(this.clicks);
    }

    randomRectangle() {
        const margin = 1;
        const maxwidth = 12;
        const maxheight = 12;
        var x = margin + Math.random()*(100-margin*2-maxwidth);
        var y = margin + Math.random()*(100-margin*2-maxheight);
        var width = 3+Math.random()*maxwidth;
        var height = 3+Math.random()*maxheight;
        $("#rectangle").css("width", width+"%");
        $("#rectangle").css("height", height+"%");
        $("#rectangle").css("top", x+"%");
        $("#rectangle").css("left", y+"%");
    }

    updateClicks() {
        $.ajax({
            url: 'http://localhost:8080/player/'+this.player,
            dataType: 'json',
            contentType: 'application/json',
            type: 'GET',
            crossDomain: true,
            success: this.setClicks
        });
    }

    setClicks(data) {
        document.title = data['name'] + " -> " + data['clicks'] + " v0.1";
        $("#player").text(data['name']);
        $("#clicks").text(data['clicks']);
    }

    click() {
        this.clicks -= 1;
        if(this.clicks==0) {
            this.clicks = 10;
            this.addClicks(10);
            this.randomRectangle();
        }
        $("#timer").text(this.clicks);
    }

    addClicks(n) {
        var data = JSON.stringify({"clicks" : n });
        $.ajax({
            url: 'http://localhost:8080/addclicks/'+this.player,
            dataType: 'json',
            contentType: 'application/json',
            type: 'POST',
            data: data,
            crossDomain: true,
            success: this.setClicks
        });
    }
}
