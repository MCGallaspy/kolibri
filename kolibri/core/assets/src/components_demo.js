'use strict';
// You can add "base" stuff to components.js in this same directory, it's imported with this line.
var components = require('components');
var logging = require('loglevel');
var KolibriModule = require('kolibri_module');

logging.setDefaultLevel(2);

logging.info('Component demo loaded!');


var ComponentDemoPlugin = KolibriModule.extend({

    events: {},

    once: {},

    initialize: function() {
        // This code will be run on page load when you visit http://localhost:8000/component_demo
        // This should be the entry point for your code
        // You can add html to the component_demo.html template.
        logging.info('Demo initialized!');
    }
});


// Add your own code starting here.


// Boilerplate, just let this be!
var cpd = new ComponentDemoPlugin();

// We don't have to export anything.
module.exports = {};
