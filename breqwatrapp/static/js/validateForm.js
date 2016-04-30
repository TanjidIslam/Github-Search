/**
 * Created by Tanjid Islam on 30/04/2016.
 */
$(document).ready(function() {
    $('#advancedSearch').formValidation({
        framework: 'bootstrap',
        icon: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            username: {
                validators: {
                    notEmpty: {
                        message: 'No Username is entered'
                    }
                }
            },
            number: {
                validators: {
                    integer: {
                        message: 'The value is not a Number'
                    }
                }
            },
            keywords: {
                validators: {
                    notEmpty: {
                        message: 'Must submit with a keyword'
                    }
                }
            }
        }
    });
});