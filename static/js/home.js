/*
 * JavaScript file for the application to demonstrate
 * using the API
 */

// Create the namespace instance
let ns = {};

// Create the model instance
ns.model = (function () {
    'use strict';

    let $event_pump = $('body');

    // Return the API
    return {
        'read': function () {
            let ajax_options = {
                type: 'GET',
                url: 'api/milestones',
                accepts: 'application/json',
                dataType: 'json',
            };
            $.ajax(ajax_options)
                .done(function (data) {
                    $event_pump.trigger('model_read_success', [data]);
                })
                .fail(function (xhr, textStatus, errorThrown) {
                    $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
                });
        },
        create: function (name, city, description) {
            let ajax_options = {
                type: 'POST',
                url: 'api/milestones',
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify({
                    name: name,
                    city: city,
                    description: description
                }),
            };
            $.ajax(ajax_options)
                .done(function (data) {
                    $event_pump.trigger('model_create_success', [data]);
                })
                .fail(function (xhr, textStatus, errorThrown) {
                    $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
                });
        },
        update: function (name, city, description) {
            let ajax_options = {
                type: 'PUT',
                url: 'api/milestones/' + name,
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify({
                    'name': name,
                    'city': city,
                    'description': description
                }),
            };
            $.ajax(ajax_options)
                .done(function (data) {
                    $event_pump.trigger('model_update_success', [data]);
                })
                .fail(function (xhr, textStatus, errorThrown) {
                    $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
                });
        },
        'delete': function (name) {
            let ajax_options = {
                type: 'DELETE',
                url: 'api/milestones/' + name,
                accepts: 'application/json',
                contentType: 'plain/text',
            };
            $.ajax(ajax_options)
                .done(function (data) {
                    $event_pump.trigger('model_delete_success', [data]);
                })
                .fail(function (xhr, textStatus, errorThrown) {
                    $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
                });
        },
    };
})();

// Create the view instance
ns.view = (function () {
    'use strict';

    let $name = $('#name'),
        $city = $('#city'),
        $description = $('#description');

    // return the API
    return {
        reset: function () {
            $name.val('').focus();
            $city.val('');
            $description.val('');
        },
        update_editor: function (name, city, description) {
            $name.val(name).focus();
            $city.val(city);
            $description.val(description);
        },
        build_table: function (milestones) {
            let rows = '';

            // clear the table
            $('.milestones table > tbody').empty();

            // did we get a milestones array?
            if (milestones) {
                for (let i = 0, l = milestones.length; i < l; i++) {
                    rows += `<tr><td class="name">${milestones[i].name}</td><td class="city">${milestones[i].city}</td><td class="description">${milestones[i].description}</td><td>${milestones[i].timestamp}</td></tr>`;
                }
                $('table > tbody').append(rows);
            }
        },
        error: function (error_msg) {
            $('.error').text(error_msg).css('visibility', 'visible');
            setTimeout(function () {
                $('.error').css('visibility', 'hidden');
            }, 3000);
        },
    };
})();

// Create the controller
ns.controller = (function (m, v) {
    'use strict';

    let model = m,
        view = v,
        $event_pump = $('body'),
        $name = $('#name'),
        $city = $('#city'),
        $description = $('#description');

    // Get the data from the model after the controller is done initializing
    setTimeout(function () {
        model.read();
    }, 100);

    // Validate input
    function validate(name, city, description) {
        return name !== '' && city !== '' && description !== '';
    }

    // Create our event handlers
    $('#create').click(function (e) {
        let name = $name.val(),
            city = $city.val(),
            description = $description.val();

        e.preventDefault();

        if (validate(name, city, description)) {
            model.create(name, city, description)
        } else {
            alert('Problem with first or last name input');
        }
    });

    $('#update').click(function (e) {
        let name = $name.val(),
            city = $city.val(),
            description = $description.val();

        e.preventDefault();

        if (validate(name, city, description)) {
            model.update(name, city, description)
        } else {
            alert('Problem with first or last name input');
        }
        e.preventDefault();
    });

    $('#delete').click(function (e) {
        let name = $name.val();

        e.preventDefault();

        if (validate('placeholder', name)) {
            model.delete(name)
        } else {
            alert('Problem with first or last name input');
        }
        e.preventDefault();
    });

    $('#reset').click(function () {
        view.reset();
    });

    $('table > tbody').on('dblclick', 'tr', function (e) {
        let $target = $(e.target),
            name,
            city,
            description;

        name = $target.parent().find('td.name').text();

        city = $target.parent().find('td.city').text();

        description = $target.parent().find('td.description').text();

        view.update_editor(name, city, description);
    });

    // Handle the model events
    $event_pump.on('model_read_success', function (e, data) {
        view.build_table(data);
        view.reset();
    });

    $event_pump.on('model_create_success', function (e, data) {
        model.read();
    });

    $event_pump.on('model_update_success', function (e, data) {
        model.read();
    });

    $event_pump.on('model_delete_success', function (e, data) {
        model.read();
    });

    $event_pump.on('model_error', function (e, xhr, textStatus, errorThrown) {
        let error_msg =
            textStatus + ': ' + errorThrown + ' - ' + xhr.responseJSON.detail;
        view.error(error_msg);
        console.log(error_msg);
    });
})(ns.model, ns.view);
