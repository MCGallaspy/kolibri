'use strict';
/**
 * Plugin module.
 * Provides the base class for Kolibri Plugins - all Plugins must extend this Base class.
 * @module plugin_base
 */

var Kolibri = require('kolibri');
var _ = require('lodash');
var Backbone = require('backbone');

/**
 * The constructor function for the base Plugin object.
 * @param {object} options - an options hash to set properties of the object.
 * @constructor
 */
var Plugin = function (options) {
    this.name = __plugin_name;
    _.extend(this, _.pick(options, this.plugin_options));
    this.initialize.apply(this, arguments);
    this._register_plugin();
};

/**
 * An array of options to select from the options object passed into the constructor.
 * @type {string[]}
 */
Plugin.prototype.plugin_options = [];

/**
 * Method to automatically register the plugin with the Kolibri core app once it has initialized.
 * @private
 */
Plugin.prototype._register_plugin = function() {
    Kolibri.register_plugin_sync(this);
};

/**
 * A dummy initialization function - this function will be passed anything passed to the constructor.
 * Useful for setting up the plugin before it is registered against the Kolibri core app.
 */
Plugin.prototype.initialize = function() {};

/**
 * Convenience method to unregister the plugin from listening to certain events.
 * @param {string} event - the event name
 * @param {string} method - the name of the method to unbind
 */
Plugin.prototype.stop_listening = function(event, method) {
    Kolibri.stop_listening(event, this, method);
};


// The Backbone Model extend method is a standalone function that is used to extend many Backbone objects.
// We use it here in preference to rolling our own to allow for extension of Plugins.

Plugin.extend = Backbone.Model.extend;

module.exports = Plugin;
