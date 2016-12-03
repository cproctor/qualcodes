var artifact = function() {
    return {
        //"user_id": USER_ID, 
        //"column_id": COLUMN_ID,
        "codes": ARTIFACT_CODES
        //"text": TEXT
    }
}

var render = function() {
    d3.select('#codes').selectAll('button')
        .data(CODES)
        .enter()
            .append('button')

    d3.select('#codes').selectAll('button')
        .data(CODES)
                .text(function(d) { return d['name']})
                .classed('selected', function(d) { return _.contains(ARTIFACT_CODES, d.id)})
                .on('click', function(d) {
                    if (_.contains(ARTIFACT_CODES, d.id)) {
                        ARTIFACT_CODES = _.without(ARTIFACT_CODES, d.id)
                    } 
                    else {
                        ARTIFACT_CODES.push(d.id)
                    } 
                    d3.json(POST_URL)
                        .header("Content-Type","application/json")  
                        .send('PUT', JSON.stringify(artifact()), function(err, data) {
                            render()
                        })
                })
}

d3.select("#new-code-submit")
    .on('click', function() {
        var name = document.getElementById('new-code-name').value
        console.log(name)
        d3.json(NEW_CODE_URL)
            .header("Content-Type","application/json")  
            .send('POST', JSON.stringify({"name": name}), function(err, data) {
                CODES.push(data)
                document.getElementById('new-code-name').value = ""
                render()
            })
    }) 

render()


