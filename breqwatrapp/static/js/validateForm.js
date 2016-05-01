/**
 * Created by Tanjid Islam on 30/04/2016.
 */
$(document).ready(function () {
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
            follower: {
                validators: {
                    integer: {
                        message: 'The value is not a Number'
                    }
                }
            },
            keyword: {
                validators: {
                    notEmpty: {
                        message: 'Must submit with a keyword'
                    }
                }
            },
            minrepo: {
                validators: {
                    integer: {
                        message: 'The value is not a Number'
                    }
                }
            },
            follower: {
                validators: {
                    integer: {
                        message: 'The value is not a Number'
                    }
                }
            }
        }
    });
});