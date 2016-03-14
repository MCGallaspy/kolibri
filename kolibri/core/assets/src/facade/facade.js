'use strict';
/**
 * Facade module.
 * Provides the public API for the Kolibri FrontEnd core app.
 * @module Facade
 */

var Mediator = require('../mediator/mediator');
var _ = require('lodash');

/**
 * Array containing the names of all methods of the Mediator that should be exposed publicly through the Facade.
 * @type {string[]}
 */
var public_methods = [
    'register_plugin_async',
    'register_plugin_sync',
    'stop_listening',
    'trigger'
];

/**
 * Constructor for lib object that exposes third party libraries that we bundle into the core app.
 * @classdesc
 */
var lib = function() {
    this.Backbone = require('backbone');
    this.loglevel = require('loglevel');
    this._ = require('lodash');
};

/**
 * Constructor for Facade object that forms the public API for the Kolibri core app.
 * @constructor
 */
var Kolibri = function() {
    this.lib = new lib();
    var mediator = new Mediator();

    // Bind 'this' value for public methods - those that will be exposed in the Facade.
    _.bindAll(mediator, public_methods);
    this.plugins = mediator._plugin_registry;
    _.extend(this, _.pick(mediator, public_methods));
};

module.exports = Kolibri;
