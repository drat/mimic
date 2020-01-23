function log(texttolog) {
    var d = new Date();
    var time = padLeft(d.getHours(), 2) + ":" + padLeft(d.getMinutes(), 2) + ":" + padLeft(d.getSeconds(), 2) + ":" + padLeft(d.getMilliseconds(), 3);
    $('#status').text(texttolog);
    $('#logging_box').append(time + ": " + texttolog + "<br>");
}
function padLeft(nr, n, str) {
    return Array(n - String(nr).length + 1).join(str || '0') + nr;
}
function imgError(image) {
    image.onerror = "";
    image.src = "noimage.png";
    return true;
}

var bs_header = ''; //'<div class=\"container\"><div class=\"row\">';
var bs_footer = ''; //'</div></div>';

/*
   Presence Dashboard Example for the Skype Web SDK
*/

function init_skype(){
    log("App Loaded");

    var Application;
    var client;

    Skype.initialize({
        apiKey: 'a42fcebd-5b43-4b89-a065-74450fb91255',// 'SWX-BUILD-SDK',
        apiKeyCC: '9c967f6b-a846-4df2-b43d-5167e47d81e1'
    }, function (api) {
        Application = api.application;
        client = new Application();
    }, function (err) {
        log('some error occurred: ' + err);
    });

    log("Client Created");

    $('#everyone').hide();
    $('#searchagain').hide();

    $('#searchagain').click(function () {
        var pSearch;
        log('Search Again Clicked');
        pSearch = client.personsAndGroupsManager.createPersonSearchQuery();
        log('Searching for ' + $('#query').text());
        pSearch.text.set($('#query').text());
        pSearch.limit.set(100);
        pSearch.getMore().then(function (results) {
            log('Processing search results (2)...');
            //console.log('Search person results', results);

            // display all found contacts
            results.forEach(function (r) {
                var tag = $('<p>').text(r.result.displayName());
                $('#results').append(tag);
            });
            log('Finished');

        })
    });

    $('#everyone').click(function () {
        log('Everyone Clicked');

        var thestatus = '';
        var destination = '';

        client.personsAndGroupsManager.all.persons.get().then(function (persons) {
            // `persons` is an array, so we can use Array::forEach here
            log('Found Collection');
            $('#dashboardtiles').append(bs_header);

            persons.forEach(function (person) {
                // the `name` may not be loaded at the moment
                person.displayName.get().then(function (name) {

                    // now subscribe to the status change of everyone - so that we can see who goes offline/away/busy/online etc.
                    person.status.changed(function (status) {
                        $("#updatelabel").val(name + ' is now ' + status);

                        var d = new Date();
                        var curr_hour = d.getHours();
                        var curr_min = d.getMinutes();
                        var curr_sec = d.getSeconds();

                        var new_presence_state = '';
                        if (status == 'Online') {
                            new_presence_state = 'alert alert-success';
                        }
                        else if (status == 'Away') {
                            new_presence_state = 'alert alert-warning';
                        }
                        else if (status == 'Busy') {
                            new_presence_state = 'alert alert-danger';
                        }
                        else {
                            if ($('#showoffline').is(":checked")) {
                                new_presence_state = 'alert alert-info';
                            }
                        }
                        if (new_presence_state != '') {
                            var name_id = name.replace(/[^a-z0-9]/gi, '');
                            $('#status' + name_id).attr('class', new_presence_state);
                        }
                    });
                    person.status.subscribe();

                    // if the name is their email address, drop the domain component so that it's a little more readable
                    var name_shortened = name.split("@")[0];
                    var name_id = name.replace(/[^a-z0-9]/gi, '');

                    var tag = $('<p>').text(name);

                    person.status.get().then(function (status) {

                        //select a bootstrap helper style that reasonably approximates the Skype presence colours.
                        var presence_state = '';
                        if (status == 'Online') {
                            presence_state = 'alert alert-success';
                            destination = 'contact_online';
                        }
                        else if (status == 'Away') {
                            presence_state = 'alert alert-warning';
                            destination = 'contact_away';
                        }
                        else if (status == 'Busy') {
                            presence_state = 'alert alert-danger';
                            destination = 'contact_busy';
                        }
                        else {
                            if ($('#showoffline').is(":checked")) {
                                presence_state = 'alert alert-info';
                                destination = 'contact_offline';
                            }
                        }
                        // if a presence has been determined, display the user.
                        if (presence_state != '') {
                            //$('#dashboardtiles').append("<div class=\"col-md-3 \" id=\"" + name + "\"><p class=\"" + presence_state + "\">" + name_shortened + " (" + status + ")</p></div>");

                            //now get their Photo/Avatar URL
                            person.avatarUrl.get().then(function (url) {
                                //successfully received an avatar/photo
                                $('#dashboardtiles').append("<div class=\"col-sm-3 \" id=\"" + name + "\"><p id=\"status" + name_id + "\" class=\"" + presence_state + "\"><img hspace=5 src=\"" + url + "\" width=32  onError=\"this.onerror=null;this.src='noimage.png';\" />" + name_shortened + "</p></div>");
                            }).then(null, function (error) {
                                // display the user with the generic user image
                                $('#dashboardtiles').append("<div class=\"col-sm-3 \" id=\"" + name + "\"><p id=\"status" + name_id + "\" class=\"" + presence_state + "\">" + name_shortened + "</p></div>");
                            });
                        }
                    });
                });
            });

            $('#dashboardtiles').append(bs_footer);


        }).then(null, function (error) {
            // if either of the operations above fails, tell the user about the problem
            //console.error(error);
            log(error || 'Something went wrong.');
        });

        log('Finished');
    });

    // when the user clicks the "Sign In" button
    $('#signin').click(function () {
        //$('#signin').hide();

        // create an instance of Client
        var pSearch;

        log('Signing in...');

        console.log("Client:",client);

        // and invoke its  "signIn" method
        client.signInManager.signIn({
            username: $('#address').text(),
            password: $('#password').val(),
            cors: true
        }).then(function () {
            log('Logged In Succesfully');
            console.log("signed in as", client.personsAndGroupsManager.mePerson.displayName());
            $('#everyone').show();
            $('#loginbox').hide();
            //$('#searchagain').show();
        }).then(null, function (error) {

            console.log($('#address').text(),$('#password').val(),'unable to signin')

            // if either of the operations above fails, tell the user about the problem
            //console.error(error);
            log('Oops, Something went wrong: '+ error);
            $('#loginbox').show()
        });
    });
}
